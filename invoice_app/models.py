from django.db import models
from customer_app.models import Customer

class ServiceCatalog(models.Model):
    name = models.CharField(max_length=200)
    provision = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name

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
    
    # snapshot of address at invoice creation
    customer_name = models.CharField(max_length=200)
    customer_address = models.TextField()
    
    # Saved final PDF
    pdf_file = models.FieldFile(updated_at="invoices/", null=True, blank=True)

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

    # Custom service name from frontend
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