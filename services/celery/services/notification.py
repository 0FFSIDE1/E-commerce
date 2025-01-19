from datetime import datetime, timedelta
from notifications.models import Notification
from django.db.models import Q
import logging
from django.db import DatabaseError


# Set up logging
logger = logging.getLogger(__name__)

def expire_notifications():
    """
    Marks notifications unread for more than 7 days as expired.
    """
    try:
        logger.info("Starting to expire unread notifications.")
        
        # Calculate the cutoff date for unread notifications
        seven_days_ago = datetime.now() - timedelta(days=7)
        
        # Query for unopened notifications older than 7 days
        unopened_notifications = Notification.objects.get(
            opened_at__isnull=True,
            created_at__lte=seven_days_ago,
            status="unread"
        )
        
        # Update the status of those notifications to 'expired'
        updated_count = unopened_notifications.update(status="expired")
        
        logger.info(f"{updated_count.count()} notifications marked as expired.")
    
    except DatabaseError as db_error:
        logger.error(f"Database error while expiring notifications: {db_error}")
        raise
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise
    else:
        logger.info("Notification expiration process completed successfully.")

    
def delete_notifications():
    """
    Deletes all notifications with status 'read' or 'expired'.
    """
    try:
        logger.info("Starting deletion of 'read' and 'expired' notifications.")
        
        # Query for notifications to delete
        read_notifications = Notification.objects.filter(
            Q(status='read') | Q(status='expired')
        )
        
        # Count notifications before deletion for logging
        count = read_notifications.count()
        
        # Delete the notifications
        read_notifications.delete()
        
        logger.info(f"Successfully deleted {count} notifications.")
    
    except DatabaseError as db_error:
        logger.error(f"Database error while deleting notifications: {db_error}")
        raise
    except Exception as e:
        logger.error(f"An unexpected error occurred while deleting notifications: {e}")
        raise
    else:
        logger.info("Notification deletion process completed successfully.")
