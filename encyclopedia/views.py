from re import M

from django.shortcuts import render
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect

from . import util
from markdown2 import Markdown
from random import choice


class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'class' : 'form-control col-md-8 col-lg-8', 'rows' : 1}))
    content = forms.CharField(label="Content", widget=forms.Textarea(attrs={'class' : 'form-control col-md-8 col-lg-8', 'rows' : 10}))


class EditEntryForm(forms.Form):
    title = forms.CharField(label="Entry Title", widget=forms.TextInput(attrs={'class' : 'form-control col-md-8 col-lg-8', 'rows': 1}))
    content = forms.CharField(label="Edit Content", widget=forms.Textarea(attrs={'class' : 'form-control col-md-8 col-lg-8', 'rows' : 10}))
    edit = forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    markdowner = Markdown()
    entry_page = util.get_entry(title)
    if entry_page is None:
        return render(request, "encyclopedia/error.html", {
            "entry_title": title
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry": markdowner.convert(entry_page),
            "entry_title": title
        })


def search(request):
    value = request.GET.get('q','')
    if(util.get_entry(value) is not None):
        return HttpResponseRedirect(reverse("entry", kwargs={'title': value}))
    else:
        subStringEntries = []
        for entry in util.list_entries():
            if value.upper() in entry.upper():
                subStringEntries.append(entry)
        
        return render(request, "encyclopedia/index.html", {
            "entries": subStringEntries,
            "search": True, 
            "value": value
        })


def new(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if(util.get_entry(title) is None):
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("entry", kwargs={'title': title}))
            else:
                return render(request, "encyclopedia/new.html", {
                    "form": form,
                    "existing": True,
                    "title": title
                })
        else:
            return render(request, "encyclopedia/new.html", {
                "form": form,
                "existing": False
            })
    else:
        return render(request, "encyclopedia/new.html", {
            "form": NewEntryForm(),
            "existing": False
        })


def edit(request, title):
    if request.method == "GET":
        entry_page = util.get_entry(title)

        if entry_page == None:
            return render(request, "encyclopedia/error.html", {
                "entry_title": title
            })
        else:
            return render(request, "encyclopedia/edit.html", {
                "title": title,
                "form": EditEntryForm(initial={"content": entry_page})
            })
    
    elif request.method == "POST":
        form = EditEntryForm(request.POST)

        if form.is_valid():
            content = form.cleaned_data['content']
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("entry", kwargs={"title": title}))

        else:
            return render(request, "encyclopedia/error.html", {
                "entry_title": title
            })


def random(request):
    entries = util.list_entries()
    random_entry = choice(entries)
    return HttpResponseRedirect(reverse("entry", kwargs={'title': random_entry}))

