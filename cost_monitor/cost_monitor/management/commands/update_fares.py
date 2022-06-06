from django.core.management.base import BaseCommand, CommandError

from playwright.sync_api import Playwright, sync_playwright

from cost_monitor.models import Journey, Fare, Connection
from cost_monitor.scrape_bahn import extract_fares

class Command(BaseCommand):
    help = 'Updates the fares for all journeys'

    def handle(self, *args, **options):
        journeys = Journey.objects.all()
        
        for journey in journeys:
            with sync_playwright() as playwright:
                connections, fares = extract_fares(playwright, journey)

            assert connections is not None, "Was not able to find any connections!"

            for connection, fare in zip(connections, fares):
                connection, created = Connection.objects.get_or_create(journey=journey, start_time=connection.start_time, end_time=connection.end_time)
                fare_object = Fare(connection=connection, fare=fare)
                fare_object.save()
                connection.fares.add(fare_object)

            journey.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully updated fare information for Journey "{journey}"'))