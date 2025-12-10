import os

from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic

from .forms import FeelingForm
from .models import Feeling


class IndexView(generic.TemplateView):
    template_name = "feelings/index.html"


class FeelingsListView(generic.ListView):
    template_name = "feelings/list.html"
    context_object_name = "feelings_list"
    model = Feeling

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(created_by=self.request.user)
            .order_by("-created_at")
        )


class FeelingCreateView(generic.CreateView):
    template_name = "feelings/create.html"
    model = Feeling
    form_class = FeelingForm
    success_url = reverse_lazy("feelings:list")

    def form_valid(self, form):
        feeling = form.save(commit=False)
        feeling.created_by = self.request.user
        feeling.save()
        messages.success(self.request, "Feeling entry created successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error creating the feeling entry.")
        return super().form_invalid(form)


class FeelingDetailView(generic.DetailView):
    template_name = "feelings/detail.html"
    context_object_name = "feeling"
    model = Feeling
    pk_url_kwarg = "pk"


class FeelingUpdateView(generic.UpdateView):
    template_name = "feelings/update.html"
    model = Feeling
    form_class = FeelingForm
    pk_url_kwarg = "pk"

    def get_success_url(self):
        return reverse_lazy("feelings:detail", kwargs={"pk": self.kwargs["pk"]})

    def form_valid(self, form):
        messages.success(self.request, "Feeling entry updated successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error updating the feeling entry.")
        return super().form_invalid(form)


class FeelingDeleteView(generic.DeleteView):
    template_name = "feelings/delete.html"
    model = Feeling
    pk_url_kwarg = "pk"
    success_url = reverse_lazy("feelings:list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Feeling entry deleted successfully.")
        return super().delete(request, *args, **kwargs)


class FeelingGraphView(generic.TemplateView):
    template_name = "feelings/graph.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        feelings = Feeling.objects.filter(created_by=self.request.user).select_related(
            "stamp"
        )
        stamp_score_pairs = sorted(
            set((f.stamp.name, f.stamp.score) for f in feelings),
            key=lambda x: x[1],
            reverse=True,
        )
        y_labels = [name for name, score in stamp_score_pairs]
        y_scores = [score for name, score in stamp_score_pairs]
        feelings = sorted(feelings, key=lambda f: f.created_at)
        context["labels"] = [f.created_at.strftime("%Y-%m-%d %H:%M") for f in feelings]
        context["scores"] = [f.stamp.score for f in feelings]
        context["comments"] = [f.comment or "" for f in feelings]
        context["y_labels"] = y_labels
        context["y_scores"] = y_scores
        stamps_dir = os.path.join(
            os.path.dirname(__file__), "..", "static", "feelings", "stamps"
        )
        stamp_images = [
            f
            for f in os.listdir(stamps_dir)
            if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))
        ]
        context["stamp_images"] = stamp_images
        return context
