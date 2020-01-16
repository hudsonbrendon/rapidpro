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
                "callback_check_string": "12j323k"
            },
        )

    def test_claim(self):
        url = reverse("channels.types.vk.claim")

        self.login(self.admin)

        # check that claim page URL appears on claim list page
        response = self.client.get(reverse("channels.channel_claim"))
        self.assertContains(response, url)

        # can fetch the claim page
        response = self.client.get(url)

        token = "x" * 200

        post_data = response.context["form"].initial
        post_data["community_access_token"] = token
        post_data["community_id"] = "123456"
        post_data["community_name"] = "Temba"

        response = self.client.post(url, post_data, follow=True)

        # assert our channel got created
        channel = Channel.objects.get(address="123456")
        self.assertEqual(channel.config[Channel.CONFIG_AUTH_TOKEN], token)
        self.assertEqual(channel.config[Channel.CONFIG_COMMUNITY_NAME], "Temba")
        self.assertEqual(channel.address, "123456")
