import json
import my_settings

from users.utils      import login_decorator

from django.http      import JsonResponse
from django.views     import View
from django.db        import transaction, IntegrityError

from products.models  import Product, ProductImage
from orders.models    import Order, Cart, OrderStatus, ShipmentInformation
from users.models     import User

SHIPMENT_COST       = 8
FREE_SHIPPING_PRICE = 20
STATUS_CART         = 1
STATUS_COMPLETE     = 0

class BasketView(View):
    @login_decorator
    def get(self,request):
        users = request.user.user_code
        order = Order.objects.filter(user_id = users, order_status = STATUS_CART).first()

        result = [{
               'product_id'        : cart_product.product.id,
                'product_name'     : cart_product.product.name,
                'product_price'    : cart_product.product.price,
                'product_image'    : cart_product.product.productimage_set.get(thumbnail_status = 1).image_url if cart_product.product.productimage_set.get(thumbnail_status = 1) else None,
                'product_quantity' : cart_product.quantity,
                'total_price'      : cart_product.order.total_price,
                'shipment_price'   : cart_product.order.shipment_cost
                } for cart_product in Cart.objects.filter(order_id = order)]

        return JsonResponse({'result':result}, status = 200)

    @login_decorator
    def post(self,request):
        try:
            data                = json.loads(request.body)
            product_id          = data['product_id']
            product_quantity    = data.get('product_quantity',0)
            user_id             = request.user.user_code

            if not (product_id and product_quantity):
                return JsonResponse({'MESSAGE':'DATA NOT ENTERED'}, status = 400)
            
            product = Product.objects.get(id = product_id)
            
            order, order_created = Order.objects.get_or_create(
                user_id         = user_id,
                order_status_id = STATUS_CART,
                defaults        = {'total_price' :product.price * int(product_quantity)})

            cart, cart_created = Cart.objects.get_or_create(
                order_id   = order.id,
                product_id = product_id,
                defaults   = {'quantity' : product_quantity, 'price' : product.price * int(product_quantity)})

            if not order_created and cart_created:
                order.total_price += cart.price
    
            order.shipment_cost = 0 if order.total_price >= FREE_SHIPPING_PRICE else SHIPMENT_COST
                
            order.save()
            return JsonResponse({'MESSAGE':'SUCCESS'},status = 200)
        except Product.DoesNotExist:
            return JsonResponse({'MESSAGE':'INVALID PRODUCT'},status = 400)
        except KeyError:
            return JsonResponse({'MESSAGE':'KEY ERROR'}, status = 400)
        except json.JSONDecodeError:
            return JsonResponse({'MESSAGE':'JSON DECODE ERROR'}, status = 400)
        except IntegrityError:
            return JsonResponse({'MESSAGE':'PRODUCT DOES NOT EXIST'},status = 400)

class BasketDetailView(View):
    @login_decorator
    def delete(self, request, product_id):
        try:
            user    = request.user.user_code
            order   = Order.objects.get(user_id = user, order_status_id = STATUS_CART)
            product = Product.objects.get(id = product_id)

            if not order:
                return JsonResponse({'MESSAGE':'DOES NOT ORDER'},status = 400)

            delete_product = Cart.objects.get(order_id = order.id, product_id = product.id)
            delete_product.delete()

            order.total_price -= delete_product.price
    
            order.shipment_cost = 0 if order.total_price >= FREE_SHIPPING_PRICE else SHIPMENT_COST
            order.save()

            if order.cart_set.count() <= 0:
                order.delete()

            return JsonResponse({'MESSAGE':'SUCCESS'},status=200)

        except json.JSONDecodeError:
            return JsonResponse({'MESSAGE':'JSON DECODE ERROR'}, status=400) 
        except Product.DoesNotExist:
            return JsonResponse({'MESSAGE':'INVALID PRODUCT'}, status = 400)