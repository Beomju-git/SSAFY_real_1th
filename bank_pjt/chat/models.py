from django.db import models

class ConversationHistory(models.Model):
    session_id = models.CharField(max_length=100)
    message = models.TextField()
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    context_data = models.JSONField(default=dict)

    class Meta:
        ordering = ['-timestamp']

class MarketData(models.Model):
    product_type = models.CharField(max_length=50)
    data_type = models.CharField(max_length=50)
    value = models.JSONField()
    updated_at = models.DateTimeField(auto_now=True)

class StandardizedTermDeposit(models.Model):
    fin_prdt_cd = models.CharField(max_length=100, primary_key=True)
    fin_prdt_nm = models.CharField(max_length=100)
    min_join_amount = models.FloatField(null=True)
    max_join_amount = models.FloatField(null=True)
    join_period = models.CharField(max_length=100)
    interest_rate = models.FloatField(null=True)
    join_member = models.TextField()
    join_way = models.TextField()
    spcl_cnd = models.TextField()