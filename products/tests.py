import json

from django.test        import TestCase, Client
from products.models    import MainCategory,SubCategory,Product

client = Client()

class NavcategoryList(TestCase):
    def setUp(self):

        MainCategory.objects.create(name = "TEST1")
        MainCategory.objects.create(name = "TEST2")
        MainCategory.objects.create(name = "TEST3")

        SubCategory.objects.create(
                                name             = "Letter Vitamins1",
                                description      = 'blablabla',
                                main_category_id = 1)

        SubCategory.objects.create(
                                name             = "Letter Vitamins2",
                                description      = 'blablabla',
                               main_category_id = 2)

        SubCategory.objects.create(
                                name             = "Letter Vitamins3",
                                description      = 'blablabla',
                                main_category_id = 3)

    def tearDown(self):
        MainCategory.objects.all().delete()
        SubCategory.objects.all().delete()

    def test_category_get_sucess(self):
        response = client.get('/products/categories')

        self.assertEqual(response.json(),{
                "result": [
                    {
                        "category_id"   : 1,
                        "category_name" : "TEST1",
                        "subcategories" : [
                            {
                                "id": 1,
                                "subcategory_name" : "Letter Vitamins1"
                            }
                            ]
                    },
                    {
                        "category_id"   : 2,
                        "category_name" : "TEST2",
                        "subcategories" : [
                            {
                                "id": 2,
                                "subcategory_name" : "Letter Vitamins2"
                            },
                        ]
                    },
                    {
                        "category_id"   : 3,
                        "category_name" : "TEST3",
                        "subcategories" : [
                            {
                                "id" : 3,
                                "subcategory_name" : "Letter Vitamins3"
                            }
                        ]
                    }
                ]
            }
        )

        self.assertEqual(response.status_code, 200) 
