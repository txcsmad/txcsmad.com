# Create your views here.

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, CreateView, FormView
from rest_framework import viewsets
import datetime
from mad_web.madcon.forms import MADconConfirmAttendanceForm, UserResumeInlineFormSet, MADconRegisterationForm, UserResumeForm
from rest_framework.permissions import IsAuthenticated

from mad_web.madcon.forms import MADconConfirmAttendanceForm
from mad_web.madcon.models import Registration, MADcon
from mad_web.madcon.serializers import RegistrationSerializer, MADconSerializer


class RegistrationView(View):

    def get(self, request, *args, **kwargs):
        user = self.request.user
        form = UserResumeForm(instance=user)
        user_resume_form = UserResumeInlineFormSet(instance=user)
        registration = None
        try:
            registration = Registration.objects.get(user=user)
        except Registration.DoesNotExist:
            registration = None
        if registration:
            user_resume_form[0].instance = registration
        
        return render(request, 'madcon/registration.html', {'form': form, 'user_resume_form': user_resume_form})

    def post(self, request, *args, **kwargs):
        user = self.request.user
        form = UserResumeForm(request.POST, request.FILES, instance=user)
        user_resume_form = None
        registration = None
        if form.is_valid():
            new_user_info = form.save()
            user_resume_form = UserResumeInlineFormSet(request.POST, request.FILES, instance = new_user_info)
            if user_resume_form.is_valid():
                new_registration_info = user_resume_form.save(commit=False)
                if len(new_registration_info) > 0:
                    new_registration_info[0].user = new_user_info
                    new_registration_info[0].madcon = MADcon.objects.get(date__year=datetime.datetime.now().year)
                    new_registration_info[0].status =  "P"
                    new_registration_info[0].save()                    
                    messages.add_message(self.request, messages.SUCCESS, 'Your registration was successful!')
                    return HttpResponseRedirect("/madcon")
        else:
            user_resume_form =  UserResumeInlineFormSet(request.POST, request.FILES, instance=user)       
        return render(request, 'madcon/registration.html', {'form': form, 'user_resume_form': user_resume_form})

    def get_context_data(self, **kwargs):
        context = super(RegistrationView, self).get_context_data(**kwargs)

        return context

    def get_success_url(self):
        return reverse('madcon:madcon')


class ConfirmAttendanceView(View):
    template_name = 'madcon/confirm.html'
    form_class = MADconConfirmAttendanceForm
    success_url = '/thanks/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.

        return super(RegistrationView, self).form_valid(form)


class MADconMainView(TemplateView):
    template_name = 'pages/madcon.html'

    def get_context_data(self, **kwargs):
        context = super(MADconMainView, self).get_context_data(**kwargs)
        user = self.request.user
        registration = None
        if user.is_authenticated:
            try:
                registration = Registration.objects.get(user=user)
            except Registration.DoesNotExist:
                registration = None
        context['registration'] = registration
        return context

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
