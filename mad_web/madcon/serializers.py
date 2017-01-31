# Serializers define the API representation.
from rest_framework import serializers

from mad_web.madcon.models import Registration, MADcon
from mad_web.users.serializers import UserSerializer

class RegistrationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Registration
        fields = (
            'id', 'dietary_restrictions', 'first_time', 'status', 't_shirt_size', 'madcon', 'created_at')

class RegistrationUserSerializier(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Registration
        fields = ('id', 'dietary_restrictions', 'first_time', 'status', 't_shirt_size', 'madcon', 'created_at', 'user')

class MADconSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MADcon
        fields = ('id', 'date')
