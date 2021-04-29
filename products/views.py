import my_settings

from django.http     import JsonResponse
from django.views    import View

from products.models import MainCategory, SubCategory

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
