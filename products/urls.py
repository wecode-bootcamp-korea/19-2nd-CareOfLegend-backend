from django.urls        import path
from products.views     import CategoryListView

urlpatterns=[
        path('/categories',CategoryListView.as_view()),
        ]
