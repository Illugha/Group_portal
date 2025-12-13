from django.contrib import admin
from .models import Vote, VoteOption, VoteResponse


class VoteOptionInline(admin.TabularInline):
    """Inline для варіантів голосування"""
    model = VoteOption
    extra = 2
    fields = ['text', 'order']


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    """Адміністрування голосувань"""
    list_display = [
        'title', 
        'created_by', 
        'is_active', 
        'created_at', 
        'total_votes',
        'is_open'
    ]
    list_filter = ['is_active', 'created_at', 'is_anonymous', 'allow_revote']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at', 'total_votes', 'unique_voters']
    
    fieldsets = (
        ('Основна інформація', {
            'fields': ('title', 'description', 'created_by')
        }),
        ('Налаштування', {
            'fields': (
                'is_active', 
                'start_date', 
                'end_date', 
                'allow_revote', 
                'is_anonymous'
            )
        }),
        ('Статистика', {
            'fields': ('created_at', 'updated_at', 'total_votes', 'unique_voters'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [VoteOptionInline]
    
    def save_model(self, request, obj, form, change):
        """Автоматично встановлюємо created_by при створенні"""
        if not change:  # Якщо створюємо новий об'єкт
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    def get_readonly_fields(self, request, obj=None):
        """Робимо created_by незмінним після створення"""
        if obj:  # Редагування існуючого
            return self.readonly_fields + ['created_by']
        return self.readonly_fields


@admin.register(VoteOption)
class VoteOptionAdmin(admin.ModelAdmin):
    """Адміністрування варіантів голосування"""
    list_display = ['vote', 'text', 'order', 'vote_count', 'vote_percentage']
    list_filter = ['vote']
    search_fields = ['text', 'vote__title']
    ordering = ['vote', 'order']


@admin.register(VoteResponse)
class VoteResponseAdmin(admin.ModelAdmin):
    """Адміністрування відповідей користувачів"""
    list_display = ['user', 'vote_title', 'vote_option', 'voted_at']
    list_filter = ['voted_at', 'vote_option__vote']
    search_fields = ['user__username', 'vote_option__vote__title']
    readonly_fields = ['voted_at', 'updated_at']
    date_hierarchy = 'voted_at'
    
    def vote_title(self, obj):
        """Показуємо назву голосування"""
        return obj.vote_option.vote.title
    vote_title.short_description = 'Голосування'
    
    def has_add_permission(self, request):
        """Заборона додавання відповідей через адмінку"""
        return False