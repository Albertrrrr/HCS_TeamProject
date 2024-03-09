from django.db import models


# Create your models here.

class User(models.Model):
    nickname = models.CharField(max_length=20, verbose_name="nickname")
    email = models.EmailField(verbose_name="email",unique=True)

    class Mate:
        verbose_name = "user information"
        verbose_name_plural = verbose_name
        db_table = "user"

class PageResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    page_1_responses = models.TextField()
    page_2_responses = models.TextField()
    page_3_responses = models.TextField()
    page_4_responses = models.TextField()
    page_5_responses = models.TextField()
    page_6_responses = models.TextField()
    quiz = models.TextField()

