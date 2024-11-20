from rest_framework import serializers
from .models import TermDeposit, TermDepositOptions, Savings, SavingsOptions, LoanProducts, LoanOptions, CreditLoanProducts, CreditLoanOptions

# 정기 예금 update
class TermDepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermDeposit
        fields='__all__'
        read_only_fields =('zzimed_product',)
        
# 정기 예금 option update
class TermDepositOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermDepositOptions
        fields='__all__'
        read_only_fields =('product',)

        
# 정기 예금 전체 조회     
class TermDepositAllSerializer(serializers.ModelSerializer):
    class TermDepositOptionTermSerializer(serializers.ModelSerializer):
        class Meta:
            model = TermDepositOptions
            fields=('save_trm', 'intr_rate',)
    termdepositoptions_set =TermDepositOptionTermSerializer(read_only= True, many=True)
    
    class Meta:
        model = TermDeposit
        fields= ('product_type', 'dcls_strt_day','kor_co_nm','fin_prdt_nm','termdepositoptions_set','fin_prdt_cd', )           
        
#############################        
# 적금 update
class SavingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Savings
        fields='__all__'
        
# 적금 option update
class SavingsOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingsOptions
        fields='__all__'
        read_only_fields =('product',)

        
# 적금 전체 조회     
class SavingsAllSerializer(serializers.ModelSerializer):
    class SavingsOptionTermSerializer(serializers.ModelSerializer):
        class Meta:
            model = SavingsOptions
            fields=('save_trm', 'intr_rate',)
    savingsoptions_set =SavingsOptionTermSerializer(read_only= True, many=True)
    
    class Meta:
        model = Savings
        fields= ('dcls_strt_day','kor_co_nm','fin_prdt_nm','savingsoptions_set')           


######################  
##대출      
class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanProducts
        fields='__all__'
        
# 대출 option update
class LoanOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanOptions
        fields='__all__'
        read_only_fields =('product',)

        
#  대출 전체 조회     
class LoanAllSerializer(serializers.ModelSerializer):
    class LoanOptionDetailSerializer(serializers.ModelSerializer):
        class Meta:
            model = LoanOptions
            fields='__all__'
    loanoptions_set = LoanOptionDetailSerializer(read_only= True, many=True)
    
    class Meta:
        model = LoanProducts
        fields= '__all__'          


######################  
##신용
class CreditLoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditLoanProducts
        fields='__all__'
        
# 신용 option update
class CreditLoanOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditLoanOptions
        fields='__all__'
        read_only_fields =('product',)

        
#  신용 전체 조회     
class CreditLoanAllSerializer(serializers.ModelSerializer):
    class CreditLoanOptionDetailSerializer(serializers.ModelSerializer):
        class Meta:
            model = CreditLoanOptions
            fields='__all__'
    creditloanoptions_set = CreditLoanOptionDetailSerializer(read_only= True, many=True)
    
    class Meta:
        model = CreditLoanProducts
        fields= '__all__'          