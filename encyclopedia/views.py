from re import M

from django.shortcuts import render
from django import forms
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


# Index Page, returns all entries in a list
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

