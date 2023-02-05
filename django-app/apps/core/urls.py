from .views import (
    CompleteSummonerInfo,
    HomePage,
    Regions,
)
from django.urls import path


urlpatterns = [
    path('info',
        CompleteSummonerInfo.as_view(),
        name="info",
    ),
    path('',
        HomePage.as_view(), 
        name="home", 
    ),
    path('regions',
         Regions.as_view(),
         name="regions",
    ),
]