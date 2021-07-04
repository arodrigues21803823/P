from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path("", views.index, name="index"),

    path("patientoverview", views.patientoverview, name="patientoverview"),
    path("mentha-care", views.mentha_care, name="mentha-care"),
    path("register", views.register, name="register"),
    path("Registo", views.regPatient, name="regPatient"),
    path("about", views.about, name="about"),
    path("Teste<int:testID>-Paciente<int:patientID>", views.fazPrimeiraPergunta, name="fazPrimeiraPergunta"),
    path("Resolucao<int:resolutionID>-Questao<int:questionID>", views.fazPergunta, name="fazPergunta"),
    path("Report<int:testID>-<int:patientID>", views.firstReportQuestion, name="firstReportQuestion"),
    path("Report<int:resolutionID>--Questao<int:questionID>", views.reportnextQuestion, name="reportnextQuestion"),
    path("Report<int:resolutionID>---Questao<int:questionID>", views.reportPrevQuestion, name="reportPrevQuestion"),
    path("contacts", views.contact, name="contact"),
    path("comments", views.comments, name="comments"),
    path("patient-summary<int:patientID>", views.patient_summary, name="patientSummary"),
    path("contactList", views.contacts_list, name="contactList"),
    path("velhotes", views.velhotes, name="velhotes"),
    path("api", views.api, name="api"),
    #Django Auth

    path("login_", views.login_, name="login_"),
    path("logout_", views.logout_, name="logout_")
]

