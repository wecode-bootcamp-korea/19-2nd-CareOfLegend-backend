from django.db import models

class User(models.Model):
    user_code         = models.IntegerField()
    nickname          = models.CharField(max_length=45)
    profile_image_url = models.CharField(max_length=2000, null=True)
    platform          = models.ForeignKey('SocialPlatform', on_delete=models.CASCADE)

    class Meta:
        db_table = 'users'

class SocialPlatform(models.Model):
    platform = models.CharField(max_length=45)

    class Meta:
        db_table = 'social_platforms'

class Answer(models.Model):
    user     = models.ForeignKey('User', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    option   = models.ForeignKey('Option', on_delete=models.CASCADE)

    class Meta:
        db_table = 'answers'

class Question(models.Model):
    query = models.CharField(max_length=500)
    user  = models.ManyToManyField('User', through='Answer')

    class Meta:
        db_table = 'questions'

class Option(models.Model):
    name      = models.CharField(max_length=45)
    image_url = models.CharField(max_length=2000)
    question  = models.ForeignKey('Question', on_delete=models.CASCADE)
    product   = models.OneToOneField('products.Product', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'options'
