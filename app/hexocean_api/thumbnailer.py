from PIL import Image
import random
import string
from core import models
import requests
from io import BytesIO
from django.core.files.base import ContentFile

'''Whole module needs refactoring to SOLID'''


def create_access_str(N):
    '''Creates a random access string for a thumbnail link'''
    access_str = ''.join(
        random.SystemRandom().choice(string.ascii_uppercase + string.digits)
        for _ in range(N))
    return access_str


def add_thumbnail_image_and_create_link(size, passed_image_url, instance,
                                        th_name):
    '''Function for adding an image to passed instance of Thumbnail and
    creating a link'''

    '''For some reason img has to be opened here, otherwise img.thumbnail
    does not work, probably memory-passing related, doesn't look clean atm'''
    img = Image.open(
        requests.get(passed_image_url, stream=True).raw)
    print(f'Size on the start: {size}, type: {type(size)}')
    if size is not None:
        img.thumbnail((100 * 10 ** 20, int(size)))

    image_io = BytesIO()
    img.save(image_io, format=img.format)
    instance.thumbnail.save(th_name + "." + img.format,
                            ContentFile(image_io.getvalue()))

    created_link = models.Link.objects.create(
        thumbnail=instance,
        access_str=create_access_str(9))

    return instance, created_link


class Thumbnailer:
    def __init__(self, id, passed_image_url, sizes, name):
        self.id = id
        self.passed_image_url = passed_image_url
        self.sizes = sizes
        self.name = name
        self.height = Image.open(
            requests.get(self.passed_image_url, stream=True).raw).size[1]

    def create_thumbnails(self):
        '''Creates a Thumbnail and a Link to the Thumbnail'''
        _, height = Image.open(
            requests.get(self.passed_image_url, stream=True).raw).size

        base_image_instance = models.BaseImage.objects.get(id=self.id)

        for size in self.sizes:
            if 0 < size < self.height:
                th_name = f'{self.name}{size}'
                '''Create a thumbnail object without an image'''
                created_thumbnail_object = models.Thumbnail.objects.create(
                    base_image=base_image_instance,
                    height=size,
                    name=th_name)

                '''Save an image to the object'''
                th_final, created_link = add_thumbnail_image_and_create_link(
                    size=size,
                    passed_image_url=self.passed_image_url,
                    instance=created_thumbnail_object,
                    th_name=th_name)

    def create_original(self):
        '''Creates a Thumbnail and a Link to the Thumbnail'''
        base_image_instance = models.BaseImage.objects.get(id=self.id)

        th_name = f'{self.name}original'
        '''Create a thumbnail object without an image'''
        created_thumbnail_object = models.Thumbnail.objects.create(
            base_image=base_image_instance,
            height=0,
            name=th_name)

        '''Save an image to the object'''
        th_final, created_link = add_thumbnail_image_and_create_link(
            size=None,
            passed_image_url=self.passed_image_url,
            instance=created_thumbnail_object,
            th_name=th_name)

    # def change_plans(self):
    # '''Function in case of account plan change'''
    # #1 Calculate the difference between current plan, and planned
    # #2 Delete the excessive thumbnails
    # #3 Create new thumbnails
