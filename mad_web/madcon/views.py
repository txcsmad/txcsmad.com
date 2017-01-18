# Create your views here.

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from mad_web.madcon.forms import MADconApplicationForm, MADconConfirmAttendanceForm
from mad_web.madcon.models import Registration, MADcon
from mad_web.madcon.serializers import RegistrationSerializer, MADconSerializer


class RegistrationView(View):
    def get(self, request, *args, **kwargs):
        form = MADconApplicationForm(request=request)

        return render(request, 'madcon/registration.html', {'form': form})

    def post(self, request, *args, **kwargs):
        # create a form instance and populate it with data from the request:
        form = MADconApplicationForm(request.POST, request.FILES, request=request)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            form.register_for_madcon()
            # redirect to a new URL:
            messages.add_message(self.request, messages.SUCCESS, 'Your registration was successful!')
            return HttpResponseRedirect("/madcon")
        return render(request, 'madcon/registration.html', {'form': form})

    def get_context_data(self, **kwargs):
        context = super(RegistrationView, self).get_context_data(**kwargs)

        return context

    def get_success_url(self):
        return reverse('madcon')


class ConfirmAttendanceView(View):
    template_name = 'madcon/confirm.html'
    form_class = MADconConfirmAttendanceForm
    success_url = '/thanks/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.

        return super(RegistrationView, self).form_valid(form)


class RegistrationStatusView(TemplateView):
    model = Registration
    template_name = 'madcon/status.html'

    def get_context_data(self, **kwargs):
        context = super(RegistrationStatusView, self).get_context_data(**kwargs)
        user = self.request.user
        registration = None
        try:
            registration = Registration.objects.get(user=user)
        except Registration.DoesNotExist:
            registration = None
        context['registration'] = registration
        return context


class MADconViewSet(viewsets.ModelViewSet):
    queryset = MADcon.objects.all()
    serializer_class = MADconSerializer


class MyRegistrationViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        return Registration.objects.filter(user=user)
