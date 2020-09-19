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
    bestof = models.IntegerField(choices=[(0,'No betting on score'),(3,'Bo3'),(5,'Bo5'),(7,'Bo7')], default=3)
    canBet = models.BooleanField(default=True)
    winner = models.IntegerField(choices=[(0,'No winner'),(1,'Player 1'),(2,'Player2')], default=0)
    resW0 = models.DecimalField(default=2,max_digits=5, decimal_places=2)
    resW1 = models.DecimalField(default=2,max_digits=5, decimal_places=2)
    resW2 = models.DecimalField(default=2,max_digits=5, decimal_places=2)
    resW3 = models.DecimalField(default=2,max_digits=5, decimal_places=2)
    resL0 = models.DecimalField(default=2,max_digits=5, decimal_places=2)
    resL1 = models.DecimalField(default=2,max_digits=5, decimal_places=2)
    resL2 = models.DecimalField(default=2,max_digits=5, decimal_places=2)
    resL3 = models.DecimalField(default=2,max_digits=5, decimal_places=2)
    p1maps = models.IntegerField(choices=[(0,0),(1,1),(2,2),(3,3),(4,4)], default=0, verbose_name='Map wins: Player 1 (if Bo3+)')
    p2maps = models.IntegerField(choices=[(0,0),(1,1),(2,2),(3,3),(4,4)], default=0, verbose_name='Map wins: Player 2 (if Bo3+)')

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
                    won = False
                    if not bet.resultBet and bet.winner == self.winner: won=True
                    elif bet.resultBet:
                        if self.bestof == 3:
                            if bet.result == 0 and self.p1maps==2 and self.p2maps==0: won=True
                            elif bet.result == 1 and self.p1maps==2 and self.p2maps==1: won=True
                            elif bet.result == 2 and self.p1maps==1 and self.p2maps==2: won=True
                            elif bet.result == 3 and self.p1maps==0 and self.p2maps==2: won=True
                        elif self.bestof == 5:
                            if bet.result == 0 and self.p1maps==3 and self.p2maps==0: won=True
                            elif bet.result == 1 and self.p1maps==3 and self.p2maps==1: won=True
                            elif bet.result == 2 and self.p1maps==3 and self.p2maps==2: won=True
                            elif bet.result == 3 and self.p1maps==2 and self.p2maps==3: won=True
                            elif bet.result == 4 and self.p1maps==1 and self.p2maps==3: won=True
                            elif bet.result == 5 and self.p1maps==0 and self.p2maps==3: won=True
                        elif self.bestof == 7:
                            if bet.result == 0 and self.p1maps==4 and self.p2maps==0: won=True
                            elif bet.result == 1 and self.p1maps==4 and self.p2maps==1: won=True
                            elif bet.result == 2 and self.p1maps==4 and self.p2maps==2: won=True
                            elif bet.result == 3 and self.p1maps==4 and self.p2maps==3: won=True
                            elif bet.result == 4 and self.p1maps==3 and self.p2maps==4: won=True
                            elif bet.result == 5 and self.p1maps==2 and self.p2maps==4: won=True
                            elif bet.result == 6 and self.p1maps==1 and self.p2maps==4: won=True
                            elif bet.result == 7 and self.p1maps==0 and self.p2maps==4: won=True
                    if won:
                        p = Points.objects.get(user=bet.user)
                        p.points += bet.payout
                        p.save()
                        bet.won = True

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

        wc = self.player1winchance/100
        lc = (100-self.player1winchance)/100
        if self.bestof == 3:
            self.resW0 = round(1/(wc*wc), 2)
            self.resW1 = round(1/(2*wc*wc*lc), 2)
            self.resL1 = round(1/(2*lc*lc*wc), 2)
            self.resL0 = round(1/(lc*lc), 2)
        elif self.bestof == 5:
            self.resW0 = round(1/(wc*wc*wc), 2)
            self.resW1 = round(1/(3*wc*wc*wc*lc), 2)
            self.resW2 = round(1/(6*wc*wc*wc*lc*lc), 2)
            self.resL2 = round(1/(6*wc*wc*lc*lc*lc), 2)
            self.resL1 = round(1/(3*lc*lc*lc*wc), 2)
            self.resL0 = round(1/(lc*lc*lc), 2)
        elif self.bestof == 7:
            self.resW0 = round(1/(wc*wc*wc*wc), 2)
            self.resW1 = round(1/(4*wc*wc*wc*wc*lc), 2)
            self.resW2 = round(1/(10*wc*wc*wc*wc*lc*lc), 2)
            self.resW3 = round(1/(20*wc*wc*wc*wc*lc*lc*lc), 2)
            self.resL3 = round(1/(20*wc*wc*wc*lc*lc*lc*lc), 2)
            self.resL2 = round(1/(10*wc*wc*lc*lc*lc*lc), 2)
            self.resL1 = round(1/(4*lc*lc*lc*lc*wc), 2)
            self.resL0 = round(1/(lc*lc*lc*lc), 2)
        super(WinnerMatch,self).save(*args,**kwargs)

class WinnerBet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    match = models.ForeignKey(WinnerMatch, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    payout = models.IntegerField(default=0)
    winner = models.IntegerField(default=0)
    result = models.IntegerField(default=0)
    resolved = models.BooleanField(default=False)
    resultBet = models.BooleanField(default=False)
    won = models.BooleanField(default=False)
    def __str__(self):
        return '{} bet on {}: {} vs {}'.format(self.user.username, self.match.title, self.match.player1, self.match.player2)
