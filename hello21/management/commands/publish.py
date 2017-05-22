import logging
import sys
from datetime import datetime

from django.core.management.base import BaseCommand

from hello21 import settings

from two1.commands import publish
from two1.server import rest_client


class Command(BaseCommand):
    help = 'Publish your app to the marketplace'

    def __init__(self):
        super().__init__()
        self._logger = logging.getLogger('hello21.publish')
        logging.basicConfig(stream=sys.stdout, level=logging.INFO)
        self._username = settings.TWO1_USERNAME
        self._client = rest_client.TwentyOneRestClient(
            username=self._username, wallet=settings.WALLET
        )

    def handle(self, *args, **options):
        manifest_path = 'hello21/manifest.yaml'
        app_name = 'hello 21'
        try:
            publish._publish(self.client, manifest_path, '21market', True, {})
            self._logger.info(
                '%s publishing %s - published: True, Timestamp: %s' %
                (self._username, app_name, datetime.now())
            )
        except Exception as e:
            self._logger.error(
                '%s publishing %s - published: False, error: %s, Timestamp: %s' %
                (self._username, app_name, e, datetime.now())
            )
