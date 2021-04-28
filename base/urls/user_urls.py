from django.urls import path
from base.views import user_views as views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='token_obtain_pair'),

    path('register', views.registerUser, name = 'register' ),

    path('',views.getUsers,name='users'),

    path('profile/',views.getUserProfile,name='users-profile'),
    path('profile/edit',views.editName,name='users-profile-edit'),
    path('change-password',views.changePassword,name='users-change-password'),

]
