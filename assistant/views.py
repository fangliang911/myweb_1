# importing render and redirect
from django.shortcuts import render, redirect
# importing the openai API
import openai
from prompt.models import Prompt_manage
from lawpoint.models import Lawpoint
# import the generated API key from the secret_key file
from .secret_key import API_KEY
# loading the API key from the secret_key file
openai.api_key = API_KEY


# this is the home view for handling home page logic
def home(request):
    try:
        # if the session does not have a messages key, create one
        if 'messages' not in request.session:
            request.session['messages'] = [
                {"role": "system", "content": "输入想学习的实体法、程序法，让我们开始吧"},
            ]
        if request.method == 'POST':
            # get the prompt from the form
            learn = request.POST.get('prompt')
            if not learn.encode().isalpha():
                prompt_template = Prompt_manage.objects.filter(prompt_type="法律情境").order_by('?').first().prompt_template
                prompt = generate(prompt_template, learn)
            else:
                prompt = learn
            # get the temperature from the form
            temperature = float(request.POST.get('temperature', 0.1))
            # append the prompt to the messages list
            request.session['messages'].append({"role": "user", "content": prompt})
            # set the session as modified
            request.session.modified = True
            # call the openai API
            response = openai.ChatCompletion.create(
                 model="gpt-3.5-turbo",
                 messages=request.session['messages'],
                 temperature=temperature,
                 max_tokens=1000,
             )
            # format the response
            formatted_response = response['choices'][0]['message']['content']
            # append the response to the messages list
            request.session['messages'].append({"role": "assistant", "content": formatted_response})
            request.session.modified = True
            # redirect to the home page
            context = {
                'messages': request.session['messages'],
                'prompt': '',
                'temperature': temperature,
            }
            return render(request, 'assistant/home.html', context)
        else:
            # if the request is not a POST request, render the home page
            context = {
                'messages': request.session['messages'],
                'prompt': '',
                'temperature': 0.8,
            }
            return render(request, 'assistant/home.html', context)
    except Exception as e:
        print(e)
        # if there is an error, redirect to the error handler
        return redirect('error_handler')


def new_chat(request):
    # clear the messages list
    request.session.pop('messages', None)
    if request.method == 'POST':
        prompt = request.POST.get('prompt_template')
    return redirect('home')


# this is the view for handling errors
def error_handler(request):
    return render(request, 'assistant/404.html')


def generate(prompt_template, learn):
    try:
        law_name = Lawpoint.objects.filter(law_name=learn).order_by('?').first().law_name
    except Exception as e:
        law_name = Lawpoint.objects.order_by('?').first().law_name

    law_points = Lawpoint.objects.filter(law_name=law_name).order_by('?')[:3]
    law_point = ""
    for point in law_points:
        law_point = law_point + point.law_point+ ","

    role = Prompt_manage.objects.filter(prompt_type="情境角色").order_by('?').first().prompt_template

    prompt_template = prompt_template.replace("{法律名称}", law_name)
    prompt_template = prompt_template.replace("{法律考点}", law_point)
    prompt_template = prompt_template.replace("{情境角色}", role)

    return prompt_template

