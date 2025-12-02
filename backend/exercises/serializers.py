from rest_framework import serializers
from .models import Exercise, Workout, WorkoutExercise

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ['id', 'name', 'description', 'date']
        read_only_fields = ['id', 'date']

class WorkoutExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutExercise
        fields = ['id', 'name', 'sets', 'amount', 'unit', 'weight']

class WorkoutSerializer(serializers.ModelSerializer):
    exercises = WorkoutExerciseSerializer(many=True, read_only=True)

    class Meta:
        model = Workout
        fields = ['id', 'name', 'date', 'exercises']
        read_only_fields = ['id', 'date']

    def create(self, validated_data):
        exercises_data = self.context['request'].data.get('exercises', [])
        workout = Workout.objects.create(**validated_data)
        for exercise_data in exercises_data:
            WorkoutExercise.objects.create(workout=workout, **exercise_data)
        return workout
