# management/commands/populate_data.py
from django.core.management.base import BaseCommand
from predictions.models import Team, Match
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **options):
        # Check if teams already exist
        if Team.objects.exists():
            self.stdout.write(self.style.SUCCESS('Teams already exist. Skipping team creation.'))
        else:
            # Create Indian IPL team names with short names
            team_data = [
                {'name': 'Chennai Super Kings', 'short_name': 'CSK'},
                {'name': 'Delhi Capitals', 'short_name': 'DC'},
                {'name': 'Kolkata Knight Riders', 'short_name': 'KKR'},
                {'name': 'Mumbai Indians', 'short_name': 'MI'},
                {'name': 'Punjab Kings', 'short_name': 'PBKS'},
                {'name': 'Rajasthan Royals', 'short_name': 'RR'},
                {'name': 'Royal Challengers Bangalore', 'short_name': 'RCB'},
                {'name': 'Sunrisers Hyderabad', 'short_name': 'SRH'},
                {'name': 'Gujarat Titans', 'short_name': 'GT'},
                {'name': 'Lucknow Supergiants', 'short_name': 'LS'},
            ]

            # Create teams
            for data in team_data:
                Team.objects.create(name=data['name'], short_name=data['short_name'])

            self.stdout.write(self.style.SUCCESS('Teams added successfully.'))

        # Create matches
        team_count = Team.objects.count()
        for i in range(team_count):
            for j in range(i + 1, team_count):
                Match.objects.create(
                    team1=Team.objects.all()[i],
                    team2=Team.objects.all()[j],
                    date=timezone.now() + timezone.timedelta(days=i + j)
                )

        self.stdout.write(self.style.SUCCESS('Match objects added successfully'))
