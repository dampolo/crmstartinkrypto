from django.db import models
from customer_app.models import Customer

class ServiceCatalog(models.Model):
    name = models.CharField(max_length=200)
    provision = models.FloatField(null=True, blank=True)
    amount = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name

class Invoice(models.Model):
    invoiceNumber = models.CharField(max_length=50, unique=True)
    customer = models.ForeignKey(Customer, related_name='invoices', on_delete=models.PROTECT)
    customerAddress = models.TextField() # snapshot of address at invoice creation
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Invoice {self.invoiceNumber}"
    
class InvoiceService(models.Model):
    invoice = models.ForeignKey(
        Invoice,
        related_name="services",
        on_delete=models.CASCADE
    )

    service_catalog = models.ForeignKey(
        ServiceCatalog,
        null=True,
        blank=True,
        related_name="invoice_items",
        on_delete=models.PROTECT
    )

    provision = models.FloatField()
    amount = models.FloatField()
    investitionsAmount = models.FloatField()

    def __str__(self):
        return self.custom_service_name or self.service_catalog.name