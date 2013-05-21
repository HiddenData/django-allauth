#!/usr/bin/env python
#-*- coding: utf-8 -*-
#vim: set ts=4 sw=4 et fdm=marker : */

from coffin.template import Library
from jinja2._markupsafe import Markup
from allauth.account.utils import user_display
from allauth.socialaccount import providers
import jinja2

register = Library()

@register.object
@jinja2.contextfunction
def provider_login_url(context, provider_id, **kwargs):
    provider = providers.registry.by_id(provider_id)
    query = kwargs
    request = context['request']
    if 'next' not in query:
        next = request.REQUEST.get('next')
        if next:
            query['next'] = next
    else:
        if not query['next']:
            del query['next']
    return provider.get_login_url(request, **query)


@register.object
@jinja2.contextfunction
def providers_media_js(context):
    request = context['request']
    ret = '\n'.join([p.media_js(request)
                     for p in providers.registry.get_list()])
    return Markup(ret)


@register.object
@jinja2.contextfunction
def do_user_display(context, user):
    display = user_display(user)
    return display
