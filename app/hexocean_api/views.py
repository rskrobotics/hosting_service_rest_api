from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from core.models import User, BaseImage
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from .serializers import UserSerializer, BaseImageSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class UserLoginApiView(ObtainAuthToken):
    '''Handle creating user authentication tokens'''
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class Logout(APIView):
    '''Logout View for deleting the authorisation token'''

    def post(self, request):
        return self.logout(request)

    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    '''Viewset for managing users'''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]


class BaseImageViewSet(viewsets.ModelViewSet):
    '''Viewset for listing and retrieving your base images'''
    queryset = BaseImage.objects.all()
    serializer_class = BaseImageSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        '''Retrieve the BaseImages for the authenticated user'''
        return self.queryset.filter(user=self.request.user)

# class ImageFromLinkViewSet(viewsets.GenericViewSet,
#                            mixins.

