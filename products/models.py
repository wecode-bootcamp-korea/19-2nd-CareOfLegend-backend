from django.db     import models

class MainCategory(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'main_categories'

class SubCategory(models.Model):
    name          = models.CharField(max_length=45)
    description   = models.CharField(max_length=2000)
    main_category = models.ForeignKey('MainCategory', on_delete=models.CASCADE)

    class Meta:
        db_table = 'sub_categories'

class Product(models.Model):
    name          = models.CharField(max_length=45)
    sub_name      = models.CharField(max_length=45)
    price         = models.DecimalField(max_digits=10, decimal_places=2)
    description   = models.CharField(max_length=2000)
    is_new        = models.BooleanField()
    heath_goal    = models.ManyToManyField('HealthGoal', through='ProductHealthGoal')
    symbol        = models.ManyToManyField('Symbol', through='ProductSymbol')
    main_category = models.ForeignKey('MainCategory', on_delete=models.CASCADE)
    sub_category  = models.ForeignKey('SubCategory', on_delete=models.CASCADE)

    class Meta:
        db_table = 'products'

class ProductImage(models.Model):
    image_url        = models.CharField(max_length=2000)
    thumbnail_status = models.BooleanField()
    product          = models.ForeignKey('Product', on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_images'

class HealthGoal(models.Model):
    name     = models.CharField(max_length=45)
    icon_url = models.CharField(max_length=2000)
    option   = models.ForeignKey('users.Option', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'health_goals'

class ProductHealthGoal(models.Model):
    product     = models.ForeignKey('Product', on_delete=models.CASCADE)
    health_goal = models.ForeignKey('HealthGoal', on_delete=models.CASCADE)

    class Meta:
        db_table = 'products_health_goals'

class Symbol(models.Model):
    name      = models.CharField(max_length=45)
    image_url = models.CharField(max_length=2000)

    class Meta:
        db_table = 'symbols'

class ProductSymbol(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    symbol  = models.ForeignKey('Symbol', on_delete=models.CASCADE)

    class Meta:
        db_table = 'products_symbols'

