from smartmin.views import SmartFormView

from django import forms
from django.utils.translation import ugettext_lazy as _

from ...models import Channel
from ...views import ClaimViewMixin


class ClaimView(ClaimViewMixin, SmartFormView):
    class Form(ClaimViewMixin.Form):
        community_access_token = forms.CharField(
            min_length=32, required=True, help_text=_("The Community Access Token")
        )
        community_name = forms.CharField(required=True, help_text=_("The name of the Community"))
        community_id = forms.IntegerField(required=True, help_text="The Community ID")
        verification_string = forms.CharField(required=True, help_text=_("The webhook verification string"))

    form_class = Form

    def form_valid(self, form):
        org = self.request.user.get_org()
        community_access_token = form.cleaned_data["community_access_token"]
        community_name = form.cleaned_data["community_name"]
        community_id = form.cleaned_data["community_id"]
        verification_string = form.cleaned_data["verification_string"]

        config = {
            Channel.CONFIG_AUTH_TOKEN: community_access_token,
            Channel.CONFIG_COMMUNITY_NAME: community_name,
            Channel.CONFIG_SECRET: Channel.generate_secret(length=50),
            Channel.CONFIG_VERIFICATION_STRING: verification_string,
        }
        self.object = Channel.create(
            org, self.request.user, None, self.channel_type, name=community_name, address=community_id, config=config
        )

        return super().form_valid(form)
