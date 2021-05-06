import json
import unittest

from django.test        import TestCase, Client

from users.models       import Question, Option
from products.models    import (MainCategory, SubCategory,  Product,
                               HealthGoal,    ProductImage, ProductHealthGoal)


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


class ProductListTEST(TestCase):
    def setUp(self):

        MainCategory.objects.create(
                                    id   = 1,
                                    name = "TEST1"
                                    )

        MainCategory.objects.create(
                                    id   = 2,
                                    name = "TEST1"
                                    )
        
        MainCategory.objects.create(
                                    id   = 3,
                                    name = "TEST1"
                                    )

        SubCategory.objects.create(
                                id               = 1,
                                name             = "Letter Vitamins1",
                                description      = "blablabla",
                                main_category_id = 1
                                )

        SubCategory.objects.create(
                                id               = 2,
                                name             = "Letter Vitamins2",
                                description      = "blablabla",
                                main_category_id = 2
                                )

        SubCategory.objects.create(
                                id               = 3,
                                name             = "Letter Vitamins3",
                                description      = "blablabla",
                                main_category_id = 3
                                )
        
        Product.objects.create(
                                id               = 1,
                                name             = "B-Complex",
                                sub_name         = "The Busy B\"s",
                                price            = 13.00,
                                description      = "Organic pea pumpkin seed protein and hemp proteins,18g of protein per serving,15-serving tub,Made with creamy MCT oil and organic cocoa powder",
                                is_new           = 1,
                                main_category_id = 1,
                                sub_category_id  = 1
                                )

        Product.objects.create(
                                id               = 2,
                                name             = "Iron",
                                sub_name         = "The Blood Booster",
                                price            = 5.00,
                                description      = "Organic pea pumpkin seed protein and hemp proteins,18g of protein per serving,15-serving tub,Made with creamy MCT oil and organic cocoa powder",
                                is_new           = 0,
                                main_category_id = 1,
                                sub_category_id  = 2
                                )

        Product.objects.create(
                                id               = 3,
                                name             = "Shatavari",
                                sub_name         = "The Rejuvenating Root",
                                price            = 9.00,
                                description      = "Organic pea pumpkin seed protein and hemp proteins,18g of protein per serving,15-serving tub,Made with creamy MCT oil and organic cocoa powder",
                                is_new           = 1,
                                main_category_id = 1,
                                sub_category_id  = 3
                                )       
        
        Product.objects.create(
                                id               = 4,
                                name             = "Collagen Matcha",
                                sub_name         = "The Skin Hero",
                                price            = 32.00,
                                description      = "Organic pea pumpkin seed protein and hemp proteins,18g of protein per serving,15-serving tub,Made with creamy MCT oil and organic cocoa powder",
                                is_new           = 0,
                                main_category_id = 2,
                                sub_category_id  = 1
                                )

        Product.objects.create(
                                id               = 5,
                                name             = "Plant Protein Vanilla",
                                sub_name         = "Plant Power",
                                price            = 28.00,
                                description      =  "Organic pea pumpkin seed protein and hemp proteins,18g of protein per serving,15-serving tub,Made with creamy MCT oil and organic cocoa powder",
                                is_new           = 1,
                                main_category_id = 2,
                                sub_category_id  = 2
                                )

        Product.objects.create(
                                id               = 6,
                                name             = "Superberry",
                                sub_name         = "The Antioxidant Ace",
                                price            = 26.00,
                                description      = "Organic pea pumpkin seed protein and hemp proteins,18g of protein per serving,15-serving tub,Made with creamy MCT oil and organic cocoa powder",
                                is_new           = 1,
                                main_category_id = 2,
                                sub_category_id  = 3
                                )
        
        Product.objects.create(
                                id               = 7,
                                name             = "Dream Team",
                                sub_name         = "On-the-go sleep support*",
                                price            = 7.00,
                                description      = "Organic pea pumpkin seed protein and hemp proteins,18g of protein per serving,15-serving tub,Made with creamy MCT oil and organic cocoa powder",
                                is_new           = 0,
                                main_category_id = 3,
                                sub_category_id  = 1
                                )

        ProductImage.objects.create(
                                id               = 1,
                                image_url        = "https://media2.giphy.com/media/ioRCKwI9ox0Qg/200w.webp?cid=ecf05e47ha20pqgo4dri6cv9xfck439oi6wyofx64iyd4ovv&rid=200w.webp&ct=g",
                                thumbnail_status = 1,
                                product_id       = 1
                                )
        
        ProductImage.objects.create(               
                                id               = 2,
                                image_url        = "https://media2.giphy.com/media/ioRCKwI9ox0Qg/200w.webp?cid=ecf05e47ha20pqgo4dri6cv9xfck439oi6wyofx64iyd4ovv&rid=200w.webp&ct=g",
                                thumbnail_status = 1,
                                product_id       = 2
                                )
        
        ProductImage.objects.create(
                                id               = 3,
                                image_url        = "https://media2.giphy.com/media/ioRCKwI9ox0Qg/200w.webp?cid=ecf05e47ha20pqgo4dri6cv9xfck439oi6wyofx64iyd4ovv&rid=200w.webp&ct=g",
                                thumbnail_status = 1,
                                product_id       = 3
                                )
        
        ProductImage.objects.create(
                                id               = 4,
                                image_url        = "https://media2.giphy.com/media/ioRCKwI9ox0Qg/200w.webp?cid=ecf05e47ha20pqgo4dri6cv9xfck439oi6wyofx64iyd4ovv&rid=200w.webp&ct=g",
                                thumbnail_status = 1,
                                product_id       = 4
                                )
        
        ProductImage.objects.create(
                                id               = 5,
                                image_url        = "https://media2.giphy.com/media/ioRCKwI9ox0Qg/200w.webp?cid=ecf05e47ha20pqgo4dri6cv9xfck439oi6wyofx64iyd4ovv&rid=200w.webp&ct=g",
                                thumbnail_status = 1,
                                product_id       = 5
                                )

        ProductImage.objects.create(
                                id               = 6,
                                image_url        = "https://media2.giphy.com/media/ioRCKwI9ox0Qg/200w.webp?cid=ecf05e47ha20pqgo4dri6cv9xfck439oi6wyofx64iyd4ovv&rid=200w.webp&ct=g",
                                thumbnail_status = 1,
                                product_id       = 6
                                )

        ProductImage.objects.create(
                                id               = 7,
                                image_url        = "https://media2.giphy.com/media/ioRCKwI9ox0Qg/200w.webp?cid=ecf05e47ha20pqgo4dri6cv9xfck439oi6wyofx64iyd4ovv&rid=200w.webp&ct=g",
                                thumbnail_status = 1,
                                product_id       = 7
                                )

        Question.objects.create(
                                id    = 1,
                                query = "When it comes to vitamins and supplements, you are:"
                                )

        Question.objects.create(
                                id    = 2,
                                query = "Have you taken vitamins in the past? Vitamins, fish oil or similar."
                                )
        Question.objects.create(
                                id    = 3,
                                query = "Have you taken powders in the past? Protein, collagen, or anything mixed into a drink."
                                )

        Option.objects.create(  
                                id          = 1,
                                question_id = 1,
                                name        = "test1",
                                product_id  = 1,
                                image_url   = "https://image.flaticon.com/icons/png/128/927/927567.png"
                            )
        
        Option.objects.create(  
                                id          = 2,
                                question_id = 2,
                                name        = "test2",
                                product_id  = 2,
                                image_url   = "https://image.flaticon.com/icons/png/128/927/927567.png"
                            )

        Option.objects.create(  
                                id          = 3,
                                question_id = 3,
                                name        = "test3",
                                product_id  = 3,
                                image_url   = "https://image.flaticon.com/icons/png/128/927/927567.png"
                            )                    

        HealthGoal.objects.create(
                                id = 1,
                                name = "Bones",
                                icon_url = "https://www.flaticon.com/kr/premium-icon/icons/svg/2655/2655093.svg",
                                option_id = 1,
                            )

        HealthGoal.objects.create(
                                id = 2,
                                name = "Bones",
                                icon_url = "https://www.flaticon.com/kr/premium-icon/icons/svg/2655/2655093.svg",
                                option_id = 1,
                            )

        HealthGoal.objects.create(
                                id = 3,
                                name = "Bones",
                                icon_url = "https://www.flaticon.com/kr/premium-icon/icons/svg/2655/2655093.svg",
                                option_id = 1,
                            )

        ProductHealthGoal.objects.create(
                                id             = 1,
                                product_id     = 1,
                                health_goal_id = 3
                            )

        ProductHealthGoal.objects.create(
                                id             = 2,
                                product_id     = 2,
                                health_goal_id = 1
                            )

        ProductHealthGoal.objects.create(
                                id             = 3,
                                product_id     = 3,
                                health_goal_id = 2
                            )

    def tearDown(self):
        MainCategory.objects.all().delete()
        SubCategory.objects.all().delete()
        Product.objects.all().delete()
        ProductImage.objects.all().delete()
        ProductHealthGoal.objects.all().delete()
        Question.objects.all().delete()
        Option.objects.all().delete()
        ProductHealthGoal.objects.all().delete()

    def test_sub_category_productlist_success(self):
        response = client.get("/products/products?sub_category=2")

        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json(),{
                    "result" : [
                        {   "product_id"              : 2,
                            "product_name"            : "Iron",
                            "product_sub_category_id" : 2,
                            "product_sub_name"        : "The Blood Booster",
                            "product_price"           : 5.00,        
                            "product_is_new"          : False,
                            "product_description"     : [
                                "Organic pea pumpkin seed protein and hemp proteins",
                                "18g of protein per serving",
                                "15-serving tub",
                                "Made with creamy MCT oil and organic cocoa powder"
                            ],
                            "product_tumbnail_image"  : "https://media2.giphy.com/media/ioRCKwI9ox0Qg/200w.webp?cid=ecf05e47ha20pqgo4dri6cv9xfck439oi6wyofx64iyd4ovv&rid=200w.webp&ct=g"
                        },
                        {
                            "product_id"              : 5,
                            "product_name"            : "Plant Protein Vanilla",
                            "product_sub_category_id" : 2,
                            "product_sub_name"        : "Plant Power",
                            "product_price"           : 28.00,
                            "product_is_new"          : True,
                            "product_description"     : [
                                "Organic pea pumpkin seed protein and hemp proteins",
                                "18g of protein per serving",
                                "15-serving tub",
                                "Made with creamy MCT oil and organic cocoa powder"
                            ],
                            "product_tumbnail_image"  : "https://media2.giphy.com/media/ioRCKwI9ox0Qg/200w.webp?cid=ecf05e47ha20pqgo4dri6cv9xfck439oi6wyofx64iyd4ovv&rid=200w.webp&ct=g"
                        }
                    ]
                }
            )

    def test_health_goal_productlist_success(self):
        response = client.get("/products/products?health_goal=1")

        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json(),{
                    "result" : [
                        {   "product_id"              : 2,
                            "product_health_goal_id"  : 1,
                            "product_name"            : "Iron",
                            "product_sub_name"        : "The Blood Booster",
                            "product_price"           : '5.00',
                            "product_is_new"          : False,
                            "product_description"     : [
                                "Organic pea pumpkin seed protein and hemp proteins",
                                "18g of protein per serving",
                                "15-serving tub",
                                "Made with creamy MCT oil and organic cocoa powder"
                            ],
                            "product_image"  : "https://media2.giphy.com/media/ioRCKwI9ox0Qg/200w.webp?cid=ecf05e47ha20pqgo4dri6cv9xfck439oi6wyofx64iyd4ovv&rid=200w.webp&ct=g"
                        },
                    ]
                }
            )

    def test_all_products_success(self):
        response = client.get("/products/products")

        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json(),{
                    "result" : [
                        {
                            "product_id"              : 1,
                            "product_name"            : "B-Complex",
                            "product_sub_category_id" : 1,
                            "product_sub_name"        : "The Busy B\"s",
                            "product_price"           : 13.00,
                            "product_is_new"          : True,
                            "product_description"     : [
                                "Organic pea pumpkin seed protein and hemp proteins",
                                "18g of protein per serving",
                                "15-serving tub",
                                "Made with creamy MCT oil and organic cocoa powder"
                            ],
                            "product_tumbnail_image"  : "https://media2.giphy.com/media/ioRCKwI9ox0Qg/200w.webp?cid=ecf05e47ha20pqgo4dri6cv9xfck439oi6wyofx64iyd4ovv&rid=200w.webp&ct=g"
                        },
                        {   "product_id"              : 2,
                            "product_name"            : "Iron",
                            "product_sub_category_id" : 2,
                            "product_sub_name"        : "The Blood Booster",
                            "product_price"           : 5.00,        
                            "product_is_new"          : False,
                            "product_description"     : [
                                "Organic pea pumpkin seed protein and hemp proteins",
                                "18g of protein per serving",
                                "15-serving tub",
                                "Made with creamy MCT oil and organic cocoa powder"
                            ],
                            "product_tumbnail_image"  : "https://media2.giphy.com/media/ioRCKwI9ox0Qg/200w.webp?cid=ecf05e47ha20pqgo4dri6cv9xfck439oi6wyofx64iyd4ovv&rid=200w.webp&ct=g"
                        },
                        {
                            "product_id"              : 3,
                            "product_name"            : "Shatavari",
                            "product_sub_category_id" : 3,
                            "product_sub_name"        : "The Rejuvenating Root",
                            "product_price"           : 9.00,
                            "product_is_new"          : True,
                            "product_description"     : [
                                "Organic pea pumpkin seed protein and hemp proteins",
                                "18g of protein per serving",
                                "15-serving tub",
                                "Made with creamy MCT oil and organic cocoa powder"
                            ],
                            "product_tumbnail_image"  : "https://media2.giphy.com/media/ioRCKwI9ox0Qg/200w.webp?cid=ecf05e47ha20pqgo4dri6cv9xfck439oi6wyofx64iyd4ovv&rid=200w.webp&ct=g"
                        },
                        {
                            "product_id"              : 4,
                            "product_name"            : "Collagen Matcha",
                            "product_sub_category_id" : 1,
                            "product_sub_name"        : "The Skin Hero",
                            "product_price"           : 32.00,
                            "product_is_new"          : False,
                            "product_description"     : [
                                "Organic pea pumpkin seed protein and hemp proteins",
                                "18g of protein per serving",
                                "15-serving tub",
                                "Made with creamy MCT oil and organic cocoa powder"
                            ],
                            "product_tumbnail_image"  : "https://media2.giphy.com/media/ioRCKwI9ox0Qg/200w.webp?cid=ecf05e47ha20pqgo4dri6cv9xfck439oi6wyofx64iyd4ovv&rid=200w.webp&ct=g"
                        },
                        {
                            "product_id"              : 5,
                            "product_name"            : "Plant Protein Vanilla",
                            "product_sub_category_id" : 2,
                            "product_sub_name"        : "Plant Power",
                            "product_price"           : 28.00,
                            "product_is_new"          : True,
                            "product_description"     : [
                                "Organic pea pumpkin seed protein and hemp proteins",
                                "18g of protein per serving",
                                "15-serving tub",
                                "Made with creamy MCT oil and organic cocoa powder"
                            ],
                            "product_tumbnail_image"  : "https://media2.giphy.com/media/ioRCKwI9ox0Qg/200w.webp?cid=ecf05e47ha20pqgo4dri6cv9xfck439oi6wyofx64iyd4ovv&rid=200w.webp&ct=g"
                        },
                        {
                            "product_id"              : 6,
                            "product_name"            : "Superberry",
                            "product_sub_category_id" : 3,
                            "product_sub_name"        : "The Antioxidant Ace",
                            "product_price"           : 26.00,
                            "product_is_new"          : True,
                            "product_description"     : [
                                "Organic pea pumpkin seed protein and hemp proteins",
                                "18g of protein per serving",
                                "15-serving tub",
                                "Made with creamy MCT oil and organic cocoa powder"
                            ],
                            "product_tumbnail_image"  : "https://media2.giphy.com/media/ioRCKwI9ox0Qg/200w.webp?cid=ecf05e47ha20pqgo4dri6cv9xfck439oi6wyofx64iyd4ovv&rid=200w.webp&ct=g"
                        },
                        {
                            "product_id"              : 7,
                            "product_name"            : "Dream Team",
                            "product_sub_category_id" : 1,
                            "product_sub_name"        : "On-the-go sleep support*",
                            "product_price"           : 7.00,
                            "product_is_new"          : False,
                            "product_description"     : [
                                "Organic pea pumpkin seed protein and hemp proteins",
                                "18g of protein per serving",
                                "15-serving tub",
                                "Made with creamy MCT oil and organic cocoa powder"
                            ],
                            "product_tumbnail_image"  : "https://media2.giphy.com/media/ioRCKwI9ox0Qg/200w.webp?cid=ecf05e47ha20pqgo4dri6cv9xfck439oi6wyofx64iyd4ovv&rid=200w.webp&ct=g"
                        },
                    ]
                }
            )
        
    def test_new_products_success(self):
        response = client.get("/products/products?is_new=1")

        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json(),{
                    "result" : [
                        {   "product_id"              : 1,
                            "product_name"            : "B-Complex",
                            "product_sub_category_id" : 1,
                            "product_sub_name"        : "The Busy B\"s",
                            "product_price"           : 13.00,        
                            "product_is_new"          : True,
                            "product_description"     : [
                                "Organic pea pumpkin seed protein and hemp proteins",
                                "18g of protein per serving",
                                "15-serving tub",
                                "Made with creamy MCT oil and organic cocoa powder"
                            ],
                            "product_tumbnail_image"  : "https://media2.giphy.com/media/ioRCKwI9ox0Qg/200w.webp?cid=ecf05e47ha20pqgo4dri6cv9xfck439oi6wyofx64iyd4ovv&rid=200w.webp&ct=g"
                        },
                        {
                            "product_id"              : 3,
                            "product_name"            : "Shatavari",
                            "product_sub_category_id" : 3,
                            "product_sub_name"        : "The Rejuvenating Root",
                            "product_price"           : 9.00,
                            "product_is_new"          : True,
                            "product_description"     : [
                                "Organic pea pumpkin seed protein and hemp proteins",
                                "18g of protein per serving",
                                "15-serving tub",
                                "Made with creamy MCT oil and organic cocoa powder"
                            ],
                            "product_tumbnail_image"  : "https://media2.giphy.com/media/ioRCKwI9ox0Qg/200w.webp?cid=ecf05e47ha20pqgo4dri6cv9xfck439oi6wyofx64iyd4ovv&rid=200w.webp&ct=g"
                        },
                        {
                            "product_id"              : 5,
                            "product_name"            : "Plant Protein Vanilla",
                            "product_sub_category_id" : 2,
                            "product_sub_name"        : "Plant Power",
                            "product_price"           : 28.00,
                            "product_is_new"          : True,
                            "product_description"     : [
                                "Organic pea pumpkin seed protein and hemp proteins",
                                "18g of protein per serving",
                                "15-serving tub",
                                "Made with creamy MCT oil and organic cocoa powder"
                            ],
                            "product_tumbnail_image"  : "https://media2.giphy.com/media/ioRCKwI9ox0Qg/200w.webp?cid=ecf05e47ha20pqgo4dri6cv9xfck439oi6wyofx64iyd4ovv&rid=200w.webp&ct=g"
                        },
                        {
                            "product_id"              : 6,
                            "product_name"            : "Superberry",
                            "product_sub_category_id" : 3,
                            "product_sub_name"        : "The Antioxidant Ace",
                            "product_price"           : 26.00,
                            "product_is_new"          : True,
                            "product_description"     : [
                                "Organic pea pumpkin seed protein and hemp proteins",
                                "18g of protein per serving",
                                "15-serving tub",
                                "Made with creamy MCT oil and organic cocoa powder"
                            ],
                            "product_tumbnail_image"  : "https://media2.giphy.com/media/ioRCKwI9ox0Qg/200w.webp?cid=ecf05e47ha20pqgo4dri6cv9xfck439oi6wyofx64iyd4ovv&rid=200w.webp&ct=g"
                        },
                    ]
                }
            )