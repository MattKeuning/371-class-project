from django.contrib import admin
from .models import Exercise

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
