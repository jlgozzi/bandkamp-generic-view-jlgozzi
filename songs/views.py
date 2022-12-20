from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Song
from rest_framework.pagination import PageNumberPagination
from .serializers import SongSerializer
from albums.models import Album
from rest_framework.generics import ListCreateAPIView


class SongView(ListCreateAPIView, PageNumberPagination):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Song.objects.all()
    serializer_class = SongSerializer

    page_size = 2
    
    lookup_url_kwarg = "pk"

    def get_queryset(self):
        pk = self.kwargs[self.lookup_url_kwarg]
        return Song.objects.filter(album_id=pk)

    def perform_create(self, serializer):
        album = get_object_or_404(Album, id=self.kwargs[self.lookup_url_kwarg])
        serializer.save(album=album)

