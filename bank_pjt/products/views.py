from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests
from .models import TermDeposit, TermDepositOptions, Savings, SavingsOptions, LoanOptions, LoanProducts, CreditLoanProducts, CreditLoanOptions
from .serializers import TermDepositSerializer, TermDepositOptionSerializer, TermDepositAllSerializer, SavingsSerializer, SavingsOptionSerializer, SavingsAllSerializer, LoanSerializer, LoanOptionSerializer, LoanAllSerializer, CreditLoanAllSerializer, CreditLoanOptionSerializer, CreditLoanSerializer
# 회원가입을 위해
from rest_framework.decorators import authentication_classes
from rest_framework.authentication import TokenAuthentication, BasicAuthentication

BASE_URL = 'http://finlife.fss.or.kr/finlifeapi'
API_KEY = '815324d1a571acce6fbe7341cfa853f1'
# Create your views here.

# 정기예금 가져오기
@api_view(['GET'])
def term_deposit_update(request):
    URL = 'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json'  # 슬래시 수정
    print(URL)
    topFinGrpNos = [ '020000', '030300' ]# 은행, 저축은행
    
    for topFinGrpNo in topFinGrpNos:
        params = {
            'auth': API_KEY,  # 변수명 오타 수정 및 일관성 유지
            'topFinGrpNo': topFinGrpNo,
            'pageNo': 1
        }
        response = requests.get(URL, params=params).json()
        products = response.get('result').get('baseList')
        ## 예금 정보 저장
        for product in products:
            fin_prdt_cd = product.get('fin_prdt_cd',)
            kor_co_nm = product.get('kor_co_nm')
            fin_prdt_nm = product.get('fin_prdt_nm')
            etc_note = product.get('etc_note' )
            join_deny = product.get('join_deny')
            join_member =product.get('join_member')
            join_way = product.get('join_way')
            spcl_cnd = product.get('spcl_cnd')
            dcls_strt_day = product.get('dcls_strt_day')
            save_data ={
                'fin_prdt_cd' : fin_prdt_cd,
                'kor_co_nm' : kor_co_nm,
                'fin_prdt_nm' : fin_prdt_nm,
                'etc_note': etc_note,
                'join_deny' : join_deny,
                'join_member': join_member,
                'join_way' : join_way,
                'spcl_cnd' : spcl_cnd,
                'dcls_strt_day':dcls_strt_day,
            }
            if TermDeposit.objects.filter(
                fin_prdt_cd = fin_prdt_cd, 
                ).exists():
                continue
            serializer = TermDepositSerializer(data =save_data)
            if serializer.is_valid(raise_exception= True):
                serializer.save()  
                
        #option 저장
        products_options = response.get('result').get('optionList') 
        for option in products_options:
            fin_prdt_cd = option.get('fin_prdt_cd',)
            intr_rate_type_nm = option.get('intr_rate_type_nm')
            intr_rate = option.get('intr_rate', -1)
            intr_rate2 = option.get('intr_rate2',-1 )
            save_trm = option.get('save_trm')
            save_option_data ={
                'fin_prdt_cd' : fin_prdt_cd,
                'intr_rate_type_nm' : intr_rate_type_nm,
                'intr_rate' : intr_rate,
                'intr_rate2': intr_rate2,
                'save_trm' : save_trm,
            }      
            if TermDepositOptions.objects.filter(
                fin_prdt_cd = fin_prdt_cd, intr_rate_type_nm = intr_rate_type_nm, intr_rate = intr_rate,
                intr_rate2 = intr_rate2, save_trm = save_trm
                ).exists():
                continue
            serializer = TermDepositOptionSerializer(data =save_option_data)
            
            product = TermDeposit.objects.get(fin_prdt_cd=fin_prdt_cd)
            if serializer.is_valid(raise_exception = True):
                serializer.save(product = product)   
        
        
    return Response({'message' : '검색 완료'})

# 정기 예금 전체 조회
@api_view(["GET"])
def term_deposit(request):
    deposits = TermDeposit.objects.all()
    serializers = TermDepositAllSerializer(deposits, many=True)
    return Response(serializers.data)


# 정기 예금 상세 조회
@api_view(["GET"])
@authentication_classes([TokenAuthentication, BasicAuthentication])
def term_deposit_detail(request,fin_prdt_cd):
    deposit = TermDeposit.objects.get(fin_prdt_cd=fin_prdt_cd)
    serializer = TermDepositSerializer(deposit)
    return Response(serializer.data)


#######################
###################################
###적금

