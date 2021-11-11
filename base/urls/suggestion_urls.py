from django.urls import path
from base.views import suggestion_views as views

urlpatterns = [
    path('create/',views.postSuggestion,name='create_suggestion'),
]
