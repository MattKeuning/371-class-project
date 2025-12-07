from django.contrib import admin
from .models import Exercise, Vote

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'description', 'date')
    search_fields = ('user__username', 'name')
    list_filter = ('date',)

from .models import Workout, WorkoutExercise

@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'date')
    search_fields = ('user__username', 'name')
    list_filter = ('date',)

@admin.register(WorkoutExercise)
class WorkoutExerciseAdmin(admin.ModelAdmin):
    list_display = ('workout', 'name', 'sets', 'amount', 'unit', 'weight')
    search_fields = ('workout__name', 'name')

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'preference', 'created_at')
    search_fields = ('user__username', 'preference')
    list_filter = ('preference', 'created_at')
    actions = ['delete_selected']

    def delete_selected(self, request, queryset):
        queryset.delete()
        self.message_user(request, f"Deleted {queryset.count()} vote(s). Users can now vote again.")
    delete_selected.short_description = "Delete selected votes (allow users to re-vote)"
