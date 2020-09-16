from django.db import models
from django.contrib.auth.models import User

class Points(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=100)
    def __str__(self):
        return 'Points {}'.format(self.user.username)
    class Meta:
        verbose_name_plural = "Points"

class WinnerMatch(models.Model):
    title = models.CharField(max_length=200)
    player1 = models.CharField(max_length=200)
    player2 = models.CharField(max_length=200)
    player1odds = models.DecimalField(default=2,max_digits=5, decimal_places=2)
    player2odds = models.DecimalField(default=2,max_digits=5, decimal_places=2)
    player1winchance = models.IntegerField(default=50, verbose_name='Player 1 win chance (%)')
    canBet = models.BooleanField(default=True)
    winner = models.IntegerField(choices=[(0,'No winner'),(1,'Player 1'),(2,'Player2')], default=0)
    def __str__(self):
        betopen = 'Closed'
        winnerset = 'No winner set '
        if self.canBet:
            betopen = 'Open'
        if self.winner != 0:
            winnerset = 'Winner set '
        return '{} & {}: {}: {} vs {}'.format(betopen, winnerset, self.title, self.player1, self.player2)
    class Meta:
        verbose_name_plural = "Winner Matches"
    def save(self,*args,**kwargs):
        old = WinnerMatch.objects.filter(pk=self.pk).first()
        if old:
            if old.winner!=self.winner:
                for bet in WinnerBet.objects.filter(match=self.pk).filter(resolved=False):
                    bet.resolved = True
                    if bet.winner == self.winner:
                        p = Points.objects.get(user=bet.user)
                        p.points += bet.payout
                        p.save()
                    bet.save()
                self.canBet = False
        else:
            #When new match is added, users get bumped to 100 points if they have less
            lowpoints =  Points.objects.filter(points__lt=100)
            for p in lowpoints:
                p.points = 100
                p.save()

        #prooooobably want to check that winchance is 1-99.
        #But surely admins know what they are doing!
        self.player1odds = round(1/(self.player1winchance/100), 2)
        self.player2odds = round(1/((100-self.player1winchance)/100), 2)
        super(WinnerMatch,self).save(*args,**kwargs)

class WinnerBet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    match = models.ForeignKey(WinnerMatch, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    payout = models.IntegerField(default=0)
    winner = models.IntegerField(default=0)
    resolved = models.BooleanField(default=False)
    def __str__(self):
        return '{} bet on {}: {} vs {}'.format(self.user.username, self.match.title, self.match.player1, self.match.player2)
