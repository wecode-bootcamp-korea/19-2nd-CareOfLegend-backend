import my_settings

from django.http     import JsonResponse
from django.views    import View

from products.models import MainCategory, SubCategory, HealthGoal

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


