from django.urls import path
from . import views
urlpatterns = [
    path('signup_applicant/', views.signup_applicant_veiw, name='signup_applicant'),
    path('signup_company/', views.signup_company_veiw, name='signup_company'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
