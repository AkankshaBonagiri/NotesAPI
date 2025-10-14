from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from .models import Note
from .serializers import RegisterSerializer, NoteSerializer

User = get_user_model()

# ✅ User Registration View
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


# ✅ List + Create Notes
class NoteListCreateView(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only return notes owned by the logged-in user
        return Note.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        # Automatically set the logged-in user as the note owner
        serializer.save(owner=self.request.user)


# ✅ Retrieve, Update, Delete a Single Note
class NoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only allow access to the user's own notes
        return Note.objects.filter(owner=self.request.user)


# Create your views here.
