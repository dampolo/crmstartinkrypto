from django.urls import path
from apply_app.api.views import ApplyView

urlpatterns = [
    path("apply/", ApplyView.as_view(), name="apply"),
]