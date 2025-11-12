from rest_framework.viewsets import ModelViewSet
from .serializer import CustomerSerializer
from customer_app.models import Customer

class CustomerView(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer