from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin


class DuesView(UserPassesTestMixin, TemplateView):
    template_name = "dues.html"

    def test_func(self):
        return self.request.user.is_superuser
