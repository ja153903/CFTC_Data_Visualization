from django.conf.urls import url
from AreaChart.views import AreaChartView

urlpatterns = [
	url(r'^$', AreaChartView.as_view()),
]