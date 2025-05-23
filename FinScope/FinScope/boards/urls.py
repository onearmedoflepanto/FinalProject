from django.urls import path
from . import views

urlpatterns = [    
    path('comments/<int:pk>/', views.edit_comment),
    path('comments/<str:name>/', views.get_comments),
]
