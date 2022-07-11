from django.views.generic import TemplateView, RedirectView

# Create your views here.

class home(TemplateView):
    template_name = "quiz/home.html"

class redirecthome(RedirectView):
    url = "http://127.0.0.1:8000/home/"
rd_home = redirecthome.as_view()