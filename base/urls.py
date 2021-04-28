from django.urls import path
from . import views

urlpatterns = [
    path('users/login/', views.LoginView.as_view(), name='token_obtain_pair'),

    path('users/register', views.registerUser, name = 'register' ),

    path('',views.getRoutes,name='routes'),

    path('users/',views.getUsers,name='users'),
    path('users/profile/',views.getUserProfile,name='users-profile'),

    path('announcement/',views.getAnnouncement,name='announcement'),

    path('blogs/',views.getBlogs,name='blogs'),
    path('blogs/<str:pk>',views.getBlog,name='blog'),
    # path('announcement/new/',views.announcementForm,name='new'),
    # path('announcement/new/add',views.addAnnouncement,name='add')
]
