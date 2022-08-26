
from typing import Any
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.template.loader import render_to_string

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import TaskForm
from .models import Category, Task


class TaskList(LoginRequiredMixin, ListView):
    # model = Task
    context_object_name = 'tasks'
    template_name = 'base/task_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        is_ajax = self.request.headers.get(
            'X-Requested-With') == "XMLHttpRequest"
        if not is_ajax:
            # number of task for each type
            context['all_count'] = context['tasks'].filter(
                complete=False).count()
            context['complete_count'] = context['tasks'].filter(
                complete=True).count()
            context['primary_count'] = context['tasks'].filter(
                primary=True).count()

            context['tasks'] = context['tasks'].filter(complete=False)
            # get all categories
            context['categories'] = Category.objects.filter(
                user=self.request.user)

        else:
            # type of search (all, complete, primary) or search-area
            search_input = self.request.GET.get('search-area') or ''
            if search_input:
                if search_input == 'complete':
                    context['tasks'] = context['tasks'].filter(complete=True)
                elif search_input == 'primary':
                    context['tasks'] = context['tasks'].filter(primary=True)
                elif search_input != 'all':
                    context['tasks'] = context['tasks'].filter(
                        title__startswith=search_input)
                    context['search_input'] = search_input
                else:
                    context['tasks'] = context['tasks'].filter(complete=False)

        # search by category
        category_input = self.request.GET.get('category') or ''
        if category_input and category_input != 'all':
            try:
                cat = Category.objects.get(
                    user=self.request.user, name=category_input)
                context['tasks'] = context['tasks'].filter(category=cat)
            except:
                pass

        return context

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs) -> HttpResponse:

        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            self.object_list = self.get_queryset()
            context = self.get_context_data(**kwargs)

            data = {"tasks": render_to_string(
                'base/partials/task_list_partial.html', context, self.request)}
            return JsonResponse(data)

        return super().get(request, *args, **kwargs)


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    # fields = ['title', 'description', 'date', 'primary', 'category']
    form_class = TaskForm
    success_url = reverse_lazy('base:tasks')

    def get(self, request, *args, **kwargs) -> HttpResponse:
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            context = dict()
            context['form'] = self.get_form()
            context['categories'] = Category.objects.filter(user=request.user)
            data = {"html_form": render_to_string(
                'base/partials/task_form_partial.html', context, self.request)}
            return JsonResponse(data)

        return redirect('base:tasks')

    def form_valid(self, form) -> HttpResponse:
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):

    model = Task
    # fields = ['title', 'description', 'date',
    #           'primary', 'category', 'complete']
    form_class = TaskForm
    success_url = reverse_lazy('base:tasks')

    def dispatch(self, request, *args: Any, **kwargs) -> HttpResponseBadRequest:
        if (request.user != Task.objects.get(pk=kwargs['pk']).user):
            return HttpResponseForbidden(request)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs) -> HttpResponse:

        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            self.object = self.get_object()
            context = self.get_context_data()

            if request.GET.get('complete'):

                context['object'].complete = not context['object'].complete
                context['object'].save()

                data = {'html_form': render_to_string(
                    'base/partials/task_complete.html', context, request)}
                return JsonResponse(data)

            # modify the format of date yyyy-mm-dd
            year = str(context['object'].date.year)
            month = str(context['object'].date.month)
            if len(month) == 1:
                month = "0"+month
            day = str(context['object'].date.day)
            context['object'].date = year+"-"+month+"-"+day

            # the category
            catId = context['object'].category.id if context['object'].category else -1
            context['categories'] = Category.objects.filter(
                user=request.user).exclude(pk=catId)

            data = {'html_form': render_to_string(
                'base/partials/task_form_partial.html', context, request)}
            return JsonResponse(data)

        return redirect('base:tasks')


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('base:tasks')

    def dispatch(self, request, *args: Any, **kwargs) -> HttpResponseBadRequest:
        if (request.user != Task.objects.get(pk=kwargs['pk']).user):
            return HttpResponseForbidden(request)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args: Any, **kwargs: Any) -> HttpResponse:
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            context = {"object": self.get_object()}

            data = {'html_form': render_to_string(
                'base/partials/task_confirm_delete_partial.html', context, request)}
            return JsonResponse(data)

        return redirect(self.get_success_url())


class CategoryCreate(LoginRequiredMixin, CreateView):
    model = Category
    fields = ['name']
    success_url = reverse_lazy('base:tasks')

    def get(self, request, *args, **kwargs) -> HttpResponse:
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            data = {"html_form": render_to_string(
                'base/partials/category_form_partial.html', {}, self.request)}
            return JsonResponse(data)

        return redirect('base:tasks')

    def form_valid(self, form) -> HttpResponse:
        form.instance.user = self.request.user
        return super(CategoryCreate, self).form_valid(form)
