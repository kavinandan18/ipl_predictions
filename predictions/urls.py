from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('predictions-index/', views.index, name='index'),
    path('make_prediction/<int:match_id>/', views.make_prediction, name='make_prediction'),
    path('prediction_success/', views.prediction_success, name='prediction_success'),
    path('edit_match/<int:match_id>/', views.edit_match, name='edit_match'),
    path('delete_match/<int:match_id>/', views.delete_match, name='delete_match'),
    path('create_match/', views.create_match, name='create_match'),
    path('view_match/<int:match_id>/', views.view_match, name='view_match'),
    path('predictions-views-status/',views.predictions_view, name='predictions_view'),
    path('predictions-views-status/<int:pk>/edit/', views.edit_prediction, name='edit_prediction'),
    path('predictions-views-status/<int:pk>/delete/', views.delete_prediction, name='delete_prediction'),
    path('change_password/', auth_views.PasswordChangeView.as_view(template_name='predictions/change_password.html'), name='change_password'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='predictions/password_change_done.html'), name='password_change_done'),  
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='predictions/reset_password.html'), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='predictions/password_reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='predictions/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='predictions/password_reset_complete.html'), name='password_reset_complete'),

]

