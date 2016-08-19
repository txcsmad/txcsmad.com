from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.views.generic.edit import FormView

from .forms import NotifyForm
from mad_web.utils.utils import OfficerRequiredMixin


class NotifyView(OfficerRequiredMixin, FormView):
    template_name = 'notify/notify_form.html'
    form_class = NotifyForm
    success_url = '/thanks/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super(NotifyView, self).form_valid(form)

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Notification successfully sent!')
        return reverse('notify:notify')
