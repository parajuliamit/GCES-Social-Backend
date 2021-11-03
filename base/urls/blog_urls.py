from django.urls import path
from base.views import blog_views as views

urlpatterns = [

    path('create/',views.postBlog,name='create_blog'),
    path('comment/',views.postComment,name='comment'),
    path('like/<str:pk>/', views.likePost, name='like_post'),
    path('<str:pk>/',views.getBlog,name='blog'),
    path('',views.getBlogs,name='blogs'),

]
