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


def entry(request, entry):
    markdowner = Markdown()
    entryPage = util.get_entry(entry)
    if entryPage is None:
        return render(request, "encyclopedia/error.html", {
            "entryTitle": entry
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry": markdowner.convert(entryPage),
            "entryTitle": entry
        })


def search(request):
    value = request.GET.get('q','')
    if(util.get_entry(value) is not None):
        return HttpResponseRedirect(reverse("entry", kwargs={'entry': value}))
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
            if(util.get_entry(title) is None or form.cleaned_data["edit"] is True):
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("entry", kwargs={'entry': title}))
            else:
                return render(request, "encyclopedia/new.html", {
                    "form": form,
                    "existing": True,
                    "entry": title
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
    entry_page = util.get_entry(title)
    if entry_page is None: 
        return render(request, "encyclopedia/error.html", {
            "entry_title": title
        })
    else:
        form = EditEntryForm()
        form.fields["title"].initial = title
        # form.fields["title"].widget = forms.HiddenInput()
        form.fields["content"].initial = entry_page
        # form.fields["edit"].initial = True
        return render(request, "encyclopedia/edit.html", {
            "form": form,
            "title": title,
            "content": entry_page
            # "edit": form.fields["edit"].initial,
            # "entry_title": form.fields["title"].initial
        })


def random(request):
    entries = util.list_entries()
    random_entry = choice(entries)
    return HttpResponseRedirect(reverse("entry", kwargs={'entry': random_entry}))

