from django.dispatch import receiver
from django.db.models.signals import post_save
from store.models import Customer
from django.contrib.auth.models import User


def create_customer(sender, created, instance, **kwargs):
    if created:
        Customer.objects.create(user=instance)


post_save.connect(create_customer, sender=User)


def update_customer(sender, created, instance, **kwargs):

    if created == False:
        instance.customer.save()


post_save.connect(update_customer, sender=User)
