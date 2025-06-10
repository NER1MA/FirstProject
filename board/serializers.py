from rest_framework import serializers
from .models import Post, Comment

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_at']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['post-title'] = rep.pop('title')
        rep['post-content'] = rep.pop('content')
        return rep

    def to_internal_value(self, data):
        data = data.copy()
        if 'post-title' in data:
            data['title'] = data.pop('post-title')
        if 'post-content' in data:
            data['content'] = data.pop('post-content')
        return super().to_internal_value(data)

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user and request.user.is_authenticated:
            validated_data['author'] = request.user
        else:
            validated_data['author'] = None  # 익명 사용자일 경우 None으로
        return super().create(validated_data)

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'user', 'content', 'created_at']
        read_only_fields = ['author']