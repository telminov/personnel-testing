# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import redirect


class LoginRequiredMiddleware(object):

    def process_request(self, request):
        except_urls = ('/login/',)
        request_path_startswith = request.path.startswith(except_urls)
        is_authenticated = request.user.is_authenticated()
        redirect_to_login = redirect('/login/?next=%s' % request.get_full_path())
        redirect_to_home = redirect('/')

        # if anonymous - only login or registration
        if not is_authenticated and not request_path_startswith:
            return redirect_to_login
        # elif authenticated - everything, but not login and registration etc
        elif is_authenticated:
            if request_path_startswith:
                return redirect_to_home

        return None
