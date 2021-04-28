from django.urls import path
from base.views import announcement_views as views

urlpatterns = [

    path('',views.getAnnouncement,name='announcement'),

]
