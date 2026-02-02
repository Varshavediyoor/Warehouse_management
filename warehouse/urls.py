"""
URL configuration for warehouse project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from admin_app import views as admin_views  # import switch_language view

# Language switch URL must be outside i18n_patterns
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),  # Django's default language switch
    path('switch-language/<str:lang_code>/', admin_views.switch_language, name='switch_language'),
    
]

# urlpatterns += i18n_patterns(
#     path('admin/', admin.site.urls),
#     path('', include('admin_app.urls')),
#     path('dashboard/maintenance/', include('maintenance.urls')),
#     path('dashboard/inventory-manager/', include('inventory_manager.urls')),
#     path('dashboard/procurement-officer/', include('procurement_officer.urls')),
    
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('admin_app.urls')),
    path(
        'procurement-officer/dashboard/',
        include('procurement_officer.urls')
    ),
    path('inventory-manager/dashbaord/', include('inventory_manager.urls')),
    path('security/dashboard/', include('security.urls')),
    
    
    path('quality_control/dashboard/', include('quality_control.urls')),
)







# Static and media setup
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



