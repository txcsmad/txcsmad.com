# Serializers define the API representation.
from rest_framework import serializers

from mad_web.madcon.models import Registration, MADcon


class RegistrationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Registration
        fields = (
            'id', 'dietary_restrictions', 'first_time', 'status', 't_shirt_size', 'madcon', 'created_at')


class MADconSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MADcon
        fields = ('id'
                  'date',)
