from .models import Customer, User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

# NB: dont' forget to use the Ready fucntion in the app.py to make all the function in signals .py ready to be executed

@receiver(post_save, sender=settings.AUTH_USER_MODEL) # for the sendere I could also put "User" but this could create a dipendencly from the store app. INstead in this way I take the User model wherever is defined in the all project.
def create_customer_for_new_user(sender, **kwargs):
    if kwargs['created']:
        Customer.objects.create(user=kwargs['instance'])

