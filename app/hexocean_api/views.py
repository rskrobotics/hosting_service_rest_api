from rest_framework import viewsets, generics, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser, \
    BasePermission
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.urls import reverse
from core.models import User, BaseImage, Thumbnail, Link, AccountPlan
from .serializers import UserSerializer, BaseImageSerializer, \
    AccountPlanSerializer, LinkSerializer
from django.contrib.auth import get_user_model
from .thumbnailer import thumbnailer
from .custom_renderers import JPEGRenderer, PNGRenderer
from datetime import datetime
import pytz, random, string

utc = pytz.UTC

'''Permission'''


def create_access_str(N):
    access_str = ''.join(
        random.SystemRandom().choice(string.ascii_uppercase + string.digits)
        for _ in range(N))
    return access_str


class CanCreateTempLinks(BasePermission):
    message = 'Creating temporary links is for users with such permission'

    def has_permission(self, request, view):
        if request.user:
            if request.user.account_plan.can_expire_links:
                return True
        return False


'''Api Views'''


class UserLoginApiView(ObtainAuthToken):
    '''Handle creating user authentication tokens'''
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ImageAPIView(generics.RetrieveAPIView):
    '''API View that checks for presence of an image with provided access str'''
    renderer_classes = [JPEGRenderer, PNGRenderer]

    def get(self, request, *args, **kwargs):
        '''Get method that takes into consideration the expiring links'''
        access_str = self.kwargs['access_str']
        try:
            queryset = Thumbnail.objects.get(
                link__access_str=access_str)
            relevant_link = Link.objects.filter(access_str=access_str)
            duration = relevant_link[0].duration
            # Compare (current time - tiem of creation) with duration
            if duration:
                if (utc.localize(datetime.now()) -
                    relevant_link[0].created_on).total_seconds() > duration:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            return Response(queryset.thumbnail)
        except Thumbnail.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class Logout(APIView):
    '''Logout View for deleting the authorisation token'''

    def post(self, request):
        return self.logout(request)

    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


'''Viewsets'''


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

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

        # user = self.request.user
        # thumbnail_sizes = \
        #     get_user_model().objects.filter(user=self.request.user)
        # thumbnailer(path, thumbnail_sizes, finalpath)

    def get_queryset(self):
        '''Retrieve the BaseImages for the authenticated user'''
        return self.queryset.filter(user=self.request.user)


class AccountPlanViewSet(viewsets.ModelViewSet):
    '''Viewset for AccountPlan model'''

    queryset = AccountPlan.objects.all()
    serializer_class = AccountPlanSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]


class ExpiringLinkViewSet(viewsets.GenericViewSet,
                          mixins.CreateModelMixin):
    '''Viewset for creation of expiring links'''
    serializer_class = LinkSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, CanCreateTempLinks]
    model = Link

    def create(self, request):
        if self.get_serializer(Link, data=request.data).is_valid():
            if not request.data['duration'] or not request.data['thumbnail']:
                return Response({'msg': 'Try providing all the data buddy'},
                                status=status.HTTP_400_BAD_REQUEST)

            created_link = Link.objects.create(
                thumbnail=Thumbnail.objects.get(id=request.data['thumbnail']),
                access_str=create_access_str(9),
                duration=request.data[
                    'duration'])

            return_url = request.build_absolute_uri(
                reverse('hexocean_api:images',
                        kwargs={'access_str': created_link.access_str}))

            return Response({'msg': 'Success', 'Link': return_url},
                            status=status.HTTP_200_OK)

        return Response({'msg': 'Serializer not valid'},
                        status=status.HTTP_200_OK)
