import os
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from ...party import PartyImporter
from ...member import MemberImporter
from ...minutes import MinutesImporter
from utils.http import HttpFetcher

class Command(BaseCommand):
    #args = '<poll_id poll_id ...>'
    help = 'Import data from the Finnish parliament'
    option_list = BaseCommand.option_list + (
        make_option('--party', action='store_true', dest='party',
                    default=False, help='Import parties'),
        make_option('--member', action='store_true', dest='member',
                    default=False, help='Import MPs'),
        make_option('--minutes', action='store_true', dest='minutes',
                    default=False, help='Import plenary session minutes'),
        make_option('--update', action='store_true', dest='update',
                    default=False, help='Update values of existing objects'),
    )

    def handle(self, *args, **options):
        http = HttpFetcher()
        http.set_cache_dir(os.path.join(settings.SITE_ROOT, '.cache'))
        if options['party']:
            importer = PartyImporter(http_fetcher=http)
            importer.replace = options['update']
            importer.import_parties()
        if options['member']:
            importer = MemberImporter(http_fetcher=http)
            importer.replace = options['update']
            importer.import_districts()
            importer.import_members()
        if options['minutes']:
            importer = MinutesImporter(http_fetcher=http)
            importer.import_minutes()