# 적금 가져오기
@api_view(['GET'])
def savings_update(request):
    URL = 'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json'  # 슬래시 수정
    print(URL)
    topFinGrpNos = [ '020000', '030300' ]# 은행, 저축은행
    
    for topFinGrpNo in topFinGrpNos:
        params = {
            'auth': API_KEY,  # 변수명 오타 수정 및 일관성 유지
            'topFinGrpNo': topFinGrpNo,
            'pageNo': 1
        }
        response = requests.get(URL, params=params).json()
        products = response.get('result').get('baseList')
        ## 적금 정보 저장
        for product in products:
            fin_prdt_cd = product.get('fin_prdt_cd',)
            kor_co_nm = product.get('kor_co_nm')
            fin_prdt_nm = product.get('fin_prdt_nm')
            etc_note = product.get('etc_note' )
            join_deny = product.get('join_deny')
            join_member =product.get('join_member')
            join_way = product.get('join_way')
            spcl_cnd = product.get('spcl_cnd')
            dcls_strt_day = product.get('dcls_strt_day')
            save_data ={
                'fin_prdt_cd' : fin_prdt_cd,
                'kor_co_nm' : kor_co_nm,
                'fin_prdt_nm' : fin_prdt_nm,
                'etc_note': etc_note,
                'join_deny' : join_deny,
                'join_member': join_member,
                'join_way' : join_way,
                'spcl_cnd' : spcl_cnd,
                'dcls_strt_day':dcls_strt_day,
            }
            if Savings.objects.filter(
                fin_prdt_cd = fin_prdt_cd, 
                ).exists():
                continue
            serializer = SavingsSerializer(data =save_data)
            if serializer.is_valid(raise_exception= True):
                serializer.save()  
                
        #option 저장
        products_options = response.get('result').get('optionList') 
        for option in products_options:
            fin_prdt_cd = option.get('fin_prdt_cd',)
            intr_rate_type_nm = option.get('intr_rate_type_nm')
            intr_rate = option.get('intr_rate', -1)
            intr_rate2 = option.get('intr_rate2',-1 )
            save_trm = option.get('save_trm')
            save_option_data ={
                'fin_prdt_cd' : fin_prdt_cd,
                'intr_rate_type_nm' : intr_rate_type_nm,
                'intr_rate' : intr_rate,
                'intr_rate2': intr_rate2,
                'save_trm' : save_trm,
            }      
            if SavingsOptions.objects.filter(
                fin_prdt_cd = fin_prdt_cd, intr_rate_type_nm = intr_rate_type_nm, intr_rate = intr_rate,
                intr_rate2 = intr_rate2, save_trm = save_trm
                ).exists():
                continue
            serializer = SavingsOptionSerializer(data =save_option_data)
            
            product = Savings.objects.get(fin_prdt_cd=fin_prdt_cd)
            if serializer.is_valid(raise_exception = True):
                serializer.save(product = product)   
    return Response({'message' : '검색 완료'})

# 적금 전체 조회
@api_view(["GET"])
def savings(request):
    deposits = Savings.objects.all()
    serializers = SavingsAllSerializer(deposits, many=True)
    return Response(serializers.data)


# 적금 상세 조회asdf
@api_view(["GET"])
@authentication_classes([TokenAuthentication, BasicAuthentication])
def savings_detail(request,fin_prdt_cd):
    deposit = Savings.objects.get(fin_prdt_cd=fin_prdt_cd)
    serializer = SavingsSerializer(deposit)
    return Response(serializer.data)

