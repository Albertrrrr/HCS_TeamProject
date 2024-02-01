from django.db import models


# Create your models here.

class User(models.Model):
    nickname = models.CharField(max_length=20, verbose_name="nickname")
    email = models.EmailField(verbose_name="email",unique=True)

    class Mate:
        verbose_name = "user information"
        verbose_name_plural = verbose_name
        db_table = "user"
