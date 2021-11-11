from django.urls import path
from base.views import assignment_views as views

urlpatterns = [

    path('create/',views.createAssignment,name='new_assignment'),
    path('submit/',views.submitAssignment,name='submit_assignment'),
    path('mark/<str:pk>/', views.markAssignment, name='mark_assignment'),
    path('view/<str:pk>/',views.getAssignment,name='assignment'),
    path('<str:pk>/',views.getAssignments,name='assignments'),

]
