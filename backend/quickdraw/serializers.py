from rest_framework import serializers
from quickdraw.models import Drawing

class DrawingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drawing
        fields = '__all__'