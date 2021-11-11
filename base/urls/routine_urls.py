from django.urls import path
from base.views import routine_views as views

urlpatterns = [

    path('<str:pk>/',views.getRoutine,name='routine'),

]
