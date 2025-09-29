from django.views import View
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
import json

class ApplyView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            title = data.get("title")
            first_name = data.get("first-name")
            last_name = data.get("last-name")
            email = data.get("email")
            phonenumber = data.get("phonenumber")
            
            send_mail(
                  subject=f"Bewerbug von {first_name} {last_name}",
                  message=(
                        f"Name:{title} {first_name} {last_name}\n"
                        f"E-Mail: {email} \n"
                        f"Handy: {phonenumber}\n"                        
                  ),
                  from_email=settings.EMAIL_HOST_USER,
                  recipient_list=[settings.EMAIL_HOST_USER],
            )

            # Confirmation email to USER
            send_mail(
                  subject=f"Start in Krypto - Bestätigung",
                  message=(
                        f"Hallo {first_name}, \n\n"
                        f"wir haben deine Bewerbung bekommen. \n"
                        f"Wir melden uns in Kurze.\n\n"
                        f"Mit freundlichen Grüßen\n"
                        f"Start in Krypto"
                  ),
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
            )

            return JsonResponse({"message": "Message sent successfully!"})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def get(self, request, *args, **kwargs):
        return JsonResponse({"error": "GET method not allowed"}, status=405)