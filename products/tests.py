import json
import unittest

from django.test        import TestCase, Client
from products.models    import MainCategory,SubCategory,Product, HealthGoal


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


class ProductCategoryTest(TestCase):

    def setUp(self):
        client = Client()

        MainCategory.objects.create(name = 'Vitamins')
        MainCategory.objects.create(name = 'Powders')
        MainCategory.objects.create(name = 'Extras')

        SubCategory.objects.create(
                name             = 'Letter Vitamins',
                description      = 'Vitamins is.',
                main_category_id = 4
                )

        SubCategory.objects.create(
                name             = 'Collagen',
                description      = 'Collagen is.',
                main_category_id = 5
                )

        SubCategory.objects.create(
                name             = 'Quick Sticks',
                description      = 'Quick Sticks is.',
                main_category_id = 6
                )

    def tearDown(self):
        MainCategory.objects.all().delete()
        SubCategory.objects.all().delete()

    def test_productcategory_get_success(self):
        client = Client()
        response = client.get('/products/subcategories')

        self.assertEqual(response.json(),{
                "result": [
                    {
                        "name": "Vitamins",
                        "subcategories": [
                            {
                                "subcategory_id": 4,
                                "description": "Vitamins is.",
                                "name": "Letter Vitamins"
                            }
                        ]
                    },
                    {
                        "name": "Powders",
                        "subcategories": [
                            {
                                "subcategory_id": 5,
                                "description": "Collagen is.",
                                "name": "Collagen"
                            }
                        ]
                    },
                    {
                        "name": "Extras",
                        "subcategories": [
                            {
                                "subcategory_id": 6,
                                "description": "Quick Sticks is.",
                                "name": "Quick Sticks"
                            }
                        ]
                    }
                ]
            }
        )
        self.assertEqual(response.status_code, 200)


class HealthGoalTest(TestCase):

    def setUp(self):
        client = Client()
        HealthGoal.objects.create(
                name           = 'name 1',
                icon_url       = 'icon_url 1'
                )

        HealthGoal.objects.create(
                name           = 'name 2',
                icon_url       = 'icon_url 2'
                )

    def tearDown(self):
        HealthGoal.objects.all().delete()

    def test_healthgoal_get_success(self):
        client = Client()
        response = client.get('/products/health-goals')

        self.assertEqual(response.json(),{
                "result": [
                    {
                        "health_goal_id": 1,
                        "name": "name 1",
                        "icon_url": "icon_url 1"
                    },
                    {
                        "health_goal_id": 2,
                        "name": "name 2",
                        "icon_url": "icon_url 2"
                    }
                ]
            }
        )
        self.assertEqual(response.status_code, 200)


