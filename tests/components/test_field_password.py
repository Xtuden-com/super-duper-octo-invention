from django import forms
from django.test import override_settings
from django.urls import path
from django.views.generic import FormView
from viewflow.urls import Application, Site

from . import LiveTestCase


@override_settings(ROOT_URLCONF=__name__)
class Test(LiveTestCase):
    def test_field_input(self):
        self.browser.get(f"{self.live_server_url}/application/form/")
        self.assertNoJsErrors()

        input = self.browser.find_element_by_css_selector('vf-field-password input')
        label = self.browser.find_element_by_css_selector('vf-field-password label')
        label_classes = label.get_attribute('class').split(' ')
        self.assertNotIn('mdc-text-field--float-above', label_classes)

        input.click()
        label_classes = label.get_attribute('class').split(' ')
        self.assertIn('mdc-text-field--focused', label_classes)
        self.assertIn('mdc-text-field--label-floating', label_classes)
        self.assertNoJsErrors()


class TestForm(forms.Form):
    field = forms.CharField(widget=forms.PasswordInput)


urlpatterns = [
    path('', Site(items=[
        Application(
            title='Test Application',
            urls=[
                path('form/', FormView.as_view(form_class=TestForm, template_name='tests/components.html'))
            ]
        ),
    ]).urls)
]