###주택담보 대출####################################################
@api_view(["GET"])
def loanproduct_update(request):
    loans=['mortgageLoanProductsSearch','rentHouseLoanProductsSearch']
    for loan in loans:
        URL = f'http://finlife.fss.or.kr/finlifeapi/{loan}.json'  # 슬래시 수정
        print(URL)
        topFinGrpNos = [ '020000', '030300', '050000' ]# 은행, 저축은행
        
        for topFinGrpNo in topFinGrpNos:
            params = {
                'auth': API_KEY,  # 변수명 오타 수정 및 일관성 유지
                'topFinGrpNo': topFinGrpNo,
                'pageNo': 1
            }
            response = requests.get(URL, params=params).json()
            products = response.get('result').get('baseList')
            ## 적금 정보 저장
            for product in products:
                fin_prdt_cd = product.get('fin_prdt_cd',)
                kor_co_nm = product.get('kor_co_nm')
                fin_prdt_nm = product.get('fin_prdt_nm')
                join_way = product.get('join_way' )
                loan_inci_expn = product.get('loan_inci_expn')
                erly_rpay_fee =product.get('erly_rpay_fee')
                dly_rate = product.get('dly_rate')
                loan_lmt = product.get('loan_lmt')
                dcls_strt_day = product.get('dcls_strt_day')
                save_data ={
                    'fin_prdt_cd' : fin_prdt_cd,
                    'kor_co_nm' : kor_co_nm,
                    'fin_prdt_nm' : fin_prdt_nm,
                    'loan_inci_expn': loan_inci_expn,
                    'erly_rpay_fee' : erly_rpay_fee,
                    'dly_rate': dly_rate,
                    'loan_lmt' : loan_lmt,
                    'join_way' : join_way,
                    'dcls_strt_day':dcls_strt_day,
                }
                if LoanProducts.objects.filter(
                    fin_prdt_cd = fin_prdt_cd, 
                    ).exists():
                    continue
                serializer = LoanSerializer(data =save_data)
                if serializer.is_valid(raise_exception= True):
                    serializer.save()  
                    
            #option 저장
            products_options = response.get('result').get('optionList') 
            for option in products_options:
                fin_prdt_cd = option.get('fin_prdt_cd',)
                mrtg_type_nm = option.get('mrtg_type_nm', '전세자금대출')
                rpay_type_nm = option.get('rpay_type_nm')
                lend_rate_type_nm = option.get('lend_rate_type_nm')
                lend_rate_min = option.get('lend_rate_min', -1)
                lend_rate_max = option.get('ilend_rate_maxntr_rate2',-1 )
                save_option_data ={
                    'fin_prdt_cd' : fin_prdt_cd,
                    'mrtg_type_nm' : mrtg_type_nm,
                    'rpay_type_nm' : rpay_type_nm,
                    'lend_rate_type_nm': lend_rate_type_nm,
                    'lend_rate_min' : lend_rate_min,
                    'lend_rate_max' : lend_rate_max,
                }      
                if LoanOptions.objects.filter(
                    fin_prdt_cd = fin_prdt_cd
                    ).exists():
                    continue
                serializer = LoanOptionSerializer(data =save_option_data)
                
                product = LoanProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
                if serializer.is_valid(raise_exception = True):
                    serializer.save(product = product)   
    return Response({'message' : '검색 완료'})

@api_view(['GET'])
def loanproduct(request):
    deposits = LoanProducts.objects.all()
    serializers = LoanAllSerializer(deposits, many=True)
    print(1)
    return Response(serializers.data)



######################
##신용 대출
@api_view(["GET"])
def creditloan_update(request):
    URL = 'http://finlife.fss.or.kr/finlifeapi/creditLoanProductsSearch.json'  # 슬래시 수정
    print(URL)
    topFinGrpNos = [ '020000','030200', '030300', '050000' ]# 은행, 저축은행
    
    for topFinGrpNo in topFinGrpNos:
        params = {
            'auth': API_KEY,  # 변수명 오타 수정 및 일관성 유지
            'topFinGrpNo': topFinGrpNo,
            'pageNo': 1
        }
        response = requests.get(URL, params=params).json()
        products = response.get('result').get('baseList')
        ## 적금 정보 저장
        for product in products:
            fin_prdt_cd = product.get('fin_prdt_cd',)
            kor_co_nm = product.get('kor_co_nm')
            fin_prdt_nm = product.get('fin_prdt_nm')
            join_way = product.get('join_way',1 )
            crdt_prdt_type_nm = product.get('crdt_prdt_type_nm')
            dcls_strt_day =product.get('dcls_strt_day')
            save_data ={
                'fin_prdt_cd' : fin_prdt_cd,
                'kor_co_nm' : kor_co_nm,
                'fin_prdt_nm' : fin_prdt_nm,
                'join_way': join_way,
                'crdt_prdt_type_nm' : crdt_prdt_type_nm,
                'dcls_strt_day': dcls_strt_day,
            }
            if CreditLoanProducts.objects.filter(
                fin_prdt_cd = fin_prdt_cd, 
                ).exists():
                continue
            serializer = CreditLoanSerializer(data =save_data)
            if serializer.is_valid(raise_exception= True):
                serializer.save()  
                
        #option 저장
        products_options = response.get('result').get('optionList') 
        for option in products_options:
            fin_prdt_cd = option.get('fin_prdt_cd',)
            crdt_lend_rate_type_nm = option.get('crdt_lend_rate_type_nm')
            crdt_grad_1 = option.get('crdt_grad_1')
            crdt_grad_4 = option.get('crdt_grad_4')
            crdt_grad_5 = option.get('crdt_grad_5')
            crdt_grad_6 = option.get('crdt_grad_6')
            crdt_grad_10 = option.get('crdt_grad_10')
            crdt_grad_11 = option.get('crdt_grad_11')
            crdt_grad_12 = option.get('crdt_grad_12')
            crdt_grad_13 = option.get('crdt_grad_13')
            crdt_grad_avg = option.get('crdt_grad_avg')
            save_option_data ={
                'fin_prdt_cd' : fin_prdt_cd,
                'crdt_lend_rate_type_nm' : crdt_lend_rate_type_nm,
                'crdt_grad_1' : crdt_grad_1,
                'crdt_grad_4': crdt_grad_4,
                'crdt_grad_5' : crdt_grad_5,
                'crdt_grad_6' : crdt_grad_6,
                'crdt_grad_10' : crdt_grad_10,
                'crdt_grad_11' : crdt_grad_11,
                'crdt_grad_12' : crdt_grad_12,
                'crdt_grad_13' : crdt_grad_13,
                'crdt_grad_avg' : crdt_grad_avg,
            }      
            if CreditLoanOptions.objects.filter(
                fin_prdt_cd = fin_prdt_cd
                ).exists():
                continue
            serializer = CreditLoanOptionSerializer(data =save_option_data)
            
            product = CreditLoanProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
            if serializer.is_valid(raise_exception = True):
                serializer.save(product = product)   
    return Response({'message' : '검색 완료'})

