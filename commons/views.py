from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from datetime import datetime, timedelta, timezone
from commons.models import *
from io import BytesIO

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import inch

import random
import string
# Create your views here.
def home(request):
    animals = Animal.objects.all()
    return render(request,'index.html',locals())

def animals(request):
    animals = Animal.objects.all()
    return render(request,'animales.html',locals())

def quiz(request, quiz_id=None):
    if quiz_id is None:
        print("no id")
        quiz = Quiz(quid=id_generator(), expires_at=datetime.now()+timedelta(minutes=30))
        quiz.save()
        question_id_list = list(Question.objects.values_list('id', flat=True))
        question_id_list = random.sample(question_id_list,10)
        random.shuffle(question_id_list)
        questions = Question.objects.filter(id__in=question_id_list)
        for q in questions:
            quiz.questions.add(q)
        url = '/quiz/'+quiz.quid
        return HttpResponseRedirect(url)

    quiz = None
    if Quiz.objects.filter(quid=quiz_id, active=True).exists():
        quiz = Quiz.objects.get(quid=quiz_id, active=True)
        if (quiz.expires_at - datetime.now(timezone.utc)).total_seconds() >= 1800:
            quiz.active = False
            quiz.save()
            return HttpResponseRedirect('/quiz')
    else:
        return HttpResponseRedirect('/quiz')
    
    if request.POST:
        answer_id_list = []
        quiz.active=False
        quiz.save()
        for x in range(0,10):
            answer_id_list.append(request.POST.get("answers_"+str(x),None))
        print(answer_id_list)
        correct_answers = Answer.objects.filter(id__in=answer_id_list, is_correct=True).count()
        if correct_answers >= 7:
            validation_id = id_generator()
            request.session['name'] = request.POST.get('name')
            request.session['certificate_id'] = validation_id
            return HttpResponseRedirect('/certificate/'+validation_id)
        else:
            return HttpResponseRedirect('/failure')

    return render(request,'quiz.html',locals())

def failure(request):
    return render(request,'failure.html')

def certificate(request, validation_id=None):
    if validation_id is None:
        return HttpResponseRedirect('/quiz')
    certificate_id = request.session.get('certificate_id', None)
    if certificate_id != validation_id:
        return HttpResponseRedirect('/quiz')
    name = request.session.get('name', '')
    if request.POST:
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=landscape(letter))
        width, height = landscape(letter)
        c.setFont("Helvetica", 25)
        c.drawImage('template.png',0,0,width=width,height=height )
        c.drawCentredString(width/2,height/2,name)
        c.save()
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Certificado.pdf"'
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response
    return render(request,'certificado.html', locals())


    
#-------------------------------------------------------------------
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))