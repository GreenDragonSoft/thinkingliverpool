from django.views.generic.base import TemplateView


class SiteHome(TemplateView):
    template_name = 'events/site_home.html'
