from rest_framework import serializers

from main_app import models


class DataSerializer(serializers.ModelSerializer):
    """  """
    
    class Meta:
        model = models.DataModel
        fields = '__all__'