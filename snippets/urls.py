from django.urls import path

from .views import SingleSnippetsView,SnippetsView,TagsView,TagsSnippetsView

urlpatterns = [
    path('snippets/',SnippetsView.as_view(),name="snippets-create"),
    path('snippet/<int:snippet_id>',SingleSnippetsView.as_view(),name="snippets-details"),
    path('tags/',TagsView.as_view()),
    path('tag/snippet/<int:tag_id>',TagsSnippetsView.as_view()),

]
