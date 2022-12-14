
from django.urls import reverse_lazy

from django import template
register = template.Library()


@register.simple_tag(takes_context=True)
def get_url(context, action, obj=None):
    # model = context['model']
    # app = model._meta.app_label
    # lower_name = model.__name__.lower()
    app = "base"
    lower_name = "task"
    if not obj:
        url_string = '{}:{}-{}'.format(app, lower_name, action)
        url = reverse_lazy(url_string)
    else:
        lower_name = obj.__class__.__name__.lower()
        url_string = '{}:{}-{}'.format(app, lower_name, action)
        if(hasattr(obj, 'uuid')):
            url = reverse_lazy(url_string, kwargs={'uuid': obj.uuid})
        elif(hasattr(obj, 'slug')):
            url = reverse_lazy(url_string, kwargs={'slug': obj.slug})
        else:
            url = reverse_lazy(url_string, kwargs={'pk': obj.pk})
    return url
