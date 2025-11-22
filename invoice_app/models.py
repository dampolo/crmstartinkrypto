from django.db import models
from customer_app.models import Customer
from auth_app.models import User


class ServiceCatalog(models.Model):
    class PriceType(models.TextChoices):
        FIXED = 'fixed', ('Fixed Amount (€)')
        PERCENT = 'percent', ('Percentage (%)')

    name = models.CharField(max_length=200)

    price_type = models.CharField(
        max_length=20,
        choices=PriceType.choices,
        default=PriceType.FIXED
    )

    # Fixed amount (example: 700.00 €)
    amount_fixed = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    # Percent amount (example: 0.05 = 5%)
    amount_percent = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        null=True,
        blank=True,
        help_text="Percentage as decimal (e.g. 0.05 = 5%)"
    )

    def __str__(self):
        return f"{self.name} ({self.price_type})"
    

class ServiceCatalogForSpecificInvoice(models.Model):
    name = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.name} {self.amount}'

class Invoice(models.Model):
    class InvoiceType(models.TextChoices):
        INVOICE = 'invoice', ('Invoice')
        CREDIT_NOTE = 'credit_note', ('Credit Note')

    invoice_number = models.CharField(max_length=50, unique=True)

    invoice_type = models.CharField(
        max_length=20,
        choices=InvoiceType.choices,
        default=InvoiceType.INVOICE
    )

    customer = models.ForeignKey(
        Customer, 
        related_name='invoices', 
        on_delete=models.PROTECT
    )

    user = models.ForeignKey(
        User, 
        related_name='invoices', 
        on_delete=models.PROTECT
    )
    
    # snapshot of address at invoice creation
    customer_name = models.CharField(max_length=200)
    customer_address = models.TextField()
    
    # Saved final PDF
    # pdf_file = models.FieldFile(updated_at="invoices/", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Invoice {self.invoice_number}"
    
class InvoiceService(models.Model):
    invoice = models.ForeignKey(
        Invoice,
        related_name="services",
        on_delete=models.PROTECT
    )

    service_catalog = models.ForeignKey(
        ServiceCatalogForSpecificInvoice,
        null=True,
        blank=True,
        related_name="invoice_items",
        on_delete=models.PROTECT
    )

     # Custom service name from frontend (special unique service)
    custom_service_name = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )

    provision = models.DecimalField(decimal_places=2)
    amount = models.DecimalField(decimal_places=2)
    investitions_amount = models.DecimalField(decimal_places=2)

    def __str__(self):
        return (
            self.custom_service_name or 
            (self.service_catalog.name if self.service_catalog else "Service")
        )