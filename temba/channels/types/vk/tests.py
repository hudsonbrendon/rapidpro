from unittest.mock import patch

from django.test import override_settings
from django.urls import reverse

from temba.tests import MockResponse, TembaTest
from temba.triggers.models import Trigger
from temba.utils import json

from ...models import Channel


class VKTypeTest(TembaTest):
    def setUp(self):
        super().setUp()

        self.channel = Channel.create(
            self.org,
            self.user,
            None,
            "VK",
            name="VK Community",
            address="12345",
            role="SR",
            schemes=["vk"],
            config={
                "auth_token": "09876543",
                "community_name": "Vk Community",
                "secret": "203ijwijwij2ej2eii02ie0i2e2e",
                "callback_check_string": "12j323k",
            },
        )

    def test_claim(self):
        url = reverse("channels.types.vk.claim")

        self.login(self.admin)

        # check that claim page URL appears on claim list page
        response = self.client.get(reverse("channels.channel_claim"))
        self.assertContains(response, url)
