from django.shortcuts import render

# Create your views here.

from .models import Photo, Album, Metadata

from django.shortcuts import get_object_or_404

from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView

from django.core.exceptions import PermissionDenied

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.urls import reverse_lazy

from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSetView, InlineFormSetFactory

from django.db.models import Q


# This ListView only utilizes one model : Photo
class PhotoListView(ListView):
    model = Photo

    template_name = 'photoshare/list.html'
    # gives a common name to the model
    context_object_name = 'photos'


# Views the tags
class PhotoTagListView(PhotoListView):
    template_name = 'photoshare/taglist.html'

    # Custom method
    def get_tag(self):
        return self.kwargs.get('tag')

    def get_queryset(self):
        return self.model.objects.filter(tags__slug=self.get_tag())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag"] = self.get_tag()
        return context


# This DetailView gets the detail of the photo clicked. Only has one model as the Metadata model gets the Photo by
# default.
class MetadataView(DetailView):
    model = Metadata

    template_name = 'photoshare/detail.html'
    # gives a common name to the model
    context_object_name = 'detail'


# One model(Metadata) approach
# class PhotoCreateView(LoginRequiredMixin, CreateView):
#     model = Metadata  # Change to photo if error
#
#     fields = ['title', 'description', 'tags', 'photo']
#
#     template_name = 'photoshare/create.html'
#
#     success_url = reverse_lazy('photo:list')
#
#     def form_valid(self, form):
#         form.instance.submitter = self.request.user
#
#         return super().form_valid(form)
#


# Two model approach
class MetadataInline(InlineFormSetFactory):
    model = Metadata

    fields = ['title', 'description', 'submitter', 'location', 'tags', 'photo', 'access']


class PhotoCreateView(LoginRequiredMixin, CreateWithInlinesView):
    model = Photo
    # TODO

    inlines = [MetadataInline]

    fields = ['image', 'submitter', 'access']

    template_name = 'photoshare/create.html'

    success_url = reverse_lazy('photoshare:list')

    # def __init__(self, *args, **kwargs):
    #     super(Photo, self).__init__(*args, **kwargs)
    #     self.initial['title'] = 'Initial value'

    # def get_initial(self):
    #     # call super if needed
    #     return {'title': 'init'}

    def form_valid(self, form):
        form.instance.submitter = self.request.user

        return super().form_valid(form)


class UserIsSubmitter(UserPassesTestMixin):

    # Custom method
    def get_metadata(self):
        return get_object_or_404(Metadata, pk=self.kwargs.get('pk'))

    def get_photo(self):
        return get_object_or_404(Photo, pk=self.kwargs.get('pk'))

    def test_func(self):

        if self.request.user.is_authenticated:
            return self.request.user == self.get_metadata().submitter

        else:
            raise PermissionDenied('Sorry you are not allowed here')


class PhotoUpdateView(UserIsSubmitter, UpdateWithInlinesView):
    # TODO

    template_name = 'photoshare/update.html'

    model = Photo  # Change to photo if error

    inlines = [MetadataInline]

    fields = ['image']

    success_url = reverse_lazy('photoshare:list')


# Delete unknown, find out for Metadata delete and Photo delete
class PhotoDeleteView(UserIsSubmitter, DeleteView):
    # TODO

    template_name = 'photoshare/delete.html'

    model = Photo  # Change to photo if error

    success_url = reverse_lazy('photoshare:list')


class SearchResultsView(ListView):
    model = Metadata
    template_name = 'search_results.html'
    queryset = Metadata.objects.filter(description__icontains='Cow qr')

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            object_list = Metadata.objects.filter(
                Q(description__icontains=query) | Q(title__icontains=query)
            )
            return object_list


