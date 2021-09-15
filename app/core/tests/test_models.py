from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models
from unittest.mock import patch


def sample_user(email='test@hexocean.pl', password='testpass'):
    '''Create a sample user'''
    return get_user_model().objects.create_user(email, password)


def sample_superuser(email='test@hexocean.pl', password='testpass'):
    '''Create a sample user'''
    return get_user_model().objects.create_superuser(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        '''Test creating a new user with an email is successful'''
        email = 'email@hexocean.pl'
        password = 'testpass'

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_create_superuser(self):
        '''Test creating a new superuser is successful'''
        user = get_user_model().objects.create_superuser(
            'test@hexocean.pl',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_new_user_email_normalized(self):
        '''Test the email for a new user is normalized'''
        email = 'email@heXOcean.pl'
        password = 'testpass'
        user = get_user_model().objects.create_user(email=email,
                                                    password=password)
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        '''Test creating user with no email raises error'''
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'testpass')

    def test_account_plan_str(self):
        '''Test the AccountPlan string representation'''
        account_plan = models.AccountPlan.objects.create(
            name='Coolplan',
            thumbnail_sizes=[300, 500]
        )
        self.assertEqual(str(account_plan), account_plan.name)

    def test_retrieving_account_plan_thumbnail_sizes(self):
        '''Test retrieving available thumbnail sizes for account plan
        and correct amount of thumbnail sizes'''
        account_plan = models.AccountPlan.objects.create(
            name='Coolplan',
            thumbnail_sizes=[300, 500, 678]
        )
        self.assertEqual(account_plan.thumbnail_sizes, [300, 500, 678])
        self.assertEqual(len(account_plan.thumbnail_sizes), 3)

    @patch('uuid.uuid4')
    def test_base_image_file_name_uuid(self, mock_uuid):
        '''Test that image is saved in the correct location'''
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.base_image_file_path(None, 'image.png')
        exp_path = f'uploads/images/{uuid}.png'

        self.assertEqual(file_path, exp_path)
