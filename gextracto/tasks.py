from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from gextracto import models
from gextracto.models import BulkRequestId
from gextracto.models import TaskId
from extr import *
logger = get_task_logger(__name__)


@periodic_task(
    run_every=(crontab(minute='*/5')),
    name="retrieve_mails_per_user",
    ignore_result=True
)
def retrieve_mails_per_user():
    """
    Saves latest image from Flickr
    """
    for count in BulkRequestId.objects.all():
        user_id = count.request_id
        label_id = count.label
        task_id = TaskId.objects.filter(request_id=user_id, label=label_id)
        if task_id:
            get(user_id, label_id)
            logger.info("Saved one request mails!")
            TaskId.objects.filter(request_id = user_id, label = label_id).delete()
           
            
    logger.info("Saved mails!")
