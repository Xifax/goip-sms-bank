# encoding: utf-8
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = 'Example command'

    def handle(self, *args, **options):
        """
        Example command
        """
        self.stdout.write('It works!')
