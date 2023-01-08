from django.urls import include, path

from test_app.urls import urlpatterns as test_app_urlpatterns

urlpatterns = [
    path("test_app/", include(test_app_urlpatterns)),
]
