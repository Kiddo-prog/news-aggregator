import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
from django.core.management.base import BaseCommand

import feedparser
from dateutil import parser
from pytz import timezone
from news_app.models import Article

# title description, url, pub_date, image
logger = logging.getLogger(__name__)


def save_new_articles(feed):
    news_title = feed.channel.title
    # news_image = feed.channel.image["href"]
    for item in feed.entries:
        if not Article.objects.filter(guid=item.guid).exists():
            article = Article(
                name=news_title,
                title=item.title,
                description=item.description,
                pub_date=parser.parse(item.published),
                url=item.link,
                image=item.img,
                guid=item.guid,
            )
            article.save()


def save_nytimes_news_articles():
    _feed = feedparser.parse(
        "https://www.nytimes.com/svc/collections/v1/publish/https://www.nytimes.com/section/world/rss.xml"
    )
    save_new_articles(_feed)


def save_cbs_world_news_articles():
    _feed = feedparser.parse("https://www.cbsnews.com/latest/rss/world")
    save_new_articles(_feed)

def save_google_new_feed():
    _feed = feedparser.parse("https://news.google.com/rss?hl=en-NG&gl=NG&ceid=NG%3Aen&oc=11")
    save_new_articles(_feed)

def save_247_news_around_the_world_articles():
    _feed = feedparser.parse("https://247newsaroundtheworld.com/feed/")
    save_new_articles(_feed)

# def save_

def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # Scheduler for nytimes feeds

        scheduler.add_job(
            save_nytimes_news_articles,
            trigger="interval",
            max_instances=2,
            minutes=2,
            id="NY Times",
            replace_existing=True,
        )
        logger.info("Added job 'NY Times'.")

        scheduler.add_job(
            save_247_news_around_the_world_articles,
            trigger="interval",
            max_instances=2,
            minutes=10,
            id="247 News Around The World",
            replace_existing=True,
        )
        logger.info("Added job '247 News'.")

        # Scheduler for cbs feeds
        scheduler.add_job(
            save_cbs_world_news_articles,
            trigger="interval",
            max_instances=2,
            minutes=10,
            id="CBS Times",
            replace_existing=True,
        )
        logger.info("Added job 'CBS Times'.")

        scheduler.add_job(
            save_google_new_feed,
            trigger="interval",
            max_instances=2,
            minutes=10,
            id="CBS Times",
            replace_existing=True,
        )
        logger.info("Added job 'CBS Times'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")