import requests

from django.utils.translation import ugettext_lazy as _

from temba.triggers.models import Trigger

from ...models import Channel, ChannelType
from .views import ClaimView


class VKType(ChannelType):
    """
    A VK channel
    """
    max_length = 320
    attachment_support = True
    free_sending = True
