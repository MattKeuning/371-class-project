from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Exercise, Workout, Vote
from .serializers import ExerciseSerializer, VoteSerializer

class ExerciseListCreateView(generics.ListCreateAPIView):
    serializer_class = ExerciseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Exercise.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ExerciseDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExerciseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Exercise.objects.filter(user=self.request.user)

from .models import Workout
from .serializers import WorkoutSerializer

class WorkoutListCreateView(generics.ListCreateAPIView):
    serializer_class = WorkoutSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Workout.objects.filter(user=self.request.user).order_by('-date')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class WorkoutDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WorkoutSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Workout.objects.filter(user=self.request.user)

class VoteCreateView(generics.CreateAPIView):
    serializer_class = VoteSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        vote, created = Vote.objects.get_or_create(
            user=self.request.user,
            defaults={'preference': serializer.validated_data['preference']}
        )
        if not created:
            vote.preference = serializer.validated_data['preference']
            vote.save()

class VoteStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        total_votes = Vote.objects.count()
        if total_votes == 0:
            return Response({'cardio': 0, 'lifting': 0})

        cardio_count = Vote.objects.filter(preference='cardio').count()
        lifting_count = Vote.objects.filter(preference='lifting').count()

        cardio_percentage = round((cardio_count / total_votes) * 100, 1)
        lifting_percentage = round((lifting_count / total_votes) * 100, 1)

        return Response({
            'cardio': cardio_percentage,
            'lifting': lifting_percentage
        })
