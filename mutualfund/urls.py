
from django.urls import path,include
from .views import  getmutualfund,mutualfunddetail,inputform

app_name='mutualfund'


urlpatterns = [
    # default run this pass query string like this 
    # locahost:8888/?income=1000&year=4
    path('',inputform,name='index'),
    path('nav',getmutualfund,name='nav'),
    # localhsot:8888/detail/100033
    path('detail/<int:schemacode>',mutualfunddetail)

]