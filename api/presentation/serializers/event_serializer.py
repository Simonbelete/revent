from rest_framework import serializers

from infrastructure import model
from infrastructure.constants import FREQ_CHOICES, WEEKDAYS

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = model.Event
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']

    def validate(self, data):
        recurrence = data.get('recurrence')
        freq = data.get('freq')
        weekdays = data.get('weekdays')
        relative_week_number = data.get('relative_week_number')
        relative_weekday = data.get('relative_weekday')
        start_datetime = data.get('start_datetime')
        end_datetime = data.get('end_datetime')

        if recurrence:
            if freq not in dict(FREQ_CHOICES):
                raise serializers.ValidationError("Frequency must be daily, weekly, or monthly for recurring events.")

            if freq == 'weekly':
                if not weekdays or len(weekdays) == 0:
                    raise serializers.ValidationError("For weekly recurrence, select at least one weekday.")

            if freq == 'monthly':
                if relative_week_number is None or relative_weekday is None:
                    raise serializers.ValidationError("For monthly recurrence, relative week number and weekday are required.")
        else:
            if not start_datetime or not end_datetime:
                raise serializers.ValidationError('Start and end can not be null')
        return data

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
