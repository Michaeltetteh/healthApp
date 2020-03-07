from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

# @login_required

# class HomePage(TemplateView,LoginRequiredMixin):
#     template_name = 'doctor/home.html'

#     def get_context_data(self, **kwargs):
#         ctx = {}
#         ctx['loggedIn'] = False
#         if self.request.user.is_authenticated:
#             ctx['loggedIn'] = True
#         return ctx


@login_required
def HomePage(request):
    return render(request, "doctor/home.html")