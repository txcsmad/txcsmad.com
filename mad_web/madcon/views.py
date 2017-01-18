# Create your views here.
import datetime

from django.contrib import messages
from django.urls import reverse
from django.views.generic import FormView
from django.views.generic import TemplateView

from mad_web.madcon.forms import MADconApplicationForm, MADconConfirmAttendanceForm
from mad_web.madcon.models import MADconApplication, MADcon


class MADconRegistrationView(FormView):
    template_name = 'madcon/registration.html'
    form_class = MADconApplicationForm
    success_url = '/thanks/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.

        most_recent_madcon = MADcon.objects.get(date__year=datetime.datetime.now().year)
        return super(MADconRegistrationView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(MADconRegistrationView, self).get_context_data(**kwargs)

        return context

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Your registration was successful!')
        return reverse('madcon:madcon')


class MADconConfirmAttendanceView(FormView):
    template_name = 'madcon/confirm.html'
    form_class = MADconConfirmAttendanceForm
    success_url = '/thanks/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.

        return super(MADconRegistrationView, self).form_valid(form)


class MADconMainView(TemplateView):
    template_name = 'pages/madcon.html'

    def get_context_data(self, **kwargs):
        context = super(MADconMainView, self).get_context_data(**kwargs)
        user = self.request.user
        registration = None
        if user.is_authenticated:
            try:
                registration = MADconApplication.objects.get(user=user)
            except MADconApplication.DoesNotExist:
                registration = None
        context['registration'] = registration
        return context



class MADconRegistrationStatusView(TemplateView):
    model = MADconApplication
    template_name = 'madcon/status.html'

    def get_context_data(self, **kwargs):
        context = super(MADconRegistrationStatusView, self).get_context_data(**kwargs)
        user = self.request.user
        registration = None
        try:
            registration = MADconApplication.objects.get(user=user)
        except MADconApplication.DoesNotExist:
            registration = None
        context['registration'] = registration
        return context
