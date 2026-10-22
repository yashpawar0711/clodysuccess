from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('api/enquiry/', views.api_submit_enquiry, name='api_enquiry'),
    path('api/quote/', views.api_submit_quote, name='api_quote'),
    path('api/pricing/', views.api_pricing_list, name='api_pricing_list'),
    path('api/project/<slug:slug>/', views.api_portfolio_details, name='api_project_details'),
]
