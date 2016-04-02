from django.shortcuts import redirect
from django.views.generic import UpdateView, ListView as DjangoListView, DetailView as DjangoDetailView,\
    View as DjangoView, TemplateView as DjangoTemplateView


class TitleMixin(object):
    title = None

    def get_title(self):
        return self.title

    def get_context_data(self, **kwargs):
        context = super(TitleMixin, self).get_context_data(**kwargs)
        context['title'] = self.get_title()
        return context


class CreateOrUpdateView(TitleMixin, UpdateView):
    http_method_names = ['get', 'post']
    form_class_create = None
    form_class_update = None
    _object = None

    def is_update(self):
        return bool(self.get_object().id)

    def is_create(self):
        return not self.is_update()

    def get_form_class(self):
        if self.is_create():
            self.form_class = self.form_class_create
        elif self.is_update():
            self.form_class = self.form_class_update
        return super(CreateOrUpdateView, self).get_form_class()

    def form_valid(self, form, commit=True):
        self.object = form.save(commit=commit)
        return redirect(self.get_success_url())

    def get_object(self, queryset=None):
        if not self._object:
            if queryset is None:
                queryset = self.get_queryset()

            pk = self.kwargs.get(self.pk_url_kwarg, None)
            slug = self.kwargs.get(self.slug_url_kwarg, None)

            if pk or slug:
                if pk is not None:
                    queryset = queryset.filter(pk=pk)

                elif slug is not None:
                    slug_field = self.get_slug_field()
                    queryset = queryset.filter(**{slug_field: slug})

                self._object = queryset.get()

            else:
                self._object = self.model()
        return self._object


class ListView(TitleMixin, DjangoListView):
    pass


class DetailView(TitleMixin, DjangoDetailView):
    pass


class View(TitleMixin, DjangoView):
    pass


class TemplateView(TitleMixin, DjangoTemplateView):
    pass
