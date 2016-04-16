import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import UpdateView, ListView as DjangoListView, DetailView as DjangoDetailView,\
    View as DjangoView, TemplateView as DjangoTemplateView, DeleteView as DjangoDeleteView


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

    def _get_object_from_qs(self, queryset):
        return queryset.get()

    def _init_object(self):
        return self.model()

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

                self._object = self._get_object_from_qs(queryset)
            else:
                self._object = self._init_object()
        return self._object

    def get_context_data(self, **kwargs):
        context = super(CreateOrUpdateView, self).get_context_data(**kwargs)
        context['is_update'] = self.is_update()
        context['is_create'] = self.is_create()
        return context


class DeleteView(TitleMixin, DjangoDeleteView):
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.deleted_at = datetime.datetime.now()
        self.object.save()
        return HttpResponseRedirect(success_url)


class ListView(TitleMixin, DjangoListView):
    pass


class DetailView(TitleMixin, DjangoDetailView):
    pass


class View(TitleMixin, DjangoView):
    pass


class TemplateView(TitleMixin, DjangoTemplateView):
    pass


class ParentMixin(object):
    parent_pk_url_kwarg = None
    _parent_object = None
    parent_model = None
    context_parent_object_name = 'parent_object'

    def get_parent_queryset(self):
        return self.parent_model.objects.all()

    def get_parent_object(self, queryset=None):
        if not self._parent_object:
            if queryset is None:
                queryset = self.get_parent_queryset()

            pk = self.kwargs.get(self.parent_pk_url_kwarg, None)

            if pk is not None:
                queryset = queryset.filter(pk=pk)

                self._parent_object = queryset.get()

            else:
                self._parent_object = self.model()
        return self._parent_object

    def get_context_data(self, **kwargs):
        context = super(ParentMixin, self).get_context_data(**kwargs)
        context[self.context_parent_object_name] = self.get_parent_object()
        return context


class ParentListView(ParentMixin, ListView):

    def get_queryset(self):
        qs = super(ParentListView, self).get_queryset()
        qs = qs.filter(examination=self.get_parent_object())
        return qs


class ParentCreateOrUpdateView(ParentMixin, CreateOrUpdateView):
    parent_field_name = None

    def _init_object(self):
        return self.model(**{self.parent_field_name: self.get_parent_object()})

    def _get_object_from_qs(self, queryset):
        return queryset.get(**{self.parent_field_name: self.get_parent_object()})