@api_view(['GET'])
def creditloan(request):
    deposits = CreditLoanProducts.objects.all()
    serializers = CreditLoanAllSerializer(deposits, many=True)
    print(1)
    return Response(serializers.data)

# ###선제담보 대출####################################################
# @api_view(["GET"])
# def renthousloan_update(request):
#     URL = 'http://finlife.fss.or.kr/finlifeapi/rentHouseLoanProductsSearch.json'  # 슬래시 수정
#     print(URL)
#     topFinGrpNos = [ '020000', '030300', '050000' ]# 은행, 저축은행
    
#     for topFinGrpNo in topFinGrpNos:
#         params = {
#             'auth': API_KEY,  # 변수명 오타 수정 및 일관성 유지
#             'topFinGrpNo': topFinGrpNo,
#             'pageNo': 1
#         }
#         response = requests.get(URL, params=params).json()
#         products = response.get('result').get('baseList')
#         ## 적금 정보 저장
#         for product in products:
#             fin_prdt_cd = product.get('fin_prdt_cd',)
#             kor_co_nm = product.get('kor_co_nm')
#             fin_prdt_nm = product.get('fin_prdt_nm')
#             join_way = product.get('join_way' )
#             loan_inci_expn = product.get('loan_inci_expn')
#             erly_rpay_fee =product.get('erly_rpay_fee')
#             dly_rate = product.get('dly_rate')
#             loan_lmt = product.get('loan_lmt')
#             dcls_strt_day = product.get('dcls_strt_day')
#             save_data ={
#                 'fin_prdt_cd' : fin_prdt_cd,
#                 'kor_co_nm' : kor_co_nm,
#                 'fin_prdt_nm' : fin_prdt_nm,
#                 'loan_inci_expn': loan_inci_expn,
#                 'erly_rpay_fee' : erly_rpay_fee,
#                 'dly_rate': dly_rate,
#                 'loan_lmt' : loan_lmt,
#                 'join_way' : join_way,
#                 'dcls_strt_day':dcls_strt_day,
#             }
#             if LoanProducts.objects.filter(
#                 fin_prdt_cd = fin_prdt_cd, 
#                 ).exists():
#                 continue
#             serializer = LoanSerializer(data =save_data)
#             if serializer.is_valid(raise_exception= True):
#                 serializer.save()  
                
#         #option 저장
#         products_options = response.get('result').get('optionList') 
#         for option in products_options:
#             fin_prdt_cd = option.get('fin_prdt_cd',)
#             mrtg_type_nm = option.get('mrtg_type_nm', '전세자금대출')
#             rpay_type_nm = option.get('rpay_type_nm')
#             lend_rate_type_nm = option.get('lend_rate_type_nm')
#             lend_rate_min = option.get('lend_rate_min', -1)
#             lend_rate_max = option.get('ilend_rate_maxntr_rate2',-1 )
#             save_option_data ={
#                 'fin_prdt_cd' : fin_prdt_cd,
#                 'mrtg_type_nm' : mrtg_type_nm,
#                 'rpay_type_nm' : rpay_type_nm,
#                 'lend_rate_type_nm': lend_rate_type_nm,
#                 'lend_rate_min' : lend_rate_min,
#                 'lend_rate_max' : lend_rate_max,
#             }      
#             if LoanOptions.objects.filter(
#                 fin_prdt_cd = fin_prdt_cd
#                 ).exists():
#                 continue
#             serializer = LoanOptionSerializer(data =save_option_data)
            
#             product = LoanProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
#             if serializer.is_valid(raise_exception = True):
#                 serializer.save(product = product)   
#     return Response({'message' : '검색 완료'})

# @api_view(['GET'])
# def renthousloan(request):
#     deposits = LoanProducts.objects.all()
#     serializers = LoanAllSerializer(deposits, many=True)
#     print(1)
#     return Response(serializers.data)