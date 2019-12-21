from django.shortcuts import render
from django.core.exceptions import ImproperlyConfigured
from django.views.generic.base import ContextMixin, TemplateResponseMixin
from django.views.generic.edit import ProcessFormView
from django.http import HttpResponse, HttpResponseRedirect
from django.db import transaction
import code 

class MultiFormsMixin(ContextMixin):
    form_classes = {}
    prefix = {}
    initial = {}

    success_url = None

    def get_prefix(self, form_name):
        return self.prefix[form_name]

    def get_initial(self, form_name):
        return self.initial[form_name]

    def get_success_url(self):
        if not self.success_url:
            raise ImproperlyConfigured("No url found. Please set the success url")
        return str(self.success_url)

    def get_form_classes(self):
        return self.form_classes


    def get_forms(self, forms = None):
        if forms is None:
            form_classes = self.get_form_classes()
        # code.interact(local = dict(globals(), **locals()))
        return dict([(key, klass(**self.get_form_kwargs(key))) for key, klass in form_classes.items()])

    def forms_valid(self, forms):
        return HttpResponseRedirect(self.success_url)

    def forms_invalid(self, forms):
        return self.render_to_response(self.get_context_data(**forms))

    def get_form_kwargs(self, form_name):
        kwargs = {}

        if self.initial:
            kwargs.update({'initial':self.get_initial(form_name)})

        if self.prefix:
            kwargs.update({'prefix':self.get_prefix(form_name)})

        if self.request.method in ("POST", "PUT"):
            kwargs.update({
                'data':self.request.POST,
                'files':self.request.FILES
            })
        return kwargs

class ProcessMutliFormsView(ProcessFormView):
    """docstring for MultiProcessView"""
    def get(self, request, *args, **kwargs):
        forms = self.get_forms()
        return self.render_to_response(self.get_context_data(**forms))

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        # form_clases = self.get_form_classes()
        forms = self.get_forms()

        if all([form.is_valid() for form in forms.values()]):
            return self.forms_valid(forms)
        else:
            return self.forms_invalid(forms)

class BaseMultiFormsView(MultiFormsMixin, ProcessMutliFormsView):
    """ A base view for displaying multiple forms"""

class MultiFormsView(TemplateResponseMixin, BaseMultiFormsView):
    """A view for displaying several forms, and rendering a template response."""
class AjaxResponseMixin:
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(self, 'ajax_template_name'):
            split = self.template_name.split(".html")
            split[-1] = "_inner"
            split.append(".html")
            self.ajax_template_name = ''.join(split)
        
        if request.is_ajax():
            self.template_name = self.ajax_template_name

        return super().dispatch(request, *args, **kwargs)

