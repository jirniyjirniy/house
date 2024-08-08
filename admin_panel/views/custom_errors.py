from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader, Context


def customhandler404(request, exception=None):
    template = loader.get_template('admin_panel/errors/404.html')
    context = {'message': 'All: %s' % request, }
    return HttpResponse(content=template.render(context), content_type='text/html; charset=utf-8', status=404)


def customhandler500(request, exception=None):
    template = loader.get_template('admin_panel/errors/500.html')
    context = {'message': 'All: %s' % request, }
    return HttpResponse(content=template.render(context), content_type='text/html; charset=utf-8', status=500)

