from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Exchange
from .serializers import ExchangeSerializers
import requests
from datetime import datetime
from django.http import JsonResponse
# Create your views here.

BASE_URL = 'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON'
API_KEY = 'Arq4VjZpxXOo3Ga4Ht6eSu4AGwhbn41u'


@api_view(['GET'])
def update(request):
    current_date = datetime.now().strftime('%Y%m%d')
    date_object = datetime.strptime(current_date, '%Y%m%d').date()
    params ={
        'authkey': API_KEY,
        # 'searchdate': 'default', // default는 현재 
        'searchdate': '20241113',
        'data': 'AP01' #AP01 환율, AP02 대출금리, AP03 국제금리
    }
    responses = requests.get(BASE_URL, params=params).json()
    for response in responses:
        cur_unit= response.get('cur_unit')
        country = response.get('cur_nm')
        rate = float(response.get('kftc_deal_bas_r').replace(',',''))

        #이미 환율정보가 저장되어있으면 환율 값만 업데이트
        is_existed= Exchange.objects.filter(country=country).first()
        print(is_existed)
        if is_existed:
            is_existed.rate = rate
            is_existed.date = date_object
            is_existed.save()
        else:
            save_data ={
                'country' :country,
                'rate':rate,
                'cur_unit':cur_unit,
                'date' : date_object
            }
            serializer = ExchangeSerializers(data=save_data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
    return JsonResponse({'message':'업데이트 완료'})

@api_view(['GET'])
def exchanges(request):
    exchanges = Exchange.objects.all()
    serializer = ExchangeSerializers(exchanges, many= True)
    return Response(serializer.data)