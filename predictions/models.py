from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



class Team(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=10)
    def __str__(self):
        return self.name

class Match(models.Model):
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team1_matches')
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team2_matches')
    date = models.DateTimeField(default=timezone.now) 
    winner = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='winning_matches', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) 

    def __str__(self):
        return f"{self.team1} vs {self.team2} on {self.date}"

class Prediction(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chosen_winner = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} predicted {self.chosen_winner} for {self.match}"
