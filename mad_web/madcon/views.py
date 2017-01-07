# Create your views here.
import datetime

from django.contrib import messages
from django.urls import reverse
from django.views.generic import DetailView
from django.views.generic import FormView

from mad_web.madcon.forms import MADconApplicationForm, MADconConfirmAttendanceForm
from mad_web.madcon.models import MADconApplication, MADcon


class MADconApplicationView(FormView):
    template_name = 'madcon/application.html'
    form_class = MADconApplicationForm
    success_url = '/thanks/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.

        most_recent_madcon = MADcon.objects.get(date__year=datetime.datetime.now().year)
        return super(MADconApplicationView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(MADconApplicationView, self).get_context_data(**kwargs)

        return context

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Confirmed!')
        return reverse('madcon')


class MADconConfirmAttendanceView(FormView):
    template_name = 'madcon/confirm.html'
    form_class = MADconConfirmAttendanceForm
    success_url = '/thanks/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.

        return super(MADconApplicationView, self).form_valid(form)


class MADconApplicationStatusView(DetailView):
    model = MADconApplication
    slug_field = id
