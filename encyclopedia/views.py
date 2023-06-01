from django.shortcuts import render

from . import util
from markdown2 import Markdown
from django.http import HttpResponseRedirect
from django.urls import reverse


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def content(request, title):

    entry = util.get_entry(title)

    if not entry:
        return render(request, "encyclopedia/error.html", {
            "message" : f"The requested URL <b> {request.get_full_path()} </b> was not found" 
        })


    markdown = Markdown()

    return render(request, "encyclopedia/content.html", {
        "page_name": title,
        "render_entries": markdown.convert(util.get_entry(title)) 
    })

def search(request):

    q = request.GET["q"]

    search_item = util.get_entry(q)

    if search_item:
        return HttpResponseRedirect(reverse("content", args=[q]))
    
    else:

        titles = util.list_entries()
        search_entries = []

        for title in titles:
            if q.lower() in title.lower():
                search_entries.append(title)

        

        return render(request, "encyclopedia/search.html",{
            "page_name": q.capitalize(),
            "keyword": q,
            "search_entries": search_entries
    })
