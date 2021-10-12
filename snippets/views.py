
# Create your views here.
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from django.contrib.auth.models import User
from django.db import transaction

from .serializers import POSTSnippetsSerializer,SnippetLinkSerializer,TagsSerializer
from .models import Snippets,Tags

class SnippetsView(APIView):

   permission_classes = [IsAuthenticated]

   def post(self,request):
      try:
         serializer = POSTSnippetsSerializer(data=request.data)
         # validate data
         if serializer.is_valid():
            data = serializer.data
            user_tags = data.pop('tags')
            snippet = Snippets(**data,user=request.user)
            snippet.save()
            db_tags = Tags.objects.filter(title__in=user_tags)
            if len(db_tags)>0:
               snippet.tags.add(*db_tags)
            for tag in db_tags:
               user_tags.remove(tag.title)
            
            new_tags = []
            with transaction.atomic():
               for t in user_tags:
                  new_tag = Tags.objects.create(title=t)  
                  new_tags.append(new_tag)
            if len(new_tags)>0:
               snippet.tags.add(*new_tags)

            return JsonResponse({'message':"success"})
         return JsonResponse({'message':"invalid data",'errors':serializer.errors},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
      except Exception as e:
         print(e)
         return JsonResponse({'message':"server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


   def get(self,request):
         try:
            snippets = Snippets.objects.filter(user=request.user)
            total = len(snippets)
            ser = SnippetLinkSerializer(snippets,many=True,context={'request':request}).data
            print(snippets)
            print(ser)
            return JsonResponse({'message':"success",'data':ser,'total':total},status=status.HTTP_200_OK)
         except Exception as e:
            print(e)
            return JsonResponse({'message':"server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class SingleSnippetsView(APIView):
   permission_classes = [IsAuthenticated]

   def get(self,request,snippet_id):
      try:
         snippet = Snippets.objects.filter(pk=snippet_id)
         if not snippet:
            return  JsonResponse({'message':"Snippet not found"},status=status.HTTP_404_NOT_FOUND)
         ser = SnippetLinkSerializer(snippet).data
         return JsonResponse({'message':"Success",'data':ser},status=status.HTTP_200_OK)
      except Exception as e:
         print(e)
         return JsonResponse({'message':"server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


   def put(self,request,snippet_id):

      try:
         serializer = POSTSnippetsSerializer(data=request.data)
         # validate data
         if serializer.is_valid():
            data = serializer.data
            user_tags = data.pop('tags')
            
            snippet = Snippets.objects.filter(pk=snippet_id)
            if not snippet:
               return JsonResponse({'message':"Snippets not found"},status=status.HTTP_404_NOT_FOUND)
            snippet = snippet[0]
            snippet.text = data['text']
            snippet.title = data['title']

            snippet.save()
            db_tags = Tags.objects.filter(title__in=user_tags)
            if len(db_tags)>0:
               snippet.tags.add(*db_tags)
            for tag in db_tags:
               user_tags.remove(tag.title)
            
            new_tags = []
            with transaction.atomic():
               for t in user_tags:
                  new_tag = Tags.objects.create(title=t)  
                  new_tags.append(new_tag)
            if len(new_tags)>0:
               snippet.tags.add(*new_tags)
            ser = SnippetLinkSerializer(snippet).data
            return JsonResponse({'message':"success",'data':ser})
         return JsonResponse({'message':"invalid data",'errors':serializer.errors},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
      except Exception as e:
         print(e)
         return JsonResponse({'message':"server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

   def delete(self,request,snippet_id):
         try:
            Snippets.objects.filter(pk=id).delete()
            return JsonResponse({'message':"success",},status=status.HTTP_200_OK)
         except Exception as e:
            print(e)
            return JsonResponse({'message':"server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TagsView(APIView):
   permission_classes = [IsAuthenticated]

   def get(self,request):
      try:
         tags = Tags.objects.all()
         print(tags)
         if not tags:
            return  JsonResponse({'message':"Snippet not found"},status=status.HTTP_404_NOT_FOUND)
         ser = TagsSerializer(tags,many=True).data
         return JsonResponse({'message':"Success",'data':ser},status=status.HTTP_200_OK)
      except Exception as e:
         print(e)
         return JsonResponse({'message':"server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class TagsSnippetsView(APIView):
   permission_classes = [IsAuthenticated]

   def get(self,request,tag_id):
      try:
         snippets = Snippets.objects.filter(tags=tag_id)
         if not snippets:
            return  JsonResponse({'message':"Snippet not found"},status=status.HTTP_404_NOT_FOUND)
         ser = SnippetLinkSerializer(snippets,many=True).data
         return JsonResponse({'message':"Success",'data':ser},status=status.HTTP_200_OK)
      except Exception as e:
         print(e)
         return JsonResponse({'message':"server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
