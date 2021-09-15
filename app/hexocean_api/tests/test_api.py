from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models
from rest_framework.test import APIClient
from django.urls import reverse


def image_upload_url(base_image_id):
    '''Return URL fore base_image upload'''
    return reverse('images:images-upload', args=[base_image_id])


def sample_user(email='test@hexocean.pl', password='testpass'):
    '''Create a sample user'''
    return get_user_model().objects.create_user(email, password)


def sample_superuser(email='test@hexocean.pl', password='testpass'):
    '''Create a sample user'''
    return get_user_model().objects.create_superuser(email, password)


def sample_base_image(user, **params):
    '''Create and return a sample BaseImage'''
    return models.BaseImage.objects.create(user=user, name='sample')


class ApiTests(TestCase):
    '''Test for api'''

    def test_uploading_an_image_by_user(self):
        '''Test that uploading an image by new user is successful'''
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'testpass')

    # def test_upload_image_bad_request(self):
    #     '''Test uploading an invalid image'''
    #     url = image_upload_url(self.recipe.id)
    #     res = self.client.post(url, {'image': 'notimage'},
    #     format='multipart')
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class BaseImageTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'rsk@hexocean.pl',
            'testpass'
        )
        self.client.force_authenticate(self.user)
        self.base_image = sample_base_image(user=self.user)

    def tearDown(self):
        self.base_image.image.delete()

    # def test_upload_image_to_base_image(self):
    #     '''Test uploading an image to BaseImage'''
    #     url = image_upload_url(self.base_image.id)
    #     with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
    #         img = Image.new('RGB', (10, 10))
    #         img.save(ntf, format='jpg')
    #         ntf.seek(0)
    #         res = self.client.post(url, {'image': ntf}, format='multipart')
    #
    #     self.base_image.refresh_from_db()
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertIn('image', res.data)
    #     self.assertTrue(os.path.exists(self.base_image.image.path))
    #
    # def test_upload_invalid_image_to_base_image(self):
    #     '''Test uploading invalid image to base image'''
    #
    #     url = image_upload_url(self.base_image.id)
    #     res = self.client.post(url, {'image': 'not an image'},
    #                            format='multipart')
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
