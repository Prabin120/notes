from rest_framework import generics,status
from .models import Note
from django.db.models import Q
from .serializers import NoteSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django.contrib.auth.models import User
from django.contrib.postgres.search import SearchVector


class NoteListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NoteSerializer

    def list(self, request, *args, **kwargs):
        queryset = Note.objects.filter(user=request.user)
        serializer = NoteSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NoteSerializer

    def get_object(self):
        try:
            note = Note.objects.get(id=self.kwargs['id'])
            return note
        except Note.DoesNotExist:
            raise NotFound()
        
    def get(self, request, *args, **kwargs):
        note = self.get_object()
        if note.user == request.user or request.user in note.shared_with.all():
            serializer = NoteSerializer(note)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        note = self.get_object() 
        if note.user == request.user:
            serializer = NoteSerializer(note, data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, *args, **kwargs):
        note = self.get_object()
        if note.user == request.user:
            note.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
        
class NoteShare(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NoteSerializer

    def put(self, request, *args, **kwargs):
        try:
            note = Note.objects.get(id=self.kwargs['id'])
        except Note.DoesNotExist:
            raise NotFound()
        # print(note)
        if note.user == request.user:
            usernames = request.data.get("shared_with", [])
            shared_users = User.objects.filter(username__in=usernames)
            shared_user_pks = [user.pk for user in shared_users]
            serializer = NoteSerializer(note, data={"shared_with": shared_user_pks}, partial=True)
            # print("Its about is valid")
            if serializer.is_valid():
                # print("Its after is valid")
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

class NoteSearchView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NoteSerializer

    # we can use SearchVector for more efficient full-text search. It is case sensitive and only works with a full word
    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        notes = Note.objects.filter(user=self.request.user)
        if query:
            notes = notes.annotate(search=SearchVector('title', 'content'))
            notes = notes.filter(search=query)

        return notes

    # This method we will use if we want to search in words without case sensitive. Slower than the above one
    # def get_queryset(self):
    #     query = self.request.query_params.get('q', '')
    #     notes = Note.objects.filter(user = self.request.user)
    #     return notes.filter(Q(title__icontains=query) | Q(content__icontains=query))