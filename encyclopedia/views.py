from django.shortcuts import render

from . import util
from markdown2 import Markdown
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def content(request, title):

    entry = util.get_entry(title)

    if not entry:
        return render(request, "encyclopedia/error.html", {
            "message" : f"The requested URL <b> {request.get_full_path()} </b> was not found",
            "redirect": "index" 
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

        

        return render(request, "encyclopedia/search.html", {
            "page_name": q.capitalize(),
            "keyword": q,
            "search_entries": search_entries
    })

class NewPageForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control w-75 mb-2'}), label="Page Title")
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control w-75 h-25'}), label="Description:")

def create(request):

    if request.method == "POST":
        form = NewPageForm(request.POST)
        titles = list(title.lower() for title in util.list_entries())

        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            if title.lower() in titles:
                return render(request, "encyclopedia/error.html",{
                    "message": "Page with this name already exists",
                    "redirect": "create"
                })
            
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("content", args=[title]))

        else:
            return render(request, "encyclopedia/create.html", {
                "form": form
                })


    return render(request, "encyclopedia/create.html", {
            "form": NewPageForm()
        })
