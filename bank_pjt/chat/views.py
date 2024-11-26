# chat/views.py

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from products.models import TermDeposit  # TermDepositProduct 대신 TermDeposit 사용
from .models import StandardizedTermDeposit  # 추가
from .serializers import StandardizedTermDepositSerializer
from groq import Groq
import json
import re  # 파일 상단에 추가
import time
from groq import RateLimitError
from rest_framework.decorators import api_view
import requests
from bs4 import BeautifulSoup
from .services import ProductAnalyzer

def process_data_with_groq(data_row, max_retries=3, delay=4):
    for attempt in range(max_retries):
        try:
            print(f"\n처리 시작: 상품코드 {data_row.fin_prdt_cd}")  # 디버깅 로그 추가
            client = Groq()
            messages = [
                {
                    "role": "system",
                    "content": """금융 데이터 표준화 전문가입니다. 다음 규칙을 엄격히 따르세요:
1. 응답은 반드시 아래 형식의 JSON만 출력합니다
2. 모든 필드는 필수입니다
3. 숫자는 문자열이 아닌 숫자로 표현합니다
4. 알 수 없는 값은 null로 표합니다"""
                },
                {
                    "role": "user",
                    "content": f"""다음 금융 상품 정보를 정확한 JSON으로 변환하세요:

상품명: {data_row.fin_prdt_nm}
기타사항: {data_row.etc_note}
가입대상: {data_row.join_member}
가입방법: {data_row.join_way}
우대조건: {data_row.spcl_cnd}

반드시 다음 JSON 형식으로만 응답하세요:
{{
    "상품명": "{data_row.fin_prdt_nm}",
    "최소가입금액": null,
    "최대가입금액": null,
    "가입기간": "실제기간" 없다면 "null",
    "이자율": null,
    "가입대상": "{data_row.join_member}",
    "가입방법": "{data_row.join_way}",
    "우대조건": "{data_row.spcl_cnd}"
}}"""
                }
            ]

            print("API 요청 시작...")  # 디버깅 로그 추가
            completion = client.chat.completions.create(
                model="llama-3.1-70b-versatile",
                messages=messages,
                temperature=0,
                max_tokens=500,
                top_p=1,
                stream=False,
                stop=None
            )
            print("API 응답 수신...")  # 디버깅 로그 추가

            response_content = completion.choices[0].message.content.strip()
            print(f"받은 응답:\n{response_content}")  # 디버깅 로그 추가
            
            try:
                json_data = json.loads(response_content)
                required_fields = ["상품명", "최소가입금액", "최대가입금액", "가입기간", 
                                 "이자율", "가입대상", "가입방법", "우대조건"]
                
                if all(field in json_data for field in required_fields):
                    try:
                        parse_and_save(response_content, data_row)
                        return True
                    except Exception as e:
                        print(f"저장 중 오류 발생: {str(e)}")
                        continue
                
                print(f"필수 필드 누락. 상품코드: {data_row.fin_prdt_cd}")
                continue
                
            except json.JSONDecodeError:
                print(f"JSON 파싱 실패. 상품코드: {data_row.fin_prdt_cd}")
                continue

        except Exception as e:
            print(f"처리 중 오류: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(delay)
                delay *= 2
                continue
            return False

    return False

def clean_text_field(value):
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    return str(value).strip()

def parse_amount(amount_str):
    if amount_str is None:
        return None
    if isinstance(amount_str, (int, float)):
        return float(amount_str)
    if isinstance(amount_str, str):
        amount_str = amount_str.replace(',', '').replace('원', '').replace('이상', '').strip()
        try:
            return float(amount_str)
        except ValueError:
            return None
    return None

def parse_interest_rate(rate_str):
    if rate_str and isinstance(rate_str, str):
        rate_str = rate_str.replace('%', '').strip()
        try:
            return float(rate_str)
        except ValueError:
            return None
    return None

def parse_and_save(response_content, data_row):
    if response_content is None:
        print(f"응답 데이터가 없습니다. 상품코드: {data_row.fin_prdt_cd}")
        return

    try:
        standardized_data = json.loads(response_content)

        # 공통 데이터 딕셔너리 생성
        common_data = {
            'fin_prdt_cd': data_row.fin_prdt_cd,
            'fin_prdt_nm': standardized_data.get('상품명', data_row.fin_prdt_nm),
            'min_join_amount': parse_amount(standardized_data.get('최소가입금액')),
            'max_join_amount': parse_amount(standardized_data.get('최대가입금액')),
            'join_period': standardized_data.get('가입기간') or "정보없음",
            'interest_rate': parse_interest_rate(standardized_data.get('이자율')),
            'join_member': clean_text_field(standardized_data.get('가입대상', data_row.join_member)),
            'join_way': clean_text_field(standardized_data.get('가입방법', data_row.join_way)),
            'spcl_cnd': clean_text_field(standardized_data.get('우대조건', data_row.spcl_cnd)),
        }

        try:
            existing_product = StandardizedTermDeposit.objects.get(fin_prdt_cd=data_row.fin_prdt_cd)
            serializer = StandardizedTermDepositSerializer(existing_product, data=common_data, partial=True)
        except StandardizedTermDeposit.DoesNotExist:
            serializer = StandardizedTermDepositSerializer(data=common_data)

        if serializer.is_valid():
            serializer.save()
        else:
            print(f"시리얼라이저 유효성 검사 오류: {serializer.errors}")
            print(f"문제가 된 데이터: {common_data}")
            
    except Exception as e:
        print(f"데이터 처리 중 오류 발생: {str(e)}")

@api_view(['GET'])
def run_standardization_view(request):
    try:
        products = TermDeposit.objects.all()
        batch_size = 5
        success_count = 0
        fail_count = 0
        
        for i in range(0, len(products), batch_size):
            batch = products[i:i+batch_size]
            for data_row in batch:
                try:
                    if process_data_with_groq(data_row):
                        success_count += 1
                    else:
                        fail_count += 1
                    time.sleep(1)
                except Exception as e:
                    print(f"Error processing product {data_row.fin_prdt_cd}: {str(e)}")
                    fail_count += 1
                    continue
            
            if i + batch_size < len(products):
                time.sleep(5)
        
        return JsonResponse({
            'message': '데이터 표준화가 완료되었습니다.',
            'success_count': success_count,
            'fail_count': fail_count
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_product_recommendation(self, user_message, intent_data):
    try:
        products = TermDeposit.objects.all()
        product_list = [f"{d.fin_prdt_nm}({d.kor_co_nm})" for d in products]
        
        messages = [
            {
                "role": "system",
                "content": """당신은 금융 상품 추천 전문가입니다. 
주의사항:
1. 반드시 제공된 상품 목록에서만 선택하세요
2. 목록에 없는 상품은 절대 추천하지 마세요
3. 다음 형식으로 정확히 답변하세요:
{
    "product": "상품명(은행명)",
    "reason": "추천 이유",
    "details": "상품 특징 설명",
    "market_analysis": "현재 시장에서의 위치"
}"""
            },
            {
                "role": "user",
                "content": f"""
사용자 요구사항: {user_message}
의도: {intent_data['type']}
키워드: {intent_data['keyword']}

선택 가능한 상품 목록:
{', '.join(product_list)}

위 목록에 있는 상품 중에서만 선택하여 추천해주세요."""
            }
        ]

        completion = self.client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=messages,
            temperature=0.1,  # 온도를 낮춰서 더 보수적인 응답 유도
            max_tokens=1000,
            top_p=1,
            stream=False,
            stop=None
        )

        response = completion.choices[0].message.content.strip()
        recommendation = json.loads(response)
        
        # 추천 결과 검증
        if not validate_recommendation(recommendation, product_list):
            return {
                "product": "추천 실패",
                "reason": "죄송합니다. 요청하신 조건에 맞는 상품을 찾을 수 없습니다.",
                "details": "다른 조건으로 다시 시도해주세요.",
                "market_analysis": "현재 이용할 수 없습니다."
            }
            
        return recommendation

    except Exception as e:
        print(f"Recommendation error: {str(e)}")
        return {
            "product": "추천 실패",
            "reason": "죄송합니다. 추천을 생성하는 중 오류가 발생했습니다.",
            "details": "잠시 후 다시 시도해주세요.",
            "market_analysis": "현재 이용할 수 없습니다."
        }

@api_view(['POST'])
def recommend_products(request):
    try:
        user_input = request.data.get('user_input')
        if not user_input:
            return JsonResponse({'error': '사용자 입력이 필요합니다'}, status=400)

        # DB에서 모든 상품 정보 가져오기
        term_deposits = TermDeposit.objects.all()
        savings = Savings.objects.all()
        loans = LoanProducts.objects.all()
        credit_loans = CreditLoanProducts.objects.all()

        # 상품 정보를 컨텍스트에 추가
        context = f"""
사용자 입력: {user_input}

참고할 수 있는 상품들:
1. 정기예금: {', '.join([f"{d.fin_prdt_nm}({d.kor_co_nm})" for d in term_deposits])}
2. 적금: {', '.join([f"{s.fin_prdt_nm}({s.kor_co_nm})" for s in savings])}
3. 대출: {', '.join([f"{l.fin_prdt_nm}({l.kor_co_nm})" for l in loans])}
4. 신용대출: {', '.join([f"{c.fin_prdt_nm}({c.kor_co_nm})" for c in credit_loans])}
"""

        recommendation = get_product_recommendation(context)
        if recommendation:
            return JsonResponse({
                'recommendation': recommendation,
                'status': 'success'
            })
        else:
            return JsonResponse({
                'error': '추천을 생성하는 중 오류가 발생했습니다',
                'status': 'error'
            }, status=500)

    except Exception as e:
        return JsonResponse({
            'error': str(e),
            'status': 'error'
        }, status=500)

def search_duckduckgo(query):
    """Search DuckDuckGo and return the first result."""
    url = f"https://duckduckgo.com/?q={query}&t=h_&ia=web"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all('a', class_='result__a', limit=1)  # Get the first result
    if results:
        return results[0].text  # Return the text of the first result
    return None

@api_view(['POST'])
def chat_recommend(request):
    try:
        user_message = request.data.get('message')
        session_id = request.data.get('session_id', 'default')
        
        if not user_message:
            return JsonResponse({'error': '메시지가 필요합니다'}, status=400)

        analyzer = ProductAnalyzer(session_id)
        intent_data = analyzer.analyze_intent(user_message)
        recommendation = analyzer.get_product_recommendation(user_message, intent_data)
        
        if recommendation:
            analyzer.context_manager.add_context(
                message=user_message,
                response=json.dumps(recommendation),
                context_data={'intent': intent_data}
            )
            
            return JsonResponse({
                'message': recommendation,
                'status': 'success'
            })
        
        return JsonResponse({
            'error': '추천을 생성할 수 없습니다',
            'status': 'error'
        }, status=500)

    except Exception as e:
        print(f"Error in chat_recommend: {str(e)}")
        return JsonResponse({
            'error': str(e),
            'status': 'error'
        }, status=500)

def validate_recommendation(recommendation, available_products):
    """추천된 상품이 실제 DB에 존재하는지 검증"""
    if not recommendation or 'product' not in recommendation:
        return False
        
    # 정확한 상품명 매칭을 위해 정규화된 문자열 비교
    recommended_product = recommendation['product'].strip()
    
    # 정확히 일치하는 상품이 있는지 확인
    exact_match = any(product.strip() == recommended_product for product in available_products)
    if exact_match:
        return True
        
    # 부분 일치하는 상품이 있는지 확인
    partial_matches = [product for product in available_products 
                      if recommended_product in product or product in recommended_product]
    
    if partial_matches:
        # 가장 유사한 상품으로 recommendation 업데이트
        recommendation['product'] = partial_matches[0]
        return True
        
    return False
