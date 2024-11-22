from django.urls import path, include
from . import views


urlpatterns = [
    # 정기 예금 가져오기
    path('term_deposit/update/', views.term_deposit_update, name='term_deposit_update'),
    path('term_deposit_text/update/', views.term_deposit_text_update, name='term_deposit_text_update'),
    # 정기 예금 전체 조회( 정기 예금 상품의 기간 별 금리 포함)
    path('term_deposit/', views.term_deposit, name='term_deposit'),
    # 상품 찜 하기
    path('term_deposit/detail/<fin_prdt_cd>/recommend/', views.term_deposit_recommend, name='term_deposit_recommend'), 
    # 상세 정기 예금 상품 조회
    path('term_deposit/detail/<fin_prdt_cd>/', views.term_deposit_detail, name='term_deposit_detail'), 
    # 적금 가져오기
    path('savings/update/', views.savings_update, name='savings_update'),
    # 적금 전체 조회( 정기 예금 상품의 기간 별 금리 포함)
    path('savings/', views.savings, name='savings'),
    # 상세 적금 상품 조회
    path('savings/detail/<fin_prdt_cd>/', views.savings_detail, name='savings_detail'),
    
    # 주택담보/전세자금 대출 가져오기
    path('loanproduct/update/', views.loanproduct_update, name='loanproduct_update'),
    # 주탁 담보/전세자금 대출
    path('loanproduct/', views.loanproduct, name='loanproduct'),
    
    # 전세자금 대출 가져오기
    path('creditloan/update/', views.creditloan_update, name='creditloan_update'),
    # 전세자금 담보 대출
    path('creditloan/', views.creditloan, name='creditloan'),


]
