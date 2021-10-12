from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model

# Create your models here.
class Snippets(models.Model):

   title = models.CharField(max_length=50)
   text = models.CharField(max_length=200)
   create_at = models.DateTimeField()
   user = models.ForeignKey(User)

   class Meta:
      db_table="snippets"
class Tags(models.Model):
   title = models.CharField(max_length=100,unique=True)
   snippet = models.ManyToManyField(Snippets)

   class Meta:
      db_table="tags"