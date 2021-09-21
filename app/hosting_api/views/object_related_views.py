from rest_framework import viewsets, generics, mixins
from hosting_api.custom_renderers import JPEGRenderer, PNGRenderer
from hosting_api.thumbnailer import Thumbnailer
from core.models import BaseImage, Thumbnail, Link, AccountPlan
from hosting_api.serializers import BaseImageSerializer, \
    AccountPlanSerializer, BaseImageListSerializer, ExpiringLinkSerializer, \
    ThumbnailSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from hosting_api.custom_permissions import CanCreateTempLinks
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from django.urls import reverse
import random
import string
import pytz

utc = pytz.UTC


def create_access_str(N):
    '''Creates a random access string for a thumbnail link'''
    access_str = ''.join(
        random.SystemRandom().choice(string.ascii_uppercase + string.digits)
        for _ in range(N))
    return access_str


class ImageAPIView(generics.RetrieveAPIView):
    '''API View that checks for presence of an image
    with provided access str'''
    renderer_classes = [JPEGRenderer, PNGRenderer]

    def get(self, request, *args, **kwargs):
        '''Get method that takes into consideration the expiring links'''
        utc = pytz.UTC
        access_str = self.kwargs['access_str']
        try:
            queryset = Thumbnail.objects.get(
                link__access_str=access_str)
            relevant_link = Link.objects.filter(access_str=access_str)
            duration = relevant_link[0].duration
            if duration:
                if (utc.localize(datetime.now()) -
                    relevant_link[0].created_on).total_seconds() \
                        > duration:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            return Response(queryset.thumbnail)
        except Thumbnail.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class BaseImageViewSet(viewsets.ModelViewSet):
    '''Viewset for listing and retrieving your base images'''
    queryset = BaseImage.objects.all()
    serializer_class = BaseImageSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        name = serializer.data['name']
        thumbnail_sizes = AccountPlan.objects.get(
            user__name=self.request.user).thumbnail_sizes
        base_image_id = serializer.data['id']
        image = serializer.data['image']

        '''Create the needed thumbnails/original thumbnail'''
        thumbnailer = Thumbnailer(base_image_id, image, thumbnail_sizes,
                                  name)

        thumbnailer.create_thumbnails()
        if self.request.user.account_plan.original_link_access:
            thumbnailer.create_original()

    def get_serializer_class(self):
        if self.action == 'list':
            return BaseImageListSerializer
        return BaseImageSerializer

    def get_queryset(self):
        '''List the BaseImages for the authenticated user'''
        return self.queryset.filter(user=self.request.user)


class AccountPlanViewSet(viewsets.ModelViewSet):
    '''Viewset for AccountPlan model'''

    queryset = AccountPlan.objects.all()
    serializer_class = AccountPlanSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]


class ExpiringLinkViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    '''Viewset for creation of expiring links'''
    serializer_class = ExpiringLinkSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, CanCreateTempLinks]

    def create(self, request):
        if self.get_serializer(Link, data=request.data).is_valid():
            current_user = self.request.user
            owner = BaseImage.objects.get(
                thumbnail__id=self.request.data['thumbnail']).user
            print(f'Current_user {current_user} Owner {owner}')

            '''If below should not be possible, it's a hotfix 2 hrs before
            deadline, queryset was not working, obviously unit tests should
            catch that'''

            if current_user != owner:
                return Response({'msg': 'Use your own thumbnail'},
                                status=status.HTTP_400_BAD_REQUEST)

                if not request.data['duration'] or not \
                        request.data['thumbnail']:
                    return Response(
                        {'msg': 'Try providing all the data buddy'},
                        status=status.HTTP_400_BAD_REQUEST)

            created_link = Link.objects.create(
                thumbnail=Thumbnail.objects.get(id=request.data['thumbnail']),
                access_str=create_access_str(9),
                duration=request.data[
                    'duration'])

            return_url = request.build_absolute_uri(
                reverse('hosting_api:images',
                        kwargs={'access_str': created_link.access_str}))

            return Response({'msg': 'Success', 'Link': return_url},
                            status=status.HTTP_200_OK)

        return Response({'msg': 'Serializer not valid, is duration in range?'},
                        status=status.HTTP_400_BAD_REQUEST)


class MyThumbnails(viewsets.GenericViewSet, mixins.ListModelMixin):
    '''Viewset for listing thumbnails available for our user'''
    queryset = Thumbnail.objects.all()
    serializer_class = ThumbnailSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        '''List the Thumbnails for the authenticated user'''
        print('lets_filter')
        return self.queryset.filter(base_image__user=self.request.user)
