# Create your views here.

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, CreateView, FormView, ListView
from rest_framework import viewsets
import datetime
import itertools

from mad_web.madcon.forms import MADconConfirmAttendanceForm, UserResumeInlineFormSet, MADconRegisterationForm, UserResumeForm, MADconConfirmAttendanceForm
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from mad_web.madcon.forms import MADconConfirmAttendanceForm
from mad_web.madcon.models import Registration, MADcon
from mad_web.events.models import Event, EventTag
from rest_framework.exceptions import NotFound
from mad_web.madcon.serializers import RegistrationSerializer, MADconSerializer, RegistrationUserSerializier

def current_madcon():
    return MADcon.objects.get(date__year=datetime.datetime.now().year)

class RegistrationView(View):
    def get(self, request, *args, **kwargs):
        user = self.request.user
        form = UserResumeForm(instance=user)
        user_resume_form = UserResumeInlineFormSet(instance=user)
        registration = None
        try:
            registration = Registration.objects.get(user=user, madcon=current_madcon())
        except Registration.DoesNotExist:
            registration = None
        if registration:
            user_resume_form[0].instance = registration

        return render(request, 'madcon/registration.html',
                      {'form': form, 'user_resume_form': user_resume_form})

    def post(self, request, *args, **kwargs):
        user = self.request.user
        form = UserResumeForm(request.POST, request.FILES, instance=user)
        user_resume_form = None
        registration = None
        if form.is_valid():
            new_user_info = form.save()
            user_resume_form = UserResumeInlineFormSet(request.POST, request.FILES,
                                                       instance=new_user_info)
            if user_resume_form.is_valid():
                new_registration_info = user_resume_form.save(commit=False)
                if len(new_registration_info) > 0:
                    new_registration_info[0].user = new_user_info
                    new_registration_info[0].madcon = current_madcon()
                    new_registration_info[0].status = "P"
                    new_registration_info[0].save()
                    messages.add_message(self.request, messages.SUCCESS,
                                         'Your registration was successful!')
                    return HttpResponseRedirect("/madcon")
        else:
            user_resume_form = UserResumeInlineFormSet(request.POST, request.FILES, instance=user)
        return render(request, 'madcon/registration.html',
                      {'form': form, 'user_resume_form': user_resume_form})

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
                registration = Registration.objects.get(user=user, madcon=current_madcon())
            except Registration.DoesNotExist:
                registration = None
        context['registration'] = registration
        return context


class RegistrationStatusView(FormView):
    template_name = 'madcon/status.html'
    form_class = MADconConfirmAttendanceForm
    success_url = '/thanks/'

    def get_context_data(self, **kwargs):
        context = super(RegistrationStatusView, self).get_context_data(**kwargs)
        user = self.request.user
        registration = None
        try:
            registration = Registration.objects.get(user=user, madcon=current_madcon())
        except Registration.DoesNotExist:
            registration = None
        context['registration'] = registration
        return context

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.confirm_attendance()
        return super(RegistrationStatusView, self).form_valid(form)

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Confirmed!')
        return reverse('madcon:status')


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
        return Registration.objects.filter(user=user, madcon=current_madcon())

class ScheduleListView(View):

    def get(self, request, *args, **kwargs):
        queryset = None
        current_madcon = None
        madcon_tag = None
        try:
            current_madcon = MADcon.objects.get(date__year=datetime.datetime.now().year)
            madcon_tag = EventTag.objects.get(pk=4)
        except (MADcon.DoesNotExist, EventTag.DoesNotExist):
            return render(request, 'madcon/schedule.html', {'event_list': []})        
        queryset = Event.objects.filter(start_time__year=current_madcon.date.year, start_time__month=current_madcon.date.month, start_time__day=current_madcon.date.day, event_tags=madcon_tag).order_by('start_time')
        slots = itertools.groupby(queryset, lambda x:self.get_date_hour(x.start_time))
        schedule_slots = []
        for group,matches in slots:
            slot = ScheduleSlot(matches, group)
            schedule_slots.append(slot)
        return render(request, 'madcon/schedule.html', {'event_list': queryset, 'slots': schedule_slots, 'madcon':current_madcon})

    def get_date_hour(self, timestamp):
        return timestamp.strftime("%x %H")

class ScheduleSlot:
    def __init__(self, events, time):
        self.events = list(events)

class RegistrationViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAdminUser,)
    queryset = Registration.objects.all()
    serializer_class = RegistrationUserSerializier
    pagination_class = None

    def get_queryset(self):
        queryset = Registration.objects.all()
        status = self.request.query_params.get('status', None)
        status_choices = dict(Registration.APPLICATION_STATUS_CHOICES)
        if status is not None:
            if not (status in status_choices):
                raise NotFound("Status option is not valid")
            queryset = queryset.filter(status=status)
        return queryset
