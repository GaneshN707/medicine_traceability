from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class firm_info(models.Model):
    user = models.OneToOneField(User, null=True, on_delete = models.CASCADE)
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=20)
    user_type = models.CharField(max_length=20)
    
    def __str__(self):
        return str(self.user)
    
class medicine(models.Model):
    Medicine_id = models.CharField(max_length=100)
    Medicine_Name = models.CharField(max_length=100)
    Batch_No = models.CharField(max_length=100)
    Medicine_Used = models.CharField(max_length=100)
    Manifacture_Date = models.DateField(max_length=100)
    Expiring_Date = models.DateField(max_length=100)
    Maximum_Retail_prise = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=100)
    qr_code_image = models.ImageField(upload_to='qrcode',blank=True, null=True)
    
    def __str__(self):
        return str(self.Medicine_id)