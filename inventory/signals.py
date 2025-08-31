from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Sale, InventoryLog, InventoryItem

@receiver(post_save, sender=Sale)
def handle_sale(sender, instance, created, **kwargs):
    if created:
        item = instance.item
        # decrement item.quantity safely
        original = item.quantity
        new_qty = max(0, original - instance.quantity)
        item.quantity = new_qty
        item.save()
        InventoryLog.objects.create(
            item=item,
            change_amount=-instance.quantity,
            change_type='sale',
            changed_by=instance.sold_by
        )

@receiver(pre_save, sender=InventoryItem)
def log_quantity_change(sender, instance, **kwargs):
    if not instance.pk:
        # new item — nothing to do
        return
    try:
        old = InventoryItem.objects.get(pk=instance.pk)
    except InventoryItem.DoesNotExist:
        return
    if old.quantity != instance.quantity:
        diff = instance.quantity - old.quantity
        t = 'restock' if diff > 0 else 'sale'
        InventoryLog.objects.create(
            item=instance,
            change_amount=diff,
            change_type=t,
            changed_by=instance.owner
        )
