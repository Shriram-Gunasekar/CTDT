from . import db
from .models import Account
from . import qamodel
from . import summarymodel
from . import semsimmodel
from flask_login import login_required, current_user
from flask import Blueprint, render_template, request, flash, redirect, url_for
from sentence_transformers import util

views = Blueprint('views', __name__, url_defaults=None, root_path=None ) #template_folder not specified

@views.route('/', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@views.route('/plagsim', methods=['GET','POST'])
@login_required
def plagsim():
    if request.method == 'POST':
        theirplagtext = request.form.get('theirplagtext')
        checkplagtext = request.form.get('checkplagtext')
        if theirplagtext and checkplagtext:
            simscore = plagresult(theirplagtext,checkplagtext)
            simscore = round(simscore.item()*100, 2)
            #simscore = simscore * 100
            #simscore = round(simscore, 2)
        else:
            simscore = "Enter Valid Inputs"
        return render_template('plagsim.html', user=current_user, simscore=simscore)
    return render_template('plagsim.html', user=current_user, simscore="")

@views.route('/bertsum', methods=['GET','POST'])
@login_required
def bertsum():
    if request.method == 'POST':
        theirsumtext = request.form.get('theirsumtext')
        textsentences = request.form.get('textsentences')
        if theirsumtext:
            textsummary = summarizer(theirsumtext,sentences=textsentences)
        else:
            textsummary = "Please Enter Valid Input"
        return render_template('bertsum.html', user=current_user,textsummary=textsummary)
    return render_template('bertsum.html',user=current_user,textsummary="")

@views.route('/qa', methods=['GET','POST'])
@login_required
def qa():
    if request.method == 'POST':
        theirqatext = request.form.get('theirqatext')
        theirqas = request.form.get('theirqas')
        if theirqatext and theirqas:
            answers = qaanswers(theirqatext, theirqas.split(';'))
            #answers = "".join(i for i in answers)
        else:
            answers = "Inputs are not valid. Please Enter Q's separates by semicolons for your text data"
        return render_template('qa.html',user=current_user, answers=answers)
    return render_template('qa.html',user=current_user,answers="")

@views.route('/eval',methods=['GET','POST']) 
@login_required
def eval():
    return render_template('eval.html',user=current_user)

def qaanswers(theirqatext, theirqas):
    answers = []
    for i in theirqas:
        answers.append(qamodel({'context':theirqatext,'question': i})['answer'])
    print(answers)
    return answers

def plagresult(text1,text2):
    text1_representation = semsimmodel.encode(text1)
    text2_representation = semsimmodel.encode(text2)
    cosine_sim = util.pytorch_cos_sim(text1_representation,text2_representation)   
    return cosine_sim 

def summarizer(data,sentences):
    answer = summarymodel(data, num_sentences=int(sentences), min_length=5)
    return answer

