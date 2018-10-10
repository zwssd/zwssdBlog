from django.conf.urls import url
from zuser.views import UserControl

urlpatterns = [
        url(r'^usercontrol/(?P<slug>\w+)$', UserControl.as_view()),
]
