from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    """Index page."""
    template = 'index.html'
    context = {}
    return render(request, context=context, template_name=template)
