from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.timezone import now
from datetime import timedelta
from .models import Product, User
from django.core.mail import send_mail
from django.contrib.auth.models import User

EXPIRY_THRESHOLD_DAYS = 30

def send_expiry_alert(drug):
    subject = f"Expiry Warning: {drug.name}"
    message = (
        f"The drug '{drug.name}' is set to expire on {drug.expiry_date}. "
        f"Please take the necessary actions. Remaining days: "
        f"{(drug.expiry_date - now().date()).days}"
    )
    recipients = [user.email for user in User.objects.filter(is_staff=True)]
    send_mail(subject, message, 'curanetapp@gmail.com', recipients)

@receiver(pre_save, sender=Product)
def check_expiry_on_update(sender, instance, **kwargs):
    if instance.pk:
        existing_drug = Product.objects.get(pk=instance.pk)
        if instance.expiry_date != existing_drug.expiry_date:
            days_remaining = (instance.expiry_date - now().date()).days
            if days_remaining <= EXPIRY_THRESHOLD_DAYS:
                send_expiry_alert(instance)

@receiver(post_save, sender=Product)
def check_expiry_on_create(sender, instance, created, **kwargs):
    if created:
        days_remaining = (instance.expiry_date - now().date()).days
        if days_remaining <= EXPIRY_THRESHOLD_DAYS:
            send_expiry_alert(instance)
