from django.conf.urls import url

from shop.views import CategoryView , HomePageView, FirmView

urlpatterns = [
        url(r'^$', HomePageView.as_view(), name="home"),
        url(r'^category$', CategoryView.as_view(), name="categorylist"),
        url(r'^firm$',FirmView.as_view(), name="firmlist"),
      ]

