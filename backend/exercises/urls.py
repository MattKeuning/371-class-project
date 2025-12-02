from django.urls import path
from .views import ExerciseListCreateView, ExerciseDetailView, WorkoutListCreateView, WorkoutDetailView

app_name = 'exercises'

urlpatterns = [
    path('', ExerciseListCreateView.as_view(), name='exercise-list-create'),
    path('<int:pk>/', ExerciseDetailView.as_view(), name='exercise-detail'),
    path('workouts/', WorkoutListCreateView.as_view(), name='workout-list-create'),
    path('workouts/<int:pk>/', WorkoutDetailView.as_view(), name='workout-detail'),
]
