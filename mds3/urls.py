from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from opal.urls import urlpatterns as opatterns

from mds3 import views

urlpatterns = patterns(
    '',
    url(r'^$', views.IndexView.as_view()),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^register/$', views.RegisterView.as_view()),
    url(r'^patients/(?P<pk>\d+)/comorbidity/$', views.PatientComorbitityView.as_view()),
    url(r'^patient/(?P<pk>\d+)/$', views.PatientDetailView.as_view()),
)

urlpatterns += opatterns
