from django.urls import path
#from rest_framework.authtoken.views import obtain_auth_token


from . import views

urlpatterns = [
    #path('login/', obtain_auth_token),
    path('login/', views.LoginView.as_view()),
    path('accounts/', views.AccountView.as_view()),
    path('accounts/newest/<int:num>/', views.ListOrdersUsersView.as_view()),
    path('accounts/<pk>/', views.UpdateAccountView.as_view()),
    path('accounts/<pk>/management/', views.IsAdmUpdateAccountView.as_view()),


]