from re import M
from django.shortcuts import render

from . import util
from markdown2 import Markdown

import random
from random import randint


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


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
