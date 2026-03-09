from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.communityHome, name="communityForumHome"),
    path('discuss/<str:pk>',views.communitySeePost,name='communitySeePost'),
    path('create-post',views.communityCreatePost,name='communityCreatePost'),
    path('edit-post/<str:pk>',views.communityEditPost,name='communityEditPost'),
    path('delete-post/<str:pk>',views.communityDeletePost,name='communityDeletePost'),
    path('add-comment/',views.communityAddComment, name='communityAddComment'),
    path('add-reply/', views.communityAddCommentReply, name="communityAddCommentReply"),
    path('delete-comment/',views.communityDeleteComment,name='communityDeleteComment'),
    # path('delete-comment/<str:pk>',views.communityDeleteComment,name='communityDeleteComment'),
]
