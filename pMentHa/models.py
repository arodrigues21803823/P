from django.db import models
from django import forms


# Create your models here.
from django.http import JsonResponse


class Question(models.Model):
    multipla = models.BooleanField(default=False)
    category = models.TextField(max_length=1000)
    text = models.TextField(max_length=1000)
    explain = models.TextField(max_length=1000, blank=True)
    cover = models.TextField(max_length=100, blank=True)
    stimulus = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.text[:30]}"

class Comments(models.Model):
    clareza = models.IntegerField()
    pertinencia = models.IntegerField()
    help = models.CharField(max_length=10)
    original = models.CharField(max_length=10)

    def __str__(self):
        return f"ID:{self.id} - {self.clareza}, {self.pertinencia}, {self.help}, {self.original}"


class Option(models.Model):
    question = models.ForeignKey('Question', on_delete=models.SET_NULL, null=True)
    option = models.TextField(max_length=1000)
    order = models.IntegerField()

    def __str__(self):
        return f"{self.id} Question:{self.question.text}, option:{self.option}, order:{self.order}"


class QuestionOrder(models.Model):
    question = models.ForeignKey('Question', on_delete=models.SET_NULL, null=True)
    order = models.IntegerField()
    test = models.ForeignKey('Test', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Test:{self.test.name}, question:{self.question.text}, order:{self.order}"


class Test(models.Model):
    name = models.CharField(max_length=64)
    statement = models.TextField(max_length=1000)
    questions = models.ManyToManyField('Question', blank=True, related_name="questions")
    advisor = models.ForeignKey('Advisor', on_delete=models.SET_NULL, null=True, related_name="advisor")

    def __str__(self):
        return f"Teste {self.name}"


class Answer(models.Model):
    text = models.TextField(max_length=258)
    quotation = models.CharField(max_length=64, blank=True, null=True)
    question = models.ForeignKey('Question', on_delete=models.SET_NULL, null=True, related_name="respostas")
    resolution = models.ForeignKey('Resolution', on_delete=models.SET_NULL, null=True, related_name="resolution")

    def __str__(self):
        return f"quest="


class Advisor(models.Model):
    name = models.CharField(max_length=64)
    email = models.CharField(max_length=254, blank=True)

    def __str__(self):
        return f"{self.name}"


class Patient(models.Model):
    name = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    gender = models.CharField(max_length=64)
    nacionality = models.CharField(max_length=64)
    date = models.DateField()
    disease = models.CharField(max_length=64)
    disease2 = models.TextField(max_length=258, blank=True)
    number = models.IntegerField()
    tests = models.ManyToManyField('Test', blank=True, related_name="tests")
    resolutions = models.ManyToManyField('Resolution', blank=True, related_name="resolutions")

    def __str__(self):
        return f"{self.name}"


class Resolution(models.Model):
    patient = models.ForeignKey('Patient', on_delete=models.SET_NULL, null=True, related_name="patient")
    test = models.ForeignKey('Test', on_delete=models.SET_NULL, null=True, related_name="test")

    def __str__(self):
        return f"{self.id}, {self.patient}, {self.test}"


class Report(models.Model):
    resolution = models.ForeignKey('Resolution', on_delete=models.SET_NULL, null=True)
    advisor = models.ForeignKey('Advisor', on_delete=models.SET_NULL, null=True)
    text = models.TextField(max_length=1000)

    def __str__(self):
        return f"Relatório do teste {self.resolution.test}: {self.text}"


class Contact(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=128)
    contact = models.IntegerField()
    birth = models.DateField()

    def __str__(self):
        return f"{self.name}"


def criaTabelaTestes():
    testes = []
    for patient in Patient.objects.all():

        dicPatient = {"name": patient.name, "id": patient.id}
        doneTests = []
        for test in patient.tests.all():
            doneTests.append(test.id)
        dicPatient["doneTests"] = doneTests

        if len(doneTests) < 5:
            dicPatient["nextTest"] = [len(doneTests) + 1]

        toDoTests = []
        if len(doneTests) < 5:
            for i in range(len(doneTests) + 2, 5 + 1):
                toDoTests.append(i)
        dicPatient["toDoTests"] = toDoTests
        testes.append(dicPatient)

    return testes


def criaTabelaTeste(patientID):
    testes = []
    patient = Patient.objects.get(pk=patientID)
    dicPatient = {"name": patient.name, "id": patient.id}
    doneTests = []
    for test in patient.tests.all():
        doneTests.append(test.id)
    dicPatient["doneTests"] = doneTests

    if len(doneTests) < 5:
        dicPatient["nextTest"] = [len(doneTests) + 1]
    toDoTests = []
    if len(doneTests) < 5:
        for i in range(len(doneTests) + 2, 5 + 1):
            toDoTests.append(i)
    dicPatient["toDoTests"] = toDoTests
    testes.append(dicPatient)

    return testes


def proximaPergunta(testID, questionID):
    sequenciaDeQuestionIDPorTeste = {}
    test = Test.objects.get(pk=testID)
    sequenciaDeQuestionIDPorTeste[testID] = []
    for question in test.questions.all():
        sequenciaDeQuestionIDPorTeste[testID].append(question.id)
    else:
        i = sequenciaDeQuestionIDPorTeste[testID].index(questionID)
        if i == len(sequenciaDeQuestionIDPorTeste[testID]) - 1:
            # foi a ultima pergunta do teste
            return -1
        else:
            return sequenciaDeQuestionIDPorTeste[testID][i + 1]


def addTest(testID, patientID):
    patient = Patient.objects.get(pk=patientID)
    test = Test.objects.get(pk=testID)
    newPatient = patient.tests.add(test)

    return newPatient


def questionsAwnsers(resolutionID, testID):
    anwsers = Answer.objects.filter(resolution=resolutionID)
    order = 0
    count = 0
    dicpergunta = {}
    test = len(Test.questions.filter(pk=testID))
    while count < len(test):
        question = QuestionOrder.objects.get(order=order + 1, test=testID)
        answer = Answer.objects.get(resolution=resolutionID, question=question)
        dicpergunta[question.question] = answer.text
        order += 1
        count += 1

    print(list)
    return list


def report_exists(resolutionID):
    report = Report.objects.filter(resolution=resolutionID)
    return report


def resolution_exists(patientID, testID):
    resolution = Resolution.objects.filter(patient=patientID, test=testID)
    if resolution:
        return True
    else:
        return False

def create_api():
    dicPatient = {}
    testes = {"1": [], "2": [], "3": [], "4": [], "5": []}
    for patient in Patient.objects.all():
        teste = 0
        for test in patient.tests.all():
            teste = teste + 1
            if test.id == teste:
                dicPatient = {"name": patient.name, "gender": patient.gender, "date": patient.date, "number": patient.number}

        testes[f"{teste}"].append(dicPatient)

    return JsonResponse(testes)
