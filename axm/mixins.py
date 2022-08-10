
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.template.loader import render_to_string


# add app and model to context for later use
class ModelMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['model'] = self.model
        context['model_name'] = self.model.__name__.lower()
        context['app_name'] = self.model._meta.app_label
        context['page_title'] = self.model.__name__.capitalize()

        return context


# define the main page (list page) a success page
class SuccessUrlMixin:
    def get_success_url(self):
        model_name = self.model.__name__.lower()
        app = self.model._meta.app_label
        return reverse_lazy("{}:{}-list".format(app, model_name))


# define of the GET method for AJAX request
class ObjectMixin:
    def get(self, request, *args, **kwargs):
        self.object = self.get_object() or None
        context = self.get_context_data()

        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            html_form = render_to_string(
                self.ajax_partial, context, self.request)
            data = {'html_form': html_form}
            return JsonResponse(data)

        return super().get(request, *args, **kwargs)


# define the form verified for create and update request
class FormMixin:
    def form_valid(self, form):
        form.save()
