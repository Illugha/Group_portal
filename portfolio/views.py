from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Portfolio, Screenshot, Attachment, ExternalLink
from .forms import PortfolioForm

class PortfolioListView(ListView):
    model = Portfolio
    template_name = 'portfolio/portfolio_list.html'
    context_object_name = 'portfolios'
    paginate_by = 12
    ordering = ['-created_at']

class PortfolioDetailView(DetailView):
    model = Portfolio
    template_name = 'portfolio/portfolio_detail.html'
    context_object_name = 'portfolio'

class OwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user

class PortfolioDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = Portfolio
    template_name = 'portfolio/portfolio_confirm_delete.html'
    success_url = reverse_lazy('portfolio:list')


# Список проектів з портфоліо чужого користувача
class UserPortfolioView(LoginRequiredMixin, ListView):
    model = Portfolio
    template_name = 'portfolio/user_portfolio.html'
    context_object_name = 'portfolio_items'
    paginate_by = 6

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs['username'])
        return Portfolio.objects.filter(owner=user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_user'] = get_object_or_404(User, username=self.kwargs['username']).profile
        return context


@login_required
def portfolio_create(request):
    if request.method == 'POST':
        form = PortfolioForm(request.POST)
        if form.is_valid():
            p = form.save(commit=False)
            p.owner = request.user
            p.save()
            for f in request.FILES.getlist('screenshots'):
                Screenshot.objects.create(portfolio=p, image=f)
            for f in request.FILES.getlist('attachments'):
                Attachment.objects.create(portfolio=p, file=f, name=f.name)
            link_names = request.POST.getlist('link_name')
            link_urls = request.POST.getlist('link_url')
            for name, url in zip(link_names, link_urls):
                if url:
                    ExternalLink.objects.create(portfolio=p, name=name or '', url=url)
            return redirect('portfolio:detail', pk=p.pk)
    else:
        form = PortfolioForm()
    return render(request, 'portfolio/portfolio_form.html', {'form': form})

@login_required
def portfolio_update(request, pk):
    p = get_object_or_404(Portfolio, pk=pk)
    if p.owner != request.user:
        return redirect('portfolio:detail', pk=pk)
    if request.method == 'POST':
        form = PortfolioForm(request.POST, instance=p)
        if form.is_valid():
            p = form.save()
            for f in request.FILES.getlist('screenshots'):
                Screenshot.objects.create(portfolio=p, image=f)
            for f in request.FILES.getlist('attachments'):
                Attachment.objects.create(portfolio=p, file=f, name=f.name)
            link_names = request.POST.getlist('link_name')
            link_urls = request.POST.getlist('link_url')
            for name, url in zip(link_names, link_urls):
                if url:
                    ExternalLink.objects.create(portfolio=p, name=name or '', url=url)
            return redirect('portfolio:detail', pk=p.pk)
    else:
        form = PortfolioForm(instance=p)
    return render(request, 'portfolio/portfolio_form.html', {'form': form, 'portfolio': p})
