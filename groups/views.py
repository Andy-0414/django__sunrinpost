
from django.shortcuts import render
from rest_framework import viewsets, permissions
from .serializers import GroupSerializer, PostSerializer, CommentSerializer
from .models import Group, Post, Comment

from rest_framework.decorators import action
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user


class GroupView(viewsets.ModelViewSet):
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def retrieve(self, request, pk=None):
        group = Group.objects.get(pk=pk)
        group.visit += 1
        group.save()
        serializer = GroupSerializer(group)
        return Response(serializer.data)


class PostView(viewsets.ModelViewSet):
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        group = Group.objects.get(pk=self.kwargs.get('group'))
        serializer.save(owner=self.request.user,
                        group=group)

    def get_queryset(self):
        group = self.kwargs.get('group')
        if group:
            return Post.objects.select_related('group').filter(group__pk=group)
        else:
            return Post.objects.all()

    def retrieve(self, request, pk=None, group=None):
        post = Post.objects.get(pk=pk)
        post.visit += 1
        post.save()
        serializer = PostSerializer(post)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_recommend(self, request, pk=None, group=None):
        print("TEST")
        post = Post.objects.get(pk=pk)
        post.recommend += 1
        post.save()
        serializer = PostSerializer(post)
        return Response(serializer.data)


class CommentView(viewsets.ModelViewSet):
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        post = self.kwargs.get('post')
        if post:
            return Comment.objects.select_related('post').filter(post__pk=post)
        else:
            return Comment.objects.all()
