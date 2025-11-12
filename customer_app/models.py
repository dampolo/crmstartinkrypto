from django.db import models

class Customer(models.Model):
    TITLE_CHOICES = [
        ('Herr', 'Herr'),
        ('Frau', 'Frau'),
        ('Divers', 'Divers'),
    ]

    photo = models.ImageField(upload_to='customers/photos/', blank=True, null=True)
    customer_number = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=20, choices=TITLE_CHOICES, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    street = models.CharField(max_length=200)
    number = models.CharField(max_length=10)
    post_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50, blank=True)
    portfolio = models.BooleanField(default=False)
    subscription = models.BooleanField(default=False)
    invoices = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.customer_number})"
    
class CustomerComment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment for {self.customer} on {self.created_at:%Y-%m-%d}"