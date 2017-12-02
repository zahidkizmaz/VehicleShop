from django.conf.urls import url

from shop.views import CategoryView , HomePageView 

urlpatterns = [
        url(r'^$', HomePageView.as_view(), name="home"),        
        url(r'^category$', CategoryView.as_view(), name="categorylist"), 
        
        ]
