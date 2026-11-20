from django.db import migrations
from decimal import Decimal

def convert_usd_to_inr(apps, schema_editor):
    Product = apps.get_model('store', 'Product')
    Order = apps.get_model('store', 'Order')
    OrderItem = apps.get_model('store', 'OrderItem')
    
    # Scale product prices
    for product in Product.objects.all():
        product.price = product.price * Decimal('83.00')
        product.save()
        
    # Scale order total amounts
    for order in Order.objects.all():
        order.total_amount = order.total_amount * Decimal('83.00')
        order.save()
        
    # Scale order item prices and subtotals
    for item in OrderItem.objects.all():
        item.price = item.price * Decimal('83.00')
        item.subtotal = item.subtotal * Decimal('83.00')
        item.save()

class Migration(migrations.Migration):
    dependencies = [
        ('store', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(convert_usd_to_inr),
    ]
