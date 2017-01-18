from rest_framework import serializers

from mad_web.events.models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('start_time', 'end_time', 'title', 'location', 'description', 'image_url', 'created_on', 'event_tags',
                  'speaker_bio', 'speaker', 'presented_by')
