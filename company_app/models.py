from django.db import models

class Company(models.Model):
    logo = models.ImageField(upload_to='uploads/', blank=True, null=True)
    name = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    number = models.CharField(max_length=20)
    postcode = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    owner_name = models.CharField(max_length=255)
    tax_number = models.CharField(max_length=50)
    founding = models.PositiveIntegerField(default="")
    email = models.EmailField()
    bank = models.CharField(max_length=100)
    bank_account = models.CharField(max_length=34)
    swift_code = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.name} + ({self.owner_name} + {self.email})"