from django.urls import path
from base.views import announcement_views as views

urlpatterns = [

    path('<str:pk>/',views.getAnnouncements,name='announcement'),
    path('',views.getAllAnnouncements,name='all_announcement'),

]
