from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_view, name='index'),
    path('api/v1/download/', download, name='download'),
    path('api/v1/download_continue/', download_continue, name='download_continue'),
    # path('api/v1/download2/', download2, name='download2'),
    path('api/v1/download_chemp/', download_chemp, name='download_chemp'),
    path('api/v1/download_managerlink/', download_managerlink, name='download_managerlink'),
    path('api/v1/managers/', include('managers.urls')),
]
