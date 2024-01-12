from django.urls import path 
from . import views
from .views import ReceiveJSONDataView

urlpatterns = [
    path('', views.index,name = 'index'),
    path('api/list/', views.listes),
    path('api/ajout/',views.add),
    path('api/test/',ReceiveJSONDataView.as_view(), name='receive_json_data')
]
