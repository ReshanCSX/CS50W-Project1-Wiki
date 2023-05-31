from django.shortcuts import render

from . import util
from markdown2 import Markdown


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
        "name": title,
        "render_entries": markdown.convert(util.get_entry(title)) 
    })

