from django.contrib import admin

from .models import Post, PostImage, Comment, LikedComment, LikedPost, Tag


admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(PostImage)
admin.site.register(Comment)
admin.site.register(LikedComment)
admin.site.register(LikedPost)