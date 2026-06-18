@"
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve
from main import views

urlpatterns = [
    path('', include('main.urls')),
    path('logout/', views.user_logout, name='logout'),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
"@ | Out-File -Encoding utf8 C:\Users\Sait\Desktop\d\volleyball-project-main\volleyball_site\urls.py
