def fazPergunta(request, resolutionID, questionID):
    if request.method == "POST":
        quotation = 0
        answer = Answer.objects.filter(question=questionID, resolution=resolutionID)
        if answer:
            # apenas altera a resposta
            answer = Answer.objects.get(question=questionID, resolution=resolutionID)
            answer.text = request.POST["resposta"]
            answer.save()
        else:
            answer = Answer.objects.create(
                text=request.POST["resposta"],
                quotation=quotation,
                question=Question.objects.get(pk=questionID),
                resolution=Resolution.objects.get(pk=resolutionID),
            )
            answer.save()
        testID = Resolution.objects.get(pk=resolutionID).test.id
        questionCount = len(QuestionOrder.objects.filter(test=testID))
        order = QuestionOrder.objects.get(test=testID, question=questionID).order

        if order < questionCount:
            question = QuestionOrder.objects.get(test=testID, order=order + 1).question
        else:
            # Teste Finalizado, regressar a tabela geral
            patientID = Resolution.objects.get(pk=resolutionID).patient.id
            addTest(testID, patientID)
            return redirect('patientoverview')
        answer = Answer.objects.filter(question=question.id, resolution=resolutionID)
        options = Option.objects.filter(question=question.id)


        context = {
                    "question": question,
                    "resolutionID": resolutionID,  # permite identificar patient e test
                    "options": options,
                    "order": order + 1,
                    "test": Resolution.objects.get(pk=resolutionID).test.name
                }

        if question.cover:
            context["image"] = question.cover

        if question.multipla:
            context["options"]=options
            if answer:
                context["answer"] = int(Answer.objects.get(question=question.id, resolution=resolutionID).text)
        elif answer:
            context["answer"] = Answer.objects.get(question=question.id, resolution=resolutionID).text

        if question.multipla:
            return render(request, "pMentHa/perguntas/multipla.html", context)
        else:
            return render(request, "pMentHa/perguntas/desenvolvimento.html", context)
