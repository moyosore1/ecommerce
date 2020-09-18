from django.shortcuts import redirect


def guest(view_func):

    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('Store-home')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func
#
#
#
#

