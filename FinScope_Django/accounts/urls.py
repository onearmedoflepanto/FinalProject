from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login),
    path("logout/", views.logout),
    path("sign_up/", views.sign_up),
    path("delete/", views.delete),
    path("mypage/", views.mypage),
    path("follow/<int:pk>/", views.follow),
    path("google/callback/", views.google_login),
    
    # URLs for all financial products (listing)
    path("financial-products/", views.FinancialProductListView.as_view(), name='financial_product_list'),

    # URLs for saved financial products
    path("saved-products/", views.save_financial_product, name='save_financial_product'),
    path("saved-products/<int:product_pk>/", views.unsave_financial_product, name='unsave_financial_product'),
    path("saved-products/<int:saved_product_pk>/toggle-notification/", views.toggle_product_notification, name='toggle_product_notification'),
]
