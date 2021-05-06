import my_settings

from django.http       import JsonResponse
from django.views      import View
from django.db.models  import Q

from products.models   import (MainCategory, SubCategory, Product,
                               ProductImage, HealthGoal, ProductHealthGoal,
                               Symbol, ProductSymbol)

class CategoryListView(View):
    def get(self,request):
        categories = MainCategory.objects.all()
        
        result = [{
            'category_id'      : category.id,
            'category_name'    : category.name,
            'subcategories'    : [{
                'id'               : subcategory.id,
                'subcategory_name' : subcategory.name } for subcategory in category.subcategory_set.all()]}
                for category in categories ]
                 

        return JsonResponse({'result':result}, status=200) 

class ProductCategoryView(View):
    def get(self, request):
        categories = MainCategory.objects.all()

        result = [
            {
                'name'          : category.name, 
                'subcategories' : [{
                    'subcategory_id' : subcategory.id,
                    'name'           : subcategory.name,
                    'description'    : subcategory.description
                } for subcategory in category.subcategory_set.all()]
            } for category in categories]

        return JsonResponse({'result' : result}, status = 200)


class HealthGoalView(View):
    def get(self, request):
        health_goals = HealthGoal.objects.all()

        result = [
            {
                'health_goal_id' : health_goal.id,
                'name'           : health_goal.name,
                'icon_url'       : health_goal.icon_url
                } for health_goal in health_goals]

        return JsonResponse({'result' : result}, status = 200)

class ProductListView(View):
    def get(self,request):
        sub_categories  = request.GET.get('sub_category',None)
        health_goals    = request.GET.get('health_goal',None)
        is_new          = request.GET.get('is_new',None)
        
        if health_goals:
            health_goals_products = ProductHealthGoal.objects.filter(health_goal_id = health_goals)
            result=[{
                    'product_id'             : product.product.id,
                    'product_health_goal_id' : product.health_goal_id,
                    'product_name'           : product.product.name,
                    'product_sub_name'       : product.product.sub_name,
                    'product_price'          : product.product.price,
                    'product_is_new'         : product.product.is_new,
                    'product_description'    : product.product.description.split(','),
                    'product_image'          : product.product.productimage_set.filter(thumbnail_status=1).first().image_url if product.product.productimage_set.filter(thumbnail_status=1).first() else None
                    } for product in health_goals_products]

            return JsonResponse({'result' : result}, status=200)
        q = Q()

        if not sub_categories and not health_goals and not is_new:
            products = Product.objects.all()
                        
        if sub_categories:
            q &= Q(sub_category = sub_categories)
                        
        if is_new:
            q &= Q(is_new = is_new)
                        
        products = Product.objects.filter(q)

        result=[{
            'product_id'              : product.id,
            'product_name'            : product.name,
            'product_sub_category_id' : product.sub_category_id,
            'product_sub_name'        : product.sub_name,
            'product_price'           : float(product.price),
            'product_is_new'          : product.is_new,
            'product_description'     : product.description.split(','),
            'product_tumbnail_image'  : product.productimage_set.get(thumbnail_status = True).image_url if product.productimage_set.filter(thumbnail_status=True).first() else None
                    } for product in products]
        
        return JsonResponse({'result' : result}, status = 200)
