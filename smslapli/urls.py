from django.conf import settings
from django.conf.urls import include, url, patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.conf.urls import *
from rapidsms.backends.kannel.views import KannelBackendView


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    # RapidSMS Donnees_de_base URLs
    url(r'^accounts/', include('rapidsms.urls.login_logout')),
    url(r'^$', 'rapidsms.views.dashboard', name='rapidsms-dashboard'),
    # RapidSMS contrib app URLs
    url(r'^httptester/', include('rapidsms.contrib.httptester.urls')),
    url(r'^messagelog/', include('rapidsms.contrib.messagelog.urls')),
    url(r'^messaging/', include('rapidsms.contrib.messaging.urls')),
    url(r'^registration/', include('rapidsms.contrib.registration.urls')),
    url(r"^backend/kannel-fake-smsc/$",KannelBackendView.as_view(backend_name="kannel-fake-smsc")),

    # Third party URLs
    url(r'^selectable/', include('selectable.urls')),
    url(r"^backend/kannel-usb0-smsc/$", KannelBackendView.as_view(backend_name="kannel-usb0-smsc")),
    url(r"^rapport/pluie","public.views.rpluie"),
    url(r"^public", "public.views.acc"),
    url(r"^json_rap", "public.views.json_rap"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



# urlpatterns = patterns('',
#     # ...
#     url(r"^backend/kannel-fake-smsc/$",KannelBackendView.as_view(backend_name="kannel-fake-smsc")),
# )