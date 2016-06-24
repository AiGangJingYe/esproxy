# -*- coding: utf-8 -*-
import os
import re
import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib import auth
from django.core.cache import cache
from esauth.models import ESAuth
import settings


def pass_authorize(user, index, action):
    '''if the USER could do the ACTION with the INDEX
    '''
    index_config = cache.get(index)

    # build cache
    if index_config is None:
        index_config = []
        for o in ESAuth.objects.order_by("index"):
            if not re.match(r'^%s$' % o.index_regexp, index):
                continue
            #o_action  = o.get_action_display()
            index_config.append(o)
        # cache the config
        cache.set(index, index_config, settings.AUTH_CACHE_TIMEOUT)

    for config in index_config:
        if config.get_action_display() in (action, "all"):
            if config.username in (user.username, "_ALL_") or config.group in [e.name for e in user.groups.all()]:
                return config.allowed

    # default true
    return True


def authorize(func):
    def inner(*args, **karags):
        request = args[0]
        user = request.user
        path = request.path
        if request.method == 'DELETE':
            action = '_delete'
        else:
            action = [e for e in path.split('/') if e and e[0] == '_']

        if not action:
            return func(*args, **karags)

        if isinstance(action, list):
            action = action[0]

        if action == '_msearch':
            _splited = [e for e in path.split('/')]
            indices = _splited[_splited.index('_msearch')-1].split(',')
            for i, line in enumerate(request.body.split('\n')):
                if i % 2 == 0 and line != "":
                    indices.extend(json.loads(line).get('index').split(','))
        else:
            # parts[0] is blank;#parts[1] is ELASTICSEARCH_PROXY
            if path.split('/')[2].startswith("_"):
            # it is not real indexname, maybe an action
                return func(*args, **karags)
            indices = path.split('/')[2].split(',')

        for index in indices:
            if pass_authorize(user, index, action) is False:
                return HttpResponseRedirect(settings.ELASTICSEARCH_REAL)

        return func(*args, **karags)

    return inner


def login_or_redirect_to_internal(func):
    def inner(*args, **karags):
        request = args[0]
        if request.user.is_authenticated():
            return func(*args, **karags)
        else:
            r = HttpResponse('',)
            r.status_code = 403
            return r

    return inner


@authorize
@login_or_redirect_to_internal
@csrf_exempt
def elasticsearch(request):
    fullpath = request.get_full_path().encode("UTF8")
    response = HttpResponse()
    response[
        'X-Accel-Redirect'] = fullpath.replace(settings.ELASTICSEARCH_PROXY, settings.ELASTICSEARCH_REAL, 1)
    response['Django-User'] = request.user.username
    return response


@login_required
def home(request):
    html = open(os.path.join(settings.KIBANA_DIR, "index.html")).read()
    response = HttpResponse(html)
    return response


def loginpage(request):
    return render(
        request, 'login.html', {
            'next': request.GET.get(
                'next', '/')})


def loginuser(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    nextpage = request.POST.get('next', '/')
    user = authenticate(username=username, password=password)
    if not user:
        return HttpResponseRedirect(nextpage)

    auth.login(request, user)
    return HttpResponseRedirect(nextpage)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')
