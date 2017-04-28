from django.conf.urls import url
from api.indicator.views import IndicatorDataList, IndicatorDataAggregations, ScatterPlotDataList

from django.views.decorators.cache import cache_page
from django.conf import settings


urlpatterns = [
    url(r'^$',
        IndicatorDataList.as_view(),
        name='indicator-list'),
    url(r'^scatter/$',
        ScatterPlotDataList.as_view(),
        name='scatterplotdata-list'),
    url(r'^aggregations/$',
        cache_page(settings.API_CACHE_SECONDS)(IndicatorDataAggregations.as_view()),
        name='indicator-aggregations'),
]
