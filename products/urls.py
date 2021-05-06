from django.urls        import path
from products.views     import CategoryListView, ProductCategoryView, HealthGoalView, ProductListView

urlpatterns=[
        path('/categories',CategoryListView.as_view()),
        path('/subcategories', ProductCategoryView.as_view()),
        path('/health-goals', HealthGoalView.as_view()),
        path('/products',ProductListView.as_view())
]