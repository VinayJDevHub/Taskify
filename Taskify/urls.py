from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from task import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('', include('task.urls')),
    path("__reload__/", include("django_browser_reload.urls")),
]




