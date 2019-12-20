from django.core.urlresolvers import reverse
from django.urls import resolve
from django.test import TestCase
from ..views import view_cabs

from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User

# Create your tests here.
class view_cabsTests(TestCase):
    def test_view_cabs_view_status_code(self):
        url = reverse('view_cabs')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_view_cabs_url_resolves_view_cabs_view(self):
        view = resolve('/view_cabs/')
        self.assertEquals(view.func, view_cabs)
    
    # def test_user_not_logged_in_page_contains_login_options(self):
