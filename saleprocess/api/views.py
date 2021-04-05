from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from saleprocess.models import Profile
from saleprocess.api.serializers import ProfileSerializer


class CurrentProfileDetailAPIView(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        profile_serializer = ProfileSerializer(request.user)
        return Response(profile_serializer.data)
