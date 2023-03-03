import requests
import datetime
import time

from pandas import read_excel, notnull

from django.views.generic import TemplateView
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from main_app import models, serializers


def get_all_data():
    data = models.DataModel.objects.all()
    return data


class GetDataViewSet(viewsets.ModelViewSet):
    """  """
    
    queryset = models.DataModel.objects.all()
    serializer_class = serializers.DataSerializer
    
    @action(['get'], detail=True)
    def get_all(self, request, *args, **kwargs):
        serializer = serializers.DataSerializer(get_all_data(), many=True)
        return Response(serializer.data, status.HTTP_200_OK)
    
    @action(['get'], detail=True)
    def get_range(self, request, *args, **kwargs):
        if 'date_start' in request.GET and 'date_end' in request.GET:
            date_start, date_end = request.GET['date_start'], request.GET['date_end']
            data = models.DataModel.objects.filter(
                date_uploaded__range=[date_start, date_end]
            ).order_by('-date_uploaded')
            serializer = self.serializer_class(data, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        return Response({'error': 'Query parameters date_start and date_end are needed'}, status.HTTP_400_BAD_REQUEST)
    
    @csrf_exempt
    @action(['post'], detail=True)
    def upload_data_from_file(self, request):
        if request.data['file']:
            names = [
                "Название диалога", 
                "Стример",
                "Дата создания", 
                "Ссылка для скачивания", 
                "Ссылка на сайт", 
                "Оценка пользователем", 
                "Кол-во стримеров", 
                "Проведен ли стрим", 
                "Длительность",
            ]
            file = read_excel(request.data['file'], header=0, names=names)
            file = file.transpose()
            file = file.where(notnull(file), None)
            for row in file:
                try:
                    models.DataModel.objects.create(
                        title=file[row][0],
                        streamer=file[row][1],
                        createdAt=file[row][2],
                        logUrl=file[row][3],
                        websiteUrl=file[row][4],
                        rating=file[row][5],
                        streamsNumber=file[row][6],
                        isStreamMade=file[row][7],
                        duration=file[row][8],
                    )
                except Exception as e:
                    print(f'ERROR: {e}')
        return Response('ok', status.HTTP_201_CREATED)


class IndexView(TemplateView):
    """  """
    
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['DOMAIN'] = settings.DOMAIN
        context['DATA'] = get_all_data()
        return context