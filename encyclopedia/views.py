from re import M

from django.shortcuts import render
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect

from . import util
from markdown2 import Markdown
from random import randint

# Form to create new entry pages
class NewEntryForm(forms.Form):
    title = forms.CharField(label = "Title")
    content = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols": 20}), label = "Content")


# Form to edit existing entry pages
class EditEntryForm(forms.Form):
    title = forms.CharField(label = "Edit Title")
    content = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols": 20}), label = "Edit Content")


# Index Page - returns all entries in a list
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


# Display a specific entry page
def entry(request, title):
    markdowner = Markdown()
    entry_page = util.get_entry(title)

    # Check if title page exists
    # If no title page exists, display the error page
    if entry_page is None:
        return render(request, "encyclopedia/error.html")
    # If the title page exists, display the title of the entry and converted markdown content
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry_page": markdowner.convert(entry_page),
            "entry_title": entry
        })


# Returns an entry page at random
def random(request):
    markdowner = Markdown()
    # Obtain list of all entries
    all_entries = util.list_entries()

    # Use random function to pull a random entry from the list
    entry = randint(0, len(all_entries)-1)
    random_entry = all_entries[entry] 
    entry_page = util.get_entry(random_entry)
    
    return render(request, "encyclopedia/random.html", {
        "entry_page": markdowner.convert(entry_page),
        "entry_title": random_entry
    })


# Returns a form for creating a new entry in the encyclopedia
def new(request):

    # Check if the method is POST
    if request.method == "POST":

        # Take in the data the user submitted and save it as form
        form = NewEntryForm(request.POST)

        # Check if form data is valid
        if form.is_valid():

            # Isolate the title and the content from the 'cleaned' version of form data
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            # Check if entry title is already in use
            if(util.get_entry(title) is None or form.cleaned_data["edit"] is True):
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("entry:title"))

    # If request method is GET
    else:
        form = NewEntryForm()
        return render(request, "encyclopedia/new.hmtl", {
            form: "form"
        })



# def edit(request, title):

