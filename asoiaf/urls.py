from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('wall/', include('the_wall.urls')),
    path('admin/', admin.site.urls),
]
