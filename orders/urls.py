from django.urls        import path
from orders.views       import BasketView, BasketDetailView

urlpatterns=[
        path('/carts',BasketView.as_view()),
        path('/carts-detail/<int:product_id>',BasketDetailView.as_view()),
]
