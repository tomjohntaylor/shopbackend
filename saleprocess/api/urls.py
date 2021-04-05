from django.urls import path
from saleprocess.api.views import *


urlpatterns = [

    path("profile/",
         CurrentProfileDetailAPIView.as_view(),
         name="current-profile-detail"),

]