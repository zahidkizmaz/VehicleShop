from django.conf.urls import url

from shop.views import CategoryView

urlpatterns = [
                url(r'^category$', CategoryView.as_view(), name="categorylist"), 
        
        ]
