from django.db import models

class Cart(models.Model):
    quantity = models.IntegerField()
    product  = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    order    = models.ForeignKey('Order', on_delete=models.CASCADE)

    class Meta:
        db_table = 'carts'

class Order(models.Model):
    shipment_cost        = models.DecimalField(max_digits=4, decimal_places=2)
    total_price          = models.DecimalField(max_digits=10, decimal_places=2)
    user                 = models.ForeignKey('users.User', on_delete=models.CASCADE)
    order_status         = models.ForeignKey('OrderStatus', on_delete=models.PROTECT)
    shipment_information = models.OneToOneField('ShipmentInformation', on_delete=models.CASCADE)
    product              = models.ManyToManyField('products.Product', through='Cart')

    class Meta:
        db_table = 'orders'

class OrderStatus(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'order_status'

class ShipmentInformation(models.Model):
    address      = models.CharField(max_length=1000)
    phone_number = models.CharField(max_length=45)
    email        = models.CharField(max_length=200)

    class Meta:
        db_table = 'shipment_informations'
