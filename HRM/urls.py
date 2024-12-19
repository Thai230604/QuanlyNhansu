from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/login/', permanent=False)),  # Chuyển hướng đến trang login
    path('', include('hr.urls')),  # Bao gồm đường dẫn của app phụ hr
]

# Thêm phần phục vụ media files trong chế độ phát triển
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
