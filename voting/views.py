from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from .models import Vote, VoteOption, VoteResponse
from .forms import VoteForm, VoteOptionFormSet, VoteResponseForm


class ModeratorRequiredMixin(UserPassesTestMixin):
    """Mixin для перевірки прав модератора або адміністратора"""
    def test_func(self):
        return self.request.user.is_staff or self.request.user.groups.filter(name='Moderators').exists()


class VoteListView(LoginRequiredMixin, ListView):
    """Список всіх голосувань"""
    model = Vote
    template_name = 'voting/vote_list.html'
    context_object_name = 'votes'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Показуємо тільки активні голосування для звичайних користувачів
        if not (self.request.user.is_staff or self.request.user.groups.filter(name='Moderators').exists()):
            queryset = queryset.filter(is_active=True)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Додаємо інформацію про те, чи голосував користувач
        if self.request.user.is_authenticated:
            user_votes = VoteResponse.objects.filter(
                user=self.request.user,
                vote_option__vote__in=context['votes']
            ).values_list('vote_option__vote_id', flat=True)
            context['user_votes'] = set(user_votes)
        return context


class VoteDetailView(LoginRequiredMixin, DetailView):
    """Детальний перегляд голосування та можливість проголосувати"""
    model = Vote
    template_name = 'voting/vote_detail.html'
    context_object_name = 'vote'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vote = self.object
        user = self.request.user
        
        # Перевірка, чи користувач вже голосував
        user_response = VoteResponse.get_user_response(user, vote)
        context['user_response'] = user_response
        context['has_voted'] = user_response is not None
        context['can_vote'] = vote.is_open() and (not context['has_voted'] or vote.allow_revote)
        
        # Додаємо статистику
        context['total_votes'] = vote.total_votes()
        context['unique_voters'] = vote.unique_voters()
        
        # Додаємо форму для голосування
        if context['can_vote']:
            context['form'] = VoteResponseForm(vote=vote, initial={'user': user})
        
        return context
    
    def post(self, request, *args, **kwargs):
        """Обробка голосування"""
        vote = self.get_object()
        
        if not vote.is_open():
            messages.error(request, "Це голосування вже завершено або ще не розпочато.")
            return redirect('voting:vote_detail', pk=vote.pk)
        
        # Перевірка, чи користувач вже голосував
        user_response = VoteResponse.get_user_response(request.user, vote)
        
        if user_response and not vote.allow_revote:
            messages.error(request, "Ви вже проголосували. Переголосування заборонено.")
            return redirect('voting:vote_detail', pk=vote.pk)
        
        form = VoteResponseForm(request.POST, vote=vote)
        
        if form.is_valid():
            option = form.cleaned_data['vote_option']
            
            # Якщо користувач вже голосував, видаляємо стару відповідь
            if user_response:
                user_response.delete()
            
            # Створюємо нову відповідь
            VoteResponse.objects.create(
                user=request.user,
                vote_option=option
            )
            
            messages.success(request, "Ваш голос збережено!")
            return redirect('voting:vote_detail', pk=vote.pk)
        else:
            messages.error(request, "Помилка при голосуванні. Будь ласка, спробуйте ще раз.")
            return redirect('voting:vote_detail', pk=vote.pk)


class VoteCreateView(LoginRequiredMixin, ModeratorRequiredMixin, CreateView):
    """Створення нового голосування"""
    model = Vote
    form_class = VoteForm
    template_name = 'voting/vote_form.html'
    success_url = reverse_lazy('voting:vote_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['option_formset'] = VoteOptionFormSet(self.request.POST)
        else:
            context['option_formset'] = VoteOptionFormSet()
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        option_formset = context['option_formset']
        
        with transaction.atomic():
            form.instance.created_by = self.request.user
            self.object = form.save()
            
            if option_formset.is_valid():
                option_formset.instance = self.object
                option_formset.save()
                messages.success(self.request, "Голосування успішно створено!")
                return super().form_valid(form)
            else:
                return self.form_invalid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Помилка при створенні голосування. Перевірте дані.")
        return super().form_invalid(form)


class VoteUpdateView(LoginRequiredMixin, ModeratorRequiredMixin, UpdateView):
    """Редагування голосування"""
    model = Vote
    form_class = VoteForm
    template_name = 'voting/vote_form.html'
    success_url = reverse_lazy('voting:vote_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['option_formset'] = VoteOptionFormSet(self.request.POST, instance=self.object)
        else:
            context['option_formset'] = VoteOptionFormSet(instance=self.object)
        context['is_update'] = True
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        option_formset = context['option_formset']
        
        with transaction.atomic():
            self.object = form.save()
            
            if option_formset.is_valid():
                option_formset.instance = self.object
                option_formset.save()
                messages.success(self.request, "Голосування успішно оновлено!")
                return super().form_valid(form)
            else:
                return self.form_invalid(form)


class VoteDeleteView(LoginRequiredMixin, ModeratorRequiredMixin, DeleteView):
    """Видалення голосування"""
    model = Vote
    template_name = 'voting/vote_confirm_delete.html'
    success_url = reverse_lazy('voting:vote_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, "Голосування успішно видалено!")
        return super().delete(request, *args, **kwargs)


class VoteResultsView(LoginRequiredMixin, DetailView):
    """Перегляд результатів голосування"""
    model = Vote
    template_name = 'voting/vote_results.html'
    context_object_name = 'vote'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vote = self.object
        
        # Збираємо статистику по кожному варіанту
        options_stats = []
        for option in vote.options.all():
            options_stats.append({
                'option': option,
                'count': option.vote_count(),
                'percentage': option.vote_percentage()
            })
        
        context['options_stats'] = options_stats
        context['total_votes'] = vote.total_votes()
        context['unique_voters'] = vote.unique_voters()
        
        # Якщо голосування не анонімне і користувач - модератор
        if not vote.is_anonymous and (self.request.user.is_staff or 
                                       self.request.user.groups.filter(name='Moderators').exists()):
            context['show_voters'] = True
            # Отримуємо список користувачів для кожного варіанту
            for stat in options_stats:
                stat['voters'] = VoteResponse.objects.filter(
                    vote_option=stat['option']
                ).select_related('user').order_by('-voted_at')
        
        return context