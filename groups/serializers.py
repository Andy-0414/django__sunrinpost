
from rest_framework import serializers, permissions
from .models import Group, Post, Comment

class GroupSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Group
        fields = (
            'name',
            'visit',
            'owner',
            'pk'
        )

class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Post
        fields = (
            'title',
            'content',
            'visit',
            'recommend',
            'owner',
            'group',
            'pk',
            'created_at',
        )
        read_only_fields = ('created_at',)


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Comment
        fields = (
            'content',
            'owner',
            'post',
            'pk',
            'created_at',
        )
        read_only_fields = ('created_at',)
