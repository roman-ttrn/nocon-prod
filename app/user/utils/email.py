import secrets
import string
from django.core.mail import send_mail

# Генерация криптографически стойкого токена
def generate_secure_token(length=12):
    characters = string.ascii_letters + string.digits  # A-Z, a-z, 0-9
    return ''.join(secrets.choice(characters) for _ in range(length))


# Отправка кода на email
def send_verification_code(email, code):
    subject = 'Код подтверждения'
    message = f'Ваш код подтверждения: {code}'
    from_email = 'noreply@example.com'

    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=[email],
        fail_silently=False,
    )
