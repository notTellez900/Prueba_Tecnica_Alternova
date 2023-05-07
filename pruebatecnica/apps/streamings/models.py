from django.db import models

from apps.users.models import Customer

# Create your models here.
class Streamings(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    gender = models.CharField(max_length=200, null=True, blank=True)
    stream_type = models.CharField(max_length=200, null=True, blank=True)
    num_visualizations = models.IntegerField(null=True, blank=True, default=0)
    num_ratings = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    rating = models.DecimalField(max_digits=7, decimal_places=2,null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.name}'
    
class CustomerStreaming(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    streaming = models.ForeignKey(Streamings, on_delete=models.CASCADE)
    was_seen= models.BooleanField(default=False)
    is_rated = models.BooleanField(default=False)


    def __str__(self) -> str:
        return self.user.user.first_name