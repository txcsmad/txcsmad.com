# Serializers define the API representation.
from rest_framework import serializers

from mad_web.users.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = (
            'full_name', 'nick_name', 'graduation_date', 'username', 'gender', 'concentration', 'is_staff',)
