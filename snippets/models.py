from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model
class Tags(models.Model):
   title = models.CharField(max_length=100,unique=True)
   class Meta:
      db_table="tags"

class Snippets(models.Model):

   title = models.CharField(max_length=50)
   text = models.CharField(max_length=200)
   create_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)
   user = models.ForeignKey(User,on_delete=models.CASCADE)
   tags = models.ManyToManyField(Tags)
   class Meta:
      db_table="snippets"
