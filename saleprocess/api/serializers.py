from rest_framework import serializers
from saleprocess.models import Profile

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = "__all__"
        depth = 1