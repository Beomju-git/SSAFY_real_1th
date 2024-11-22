from django.db import models
from django.conf import settings

# Create your models here.
class TextTermDeposit(models.Model):
    product_type =models.TextField() # 예금/적금 타입 구별
    fin_prdt_cd = models.TextField(unique=True) # 금융 상품 코드
    kor_co_nm = models.TextField() # 금융 회사명
    fin_prdt_nm = models.TextField() # 금융상품명
    etc_note = models.TextField() # 금융상품 설명
    join_deny = models.TextField() # 가입 제한 (1: 제한 없음 2: 서민 전용 3. 일부제한)
    join_member = models.TextField() # 가입대상
    join_way = models.TextField() # 가입 방법
    spcl_cnd = models.TextField() # 우대 조건
    dcls_strt_day = models.TextField() # 공시 시작일
    
class TextTermDepositOptions(models.Model):
    product = models.ForeignKey(TextTermDeposit, on_delete= models.CASCADE)
    fin_prdt_cd = models.TextField() # 금융 상품 코드
    intr_rate_type_nm = models.CharField(max_length=100) # 저축금리 유형명
    intr_rate = models.TextField(null = True) # 저축금리
    intr_rate2 = models.TextField(null =True) # 최고우대 금리
    save_trm = models.TextField() # 저축 기간 단위(개월)

class TermDeposit(models.Model):
    zzimed_product = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='zzim_product')
    product_type =models.TextField() # 예금/적금 타입 구별
    fin_prdt_cd = models.TextField(unique=True) # 금융 상품 코드
    kor_co_nm = models.TextField() # 금융 회사명
    fin_prdt_nm = models.TextField() # 금융상품명
    etc_note = models.TextField() # 금융상품 설명
    join_deny = models.IntegerField() # 가입 제한 (1: 제한 없음 2: 서민 전용 3. 일부제한)
    join_member = models.TextField() # 가입대상
    join_way = models.TextField() # 가입 방법
    spcl_cnd = models.TextField() # 우대 조건
    dcls_strt_day = models.TextField() # 공시 시작일
    
class TermDepositOptions(models.Model):
    product = models.ForeignKey(TermDeposit, on_delete= models.CASCADE)
    fin_prdt_cd = models.TextField() # 금융 상품 코드
    intr_rate_type_nm = models.CharField(max_length=100) # 저축금리 유형명
    intr_rate = models.FloatField(null = True) # 저축금리
    intr_rate2 = models.FloatField(null =True) # 최고우대 금리
    save_trm = models.IntegerField() # 저축 기간 단위(개월)
    
    
class Savings(models.Model):
    fin_prdt_cd = models.TextField(unique=True) # 금융 상품 코드
    kor_co_nm = models.TextField() # 금융 회사명
    fin_prdt_nm = models.TextField() # 금융상품명
    etc_note = models.TextField() # 금융상품 설명
    join_deny = models.IntegerField() # 가입 제한 (1: 제한 없음 2: 서민 전용 3. 일부제한)
    join_member = models.TextField() # 가입대상
    join_way = models.TextField() # 가입 방법
    spcl_cnd = models.TextField() # 우대 조건
    dcls_strt_day = models.TextField() # 공시 시작일
    
class SavingsOptions(models.Model):
    product = models.ForeignKey(Savings, on_delete= models.CASCADE)
    fin_prdt_cd = models.TextField() # 금융 상품 코드
    intr_rate_type_nm = models.CharField(max_length=100) # 저축금리 유형명
    intr_rate = models.FloatField(null = True) # 저축금리
    intr_rate2 = models.FloatField(null =True) # 최고우대 금리
    save_trm = models.IntegerField() # 저축 기간 단위(개월)    
    
 ##########
 #대출 정보 저장   
class LoanProducts(models.Model):
    fin_prdt_cd = models.TextField(unique=True) # 금융상품 코드
    kor_co_nm = models.TextField() #금융회사 명
    fin_prdt_nm = models.TextField() # 금융 상품명
    join_way = models.TextField() # 가입 방법
    loan_inci_expn = models.TextField() # 대출 부대비용
    erly_rpay_fee = models.TextField() # 중도상환 수수료
    dly_rate = models.TextField() # 연체 이자율
    loan_lmt = models.TextField(null=True) # 대출한도
    dcls_strt_day = models.TextField()  #공시 시작일

class LoanOptions(models.Model):
    product = models.ForeignKey(LoanProducts, on_delete= models.CASCADE)
    fin_prdt_cd = models.TextField() # 금융상품 코드
    mrtg_type_nm =  models.TextField(default='전세자금대출', null =True, blank= True) # 담보유형
    rpay_type_nm =  models.TextField() # 대출상환유형
    lend_rate_type_nm =  models.TextField() # 대출금리유형
    lend_rate_min = models.FloatField(null =True) # 대출금리_최저
    lend_rate_max = models.FloatField(null =True) # 대출금리_최고
    
#################   
###신용 대출
class CreditLoanProducts(models.Model):
    fin_prdt_cd = models.TextField(unique=True) # 금융상품 코드
    kor_co_nm = models.TextField() #금융회사 명
    fin_prdt_nm = models.TextField() # 금융 상품명
    join_way = models.TextField(null= True) # 가입 방법
    crdt_prdt_type_nm = models.TextField() # 대출 종류명
    dcls_strt_day = models.TextField()  #공시 시작일    

class CreditLoanOptions(models.Model):
    product = models.ForeignKey(CreditLoanProducts, on_delete= models.CASCADE)
    fin_prdt_cd = models.TextField() # 금융상품 코드
    crdt_lend_rate_type_nm =  models.TextField() # 금리 구분
    crdt_grad_1	= models.FloatField(null =True) # 900점 초과 [소수점 2자리]
    crdt_grad_4 = models.FloatField(null =True) #	801~900점 [소수점 2자리]
    crdt_grad_5 = models.FloatField(null =True) #	701~800점 [소수점 2자리]
    crdt_grad_6 = models.FloatField(null =True) #	601~700점 [소수점 2자리]
    crdt_grad_10 = models.FloatField(null =True) #	501~600점 [소수점 2자리]
    crdt_grad_11 = models.FloatField(null =True) #	401~500점 [소수점 2자리]
    crdt_grad_12 = models.FloatField(null =True) #	301~400점 [소수점 2자리]
    crdt_grad_13 = models.FloatField(null =True) #	300점 이하 [소수점 2자리]
    crdt_grad_avg = models.FloatField(null =True) #	평균 금리 [소수점 2자리]
        