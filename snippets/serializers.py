
from rest_framework import serializers
from .models import Snippets, Tags

class POSTSnippetsSerializer(serializers.ModelSerializer):
   tags = serializers.ListField()

   class Meta:
      model = Snippets
      fields = ['title','text','tags']



class SnippetLinkSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='snippets-details',lookup_field='id', read_only=True)
    class Meta:
        model = Snippets
        fields = ['id','title', 'text', 'create_at','updated_at','url']
     


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ['id','title']
