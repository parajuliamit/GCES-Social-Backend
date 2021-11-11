from django.urls import path
from base.views import event_views as views

urlpatterns = [

    path('<str:pk>/',views.getEvents,name='events'),

]
