from django.shortcuts import render

from . import util
from markdown2 import Markdown


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
    # If the title page exists, display the corresponding page
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry_page": markdowner.convert(entry_page),
            "entry_title": entry
        })


