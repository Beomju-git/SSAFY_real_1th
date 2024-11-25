from django.db import models

class StandardizedTermDeposit(models.Model):
    fin_prdt_cd = models.TextField(unique=True)
    fin_prdt_nm = models.TextField()
    min_join_amount = models.FloatField(null=True)
    max_join_amount = models.FloatField(null=True)
    join_period = models.TextField(default="정보없음")
    interest_rate = models.FloatField(null=True)
    join_member = models.TextField(null=True, blank=True, default="")
    join_way = models.TextField(null=True, blank=True, default="")
    spcl_cnd = models.TextField(null=True, blank=True, default="")

    def __str__(self):
        return f"{self.fin_prdt_nm} ({self.fin_prdt_cd})"