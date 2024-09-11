# espace_administration/urls.py


from django.contrib import admin
from django.urls import path, include
from admin_panel import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.connexion, name='connexion'),
    path('admin_panel/', include('admin_panel.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('chatbot_nouveau/', include('chatbot_nouveau.urls')),

]
    

