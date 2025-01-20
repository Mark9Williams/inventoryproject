from __future__ import absolute_import, unicode_literals
from celery import shared_task, Celery
from .models import Product
from django.utils.timezone import now
from datetime import timedelta
from celery.schedules import crontab
from django.core.mail import send_mail



def send_expiry_alert(drug):
    subject = f"Expiry Alert: {drug.name}"
    message = (
        f"The drug '{drug.name}' in inventory is nearing expiry. "
        f"Expiry Date: {drug.expiry_date}. Please take necessary action."
    )
    recipient_list = ['mawejjemarkwilliam@gmail.com']
    
    send_mail(
        subject,
        message,
        'curanetapp@gmail.com',
        recipient_list,
        fail_silently=False,
    )

@shared_task
def check_expiry_dates():
    drugs = Product.objects.all()
    for drug in drugs:
        days_remaining = (drug.expiry_date - now().date()).days
        if days_remaining <= 30:
            send_expiry_alert(drug)

app = Celery('inventoryproject')

app.conf.beat_schedule = {
    'check-expiry-every-2-minutes': {
        'task': 'dashboard.tasks.check_expiry_dates',
        'schedule': crontab(minute='*/2'),
    },
}