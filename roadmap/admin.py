from django.contrib import admin
from .models import Roadmap, TaskNode, UserTaskProgress


@admin.register(Roadmap)
class RoadmapAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title',)


@admin.register(TaskNode)
class TaskNodeAdmin(admin.ModelAdmin):
    list_display = ('title', 'roadmap', 'parent')
    list_filter = ('roadmap',)
    search_fields = ('title',)


@admin.register(UserTaskProgress)
class UserTaskProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'task', 'is_completed', 'deadline')
    list_filter = ('is_completed', 'deadline')
    