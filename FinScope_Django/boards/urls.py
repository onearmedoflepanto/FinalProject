from django.urls import path
from . import views

urlpatterns = [    
    # Post URLs
    path('posts/', views.post_list_create),
    path('posts/<int:pk>/', views.post_detail),
    path('posts/<int:pk>/like/', views.post_like),
    path('posts/<int:pk>/bookmark/', views.post_bookmark),
    
    # Comment URLs (nested under posts)
    path('posts/<int:post_pk>/comments/', views.comment_list_create),
    path('posts/<int:post_pk>/comments/<int:comment_pk>/', views.comment_detail),
]
