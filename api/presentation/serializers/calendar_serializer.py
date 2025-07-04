from rest_framework import serializers

from infrastructure import model

class CalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = model.Calendar
        fields = '__all__'