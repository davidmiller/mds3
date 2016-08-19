"""
Views for MDS3
"""
import collections

from django.shortcuts import redirect
from django.views.generic import TemplateView
from opal.models import Patient

from mds3.models import Demographics, Diagnosis

def get_opal_data(request):
    data = collections.defaultdict(dict)
    for k in request.POST.keys():
        if k.startswith('editing.'):
            if request.POST[k]:
                modelname, fieldname = k.replace('editing.', '').split('.')
                data[modelname][fieldname] = request.POST[k]
    return data

class IndexView(TemplateView):
    template_name = 'opal.html'

    def get_context_data(self, *args, **kwargs):
        context = super(TemplateView, self).get_context_data(*args, **kwargs)
        context['patients'] = Demographics.objects.all()
        return context


class RegisterView(TemplateView):
    template_name = 'register_form.html'

    def post(self, request, *args, **kwargs):
        data = get_opal_data(request)
        print 'OPAL Data:', data

        hospital_number = data['demographics']['hospital_number']

        if hospital_number:
            patient, created = Patient.objects.get_or_create(
                demographics__hospital_number=hospital_number)
            if created:
                patient.create_episode()
                demographics = patient.demographics_set.get()
                demographics.hospital_number = hospital_number
                demographics.save()
            else:
                patient = Patient.objects.create()
                patient.create_episode()

        patient.update_from_demographics_dict(data['demographics'], request.user)
        return redirect('/patients/{0}/comorbidity/'.format(patient.pk))

        context = self.get_context_data()
        return super(TemplateView, self).render_to_response(context)


class PatientComorbitityView(TemplateView):
    template_name = 'patient_comorbidity.html'

    def get_context_data(self, *args, **kwargs):
        context = super(TemplateView, self).get_context_data(*args, **kwargs)
        patient = Patient.objects.get(pk=kwargs['pk'])
        context['patient'] = patient
        context['demographics'] = patient.demographics_set.get()
        return context

    def post(self, request, *args, **kwargs):
        data = get_opal_data(request)
        print 'OPAL Data:', data
        patient = Patient.objects.get(pk=kwargs['pk'])

        data['diagnosis']['episode_id'] = patient.episode_set.first().id
        diagnosis = Diagnosis()
        diagnosis.update_from_dict(data['diagnosis'], request.user)

        return redirect('/')


class PatientDetailView(TemplateView):
    template_name = 'mds3/patient_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(TemplateView, self).get_context_data(*args, **kwargs)
        patient = Patient.objects.get(pk=kwargs['pk'])
        context['patient'] = patient
        context['demographics'] = patient.demographics_set.get()
        context['diagnoses'] = patient.episode_set.first().diagnosis_set.all()
        return context
