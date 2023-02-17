from django.urls import path

from main_app import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('api/get-all/', views.GetDataViewSet.as_view({
        'get': 'get_all',
    })),
    path('api/get-range/', views.GetDataViewSet.as_view({
        'get': 'get_range',
    })),
    path('api/upload/file/', views.GetDataViewSet.as_view({
        'post': 'upload_data_from_file',
    }))
]
