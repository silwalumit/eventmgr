from django.shortcuts import render
from django.core.exceptions import ImproperlyConfigured
from django.views.generic.base import ContextMixin, TemplateResponseMixin
from django.views.generic.edit import ProcessFormView
from django.http import HttpResponse, HttpResponseRedirect
from django.db import transaction
 

from django.template.loader import render_to_string
import json
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

    def form_valid(self, forms):
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, forms):
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
            return self.form_valid(forms)
        else:
            return self.form_invalid(forms)

class BaseMultiFormsView(MultiFormsMixin, ProcessMutliFormsView):
    """ A base view for displaying multiple forms"""

class MultiFormsView(TemplateResponseMixin, BaseMultiFormsView):
    """A view for displaying several forms, and rendering a template response."""
class AjaxTemplateMixin:
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(self, 'ajax_template_name'):
            split = self.template_name.split(".html")
            split[-1] = "_inner"
            split.append(".html")
            self.ajax_template_name = ''.join(split)
        
        if request.is_ajax():
            self.template_name = self.ajax_template_name

        return super().dispatch(request, *args, **kwargs)

class AjaxableResponseMixin:
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    
    ajax_template_name = None
    context = {}
    context_name = "data"

    def get_context(self):
        return self.context

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        
        if self.request.is_ajax():
            data = {
            self.context_name: render_to_string(
                self.ajax_template_name, 
                self.get_context(), 
                request = self.request
            )}
            return self.render_to_json(data)
        else:
            return response 

    def render_to_json(self, data):
        return HttpResponse(
            json.dumps(data, ensure_ascii = False),
            content_type = self.request.is_ajax() and "application/json" or "text/html"
        )