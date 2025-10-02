from django.views import View
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage
import json

@method_decorator(csrf_exempt, name="dispatch")
class ApplyView(View):
    def post(self, request, *args, **kwargs):
        try:
            title = request.POST.get("title")
            first_name = request.POST.get("first-name")
            last_name = request.POST.get("last-name")
            email = request.POST.get("email")
            phonenumber = request.POST.get("phonenumber")
            file = request.FILES.get("file")
            
            # Build email
            body = (
                f"Name: {title} {first_name} {last_name}\n"
                f"E-Mail: {email}\n"
                f"Handy: {phonenumber}\n"
            )
            # E-mail to me
            email_message = EmailMessage(
                subject=f"Bewerbung von {first_name} {last_name}",
                body=body,
                from_email=f"Start in Krypto <{settings.DEFAULT_FROM_EMAIL}>",  # always your verified sender
                to=[settings.DEFAULT_FROM_EMAIL],
                reply_to=[email],
            )
            
            if file:
                email_message.attach(file.name, file.read(), file.content_type)

            email_message.send()

            # Confirmation email to USER
            send_mail(
                  subject=f"Bestätigung von Start in Krypto",
                  message=(
                        f"Hallo {first_name}, \n\n"
                        f"wir haben deine Bewerbung bekommen. \n"
                        f"Wir melden uns in Kurze.\n\n"
                        f"Mit freundlichen Grüßen\n"
                        f"Start in Krypto"
                  ),
                from_email="Elisabeth <elisabeth@startinkrypto.de>",
                recipient_list=[email],
            )

            return JsonResponse({"message": "Message sent successfully!"})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def get(self, request, *args, **kwargs):
        return JsonResponse({"error": "GET method not allowed"}, status=405)