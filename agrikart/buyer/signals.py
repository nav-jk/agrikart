from django.db.models.signals import post_save
from django.dispatch import receiver
from buyer.models import Order
from logistics.utils import assign_order_to_courier

@receiver(post_save, sender=Order)
def assign_courier_on_order(sender, instance, created, **kwargs):
    if created:
        assign_order_to_courier(instance)
