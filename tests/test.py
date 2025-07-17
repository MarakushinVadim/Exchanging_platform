from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from ads.models import Ad, ExchangeProposal


class AdTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test_user', email='test_user@mail.ru', password='testPassword21')
        self.obj = Ad.objects.create(
            user=self.user, title='test_title', description='test_description',
            category='test_category'
        )


    def test_list_view(self):
        response = self.client.get(reverse('ads:ad_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test_title')

    def test_detail_view(self):
        self.client.login(username='test_user', password='testPassword21')
        response = self.client.get(reverse('ads:ad_detail', args=[self.obj.pk], ))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test_title')

    def test_update_view(self):
        self.client.login(username='test_user', password='testPassword21')

        response = self.client.get(reverse('ads:ad_update', args=[self.obj.pk]))
        self.assertEqual(response.status_code, 200)

        update_data = {
            'title': 'updated_title',
            'description': self.obj.description,
            'category': self.obj.category,
            'condition': self.obj.condition
        }

        response = self.client.post(
            reverse('ads:ad_update', args=[self.obj.pk]), update_data
        )
        self.assertEqual(response.status_code, 302)
        self.obj.refresh_from_db()
        self.assertEqual(self.obj.title, 'updated_title')

    def test_create_view(self):
        self.client.login(username='test_user', password='testPassword21')

        response = self.client.get(reverse('ads:ad_create'))
        self.assertEqual(response.status_code, 200)

        data = {
            'title': 'test_create_title',
            'description': 'test_create_description',
            'category': 'test_create_category',
            'condition': Ad.ConditionChoices.NEW,
        }

        response = self.client.post(reverse('ads:ad_create'), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Ad.objects.count(), 2)

    def test_delete_view(self):
        self.client.login(username='test_user', password='testPassword21')
        initial_count = Ad.objects.count()

        response = self.client.post(reverse('ads:ad_delete', args=[self.obj.pk]))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Ad.objects.count(), initial_count - 1)

        with self.assertRaises(Ad.DoesNotExist):
            Ad.objects.get(pk=self.obj.pk)

    def test_delete_unauthorized(self):
        self.client.logout()

        response = self.client.post(reverse('ads:ad_delete', args=[self.obj.pk]))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Ad.objects.count(), 1)

class ExchangeProposalTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_1 = User.objects.create_user(username='test_1_user', email='test_1_user@mail.ru',
                                               password='testPassword21')
        self.user_2 = User.objects.create_user(username='test_2_user', email='test_2_user@mail.ru',
                                               password='testPassword22')
        self.obj_1 = Ad.objects.create(
            user=self.user_1, title='test_title', description='test_description',
            category='test_category'
        )
        self.obj_2 = Ad.objects.create(
            user=self.user_2, title='test_2_title', description='test_2_description',
            category='test_2_category'
        )
        data = {
            'ad_sender': self.obj_1,
            'ad_receiver': self.obj_2,
            'comment': 'any comment',
            'status': ExchangeProposal.ExchangeChoices.AWAITS
        }
        self.client.login(username='test_1_user', password='testPassword21')
        self.object = ExchangeProposal.objects.create(**data)

    def test_create_view(self):
        self.client.login(username='test_1_user', password='testPassword21')
        data = {
            'ad_sender': self.obj_1.pk,
            'ad_receiver': self.obj_2.pk,
            'comment': 'any comment',
            'status': ExchangeProposal.ExchangeChoices.AWAITS
        }
        response = self.client.post(reverse('ads:exchange_proposal_create', args=[self.obj_2.pk]), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ExchangeProposal.objects.count(), 2)

    def test_list_view(self):
        self.client.login(username='test_1_user', password='testPassword21')
        response = self.client.get(reverse('ads:exchange_proposal_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ExchangeProposal.objects.count(), 1)

    def test_accept_proposal(self):
        self.client.login(username='test_2_user', password='testPassword22')
        response = self.client.post(reverse('ads:accept_proposal', args=[self.object.pk]))
        self.object.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.object.status, ExchangeProposal.ExchangeChoices.TAKEN)

    def test_reject_proposal(self):
        self.client.login(username='test_2_user', password='testPassword22')
        response = self.client.post(reverse('ads:reject_proposal', args=[self.object.pk]))
        self.object.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.object.status, ExchangeProposal.ExchangeChoices.REJECTED)
