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

    form_class = Form

    def form_valid(self, form):
        org = self.request.user.get_org()
        auth_token = form.cleaned_data["community_access_token"]
        name = form.cleaned_data["community_name"]
        community_id = form.cleaned_data["community_id"]

        config = {
            Channel.CONFIG_AUTH_TOKEN: auth_token,
            Channel.CONFIG_PAGE_NAME: name,
            Channel.CONFIG_SECRET: Channel.generate_secret(length=50),
        }
        self.object = Channel.create(
            org, self.request.user, None, self.channel_type, name=name, address=community_id, config=config
        )

        return super().form_valid(form)
