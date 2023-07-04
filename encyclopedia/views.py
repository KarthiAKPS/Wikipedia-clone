from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from markdown2 import Markdown
import random

from . import util


def index(request):
    if request.method == "POST":
        query = request.POST['q']
        if query in util.list_entries():
            return render(request, "encyclopedia/content.html", {
                "content": convert_to_html(query),
                "title": query
            })
        else:
            l = util.list_entries()
            display = []
            for i in l:
                for j in query:
                    if j.lower() in i.lower():
                        if i not in display:
                            display.append(i)
            if display != []:
                return render(request, "encyclopedia/results.html", {
                    "entries": display,
                    "value":query
                })
            else:
                return render(request, "encyclopedia/error.html", {
                    "value": query,
                    "message": "does not exists"
                })
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })
    
def content(request, entry):
    if request.method == "POST":
        query = request.POST['q']
        if query in util.list_entries():
            return render(request, "encyclopedia/content.html", {
                "content": convert_to_html(query),
                "title": query
            })
        else:
            l = util.list_entries()
            display = []
            for i in l:
                for j in query:
                    if j.lower() in i.lower():
                        if i not in display:
                            display.append(i)
            if display != []:
                display = set(display)
                return render(request, "encyclopedia/results.html", {
                    "entries": display ,
                    "value" : query
                })
            else:
                return render(request, "encyclopedia/error.html", {
                    "value":query,
                    "message": "does not exists"
                })
                
    else:    
        if util.get_entry(entry):
            return render(request, "encyclopedia/content.html", {
                "content": convert_to_html(entry),
                "title" : entry
            })
        else:
            return render(request, "encyclopedia/error.html", {
                "value":entry,
                "message": "does not exists"
            })
        
def convert_to_html(title):
    content = util.get_entry(title)
    mark = Markdown()
    if content == None:
        return None
    else:
        return mark.convert(content)
        
class newform(forms.Form):
    title = forms.CharField(max_length=20, label='Title', widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(label="Content", widget=forms.Textarea(attrs={ 'class':'form-control', 'id':'exampleFormControlTextarea1', 'rows':'5'}))
        
def new(request):
    if request.method == 'POST':
        form = newform(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
        exists = util.get_entry(title)
        if exists != None:
            return render(request, "encyclopedia/error.html", {
                "value" : title,
                "message": "already exists"
            })
        else:
            util.save_entry(title, content)
            return render(request, "encyclopedia/content.html", {
                'title': title,
                'content': content
            })
    return render(request, "encyclopedia/new.html", {
        "form" : newform
    })
    
def edit(request):
    if request.method =="POST":
        title = request.POST['title']
        content = util.get_entry(title)
        form = newform()
        form.fields['title'].initial = title
        form.fields['content'].initial = content
        return render(request, "encyclopedia/edit.html", {
            "form" : form
        })
        
def save(request):
    if request.method == 'POST':
        form = newform(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            util.save_entry(title, content)
        return render(request, 'encyclopedia/content.html', {
            'title': title,
            'content': convert_to_html(title)
        })
        
def rand(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    url = '/{}'.format(random_entry)
    return HttpResponseRedirect(url)