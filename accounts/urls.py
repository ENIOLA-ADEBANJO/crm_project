from . import views

from django.contrib.auth import views as auth_views
from django.urls import path

urlpatterns = [
    path('register/', views.register_page, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),

    path('', views.dashboard, name='dashboard'),

    path('user/', views.user_page, name='user'),
    path('user_setting/', views.user_setting, name='user_setting'),
    
    path('customer/<str:pk>/', views.customer, name='customer'),
    path('product/', views.product, name='product'),

    path('create_order/<str:pk>/', views.create_order, name='create_order'),
    path('update_order/<str:pk>/', views.update_order, name='update_order'),
    path('delete_order/<str:pk>/', views.delete_order, name='delete_order'),
 

    path('reset_password/', 
    auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'),
    name='reset_password'),

    path('reset_password_sent/',
    auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_sent.html'), 
    name='password_reset_done'),

    path('reset/<uidb64>/<token>/', 
    auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_form.html'), 
    name='password_reset_confirm'),

    path('reset_password_complete/', 
    auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_done.html'), 
    name='password_reset_complete'),

]


'''
1 - Submit email form                         //PasswordResetView.as_view()
2 - Email sent success message                //PasswordResetDoneView.as_view()
3 - Link to password Rest form in email       //PasswordResetConfirmView.as_view()
4 - Password successfully changed message     //PasswordResetCompleteView.as_view()
'''