from django.contrib import admin
from .models import Notification
from .tasks import update_notification_task, delete_notifications_task

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('notification_id', 'title', 'message', 'created_at', 'opened_at', 'status', 'customer')

    # Define the action to delete notifications older than 7 days
    actions = ['delete_old_notifications_action']

    def delete_old_notifications_action(self, request, queryset):
        """
        Admin action to schedule Celery tasks for handling old notifications.
        """
        # Schedule Celery tasks
        update_notification_task.apply_async()
        delete_notifications_task.apply_async()
        
        # Provide feedback to the admin
        self.message_user(
            request,
            "Tasks to update and delete notifications older than 7 days have been scheduled."
        )

    delete_old_notifications_action.short_description = "Delete notifications older than 7 days"

admin.site.register(Notification, NotificationAdmin)
