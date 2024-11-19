from django.contrib import admin
from .models import Notification
# Register your models here.
from .models import Notification
from .task import delete_notifications_task, expire_notifications  # Import the Celery task

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('notification_id', 'message', 'created_at', 'title', 'message', 'opened_at', 'status', 'customer')
    
    # Define the action to delete notifications older than 7 days
    actions = ['delete_old_notifications_action']
    
    def delete_old_notifications_action(self, request, queryset):
        """Action to delete notifications older than 7 days."""
        # Call the Celery task
        delete_notifications_task.apply_async()
        expire_notifications.apply_async()
        self.message_user(request, "Scheduled the task to delete notifications older than 7 days.")
    delete_old_notifications_action.short_description = "Delete notifications older than 7 days"

admin.site.register(Notification, NotificationAdmin)
