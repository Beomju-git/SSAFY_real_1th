from django.db import models

# Create your models here.
class Exchange(models.Model):
    cur_unit = models.TextField() # 단위
    country = models.TextField() #국가/ 통화명
    rate = models.FloatField() # 서울외국환중개 매매기준율
    date = models.DateField() # 업데이트 된 날짜
