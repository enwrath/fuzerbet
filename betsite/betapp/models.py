from django.db import models
from django.contrib.auth.models import User

class MiscData(models.Model):
    data = models.TextField(default="")
    name = models.CharField(max_length=200)

class Points(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    points = models.DecimalField(default=100,max_digits=15, decimal_places=2)
    resets = models.IntegerField(default=0)
    def __str__(self):
        return 'Points {}'.format(self.user.username)
    class Meta:
        verbose_name_plural = "Points"

class CustomMatch(models.Model):
    title = models.CharField(max_length=200, verbose_name='Question (e.g. Is next game cannon rush)')
    player1 = models.CharField(max_length=200, verbose_name='Result 1 (e.g. Yes)')
    player2 = models.CharField(max_length=200, verbose_name='Result 2 (e.g. No)')
    player1winchance = models.IntegerField(default=50, verbose_name='Result 1 probability (%)')
    player2winchance = models.IntegerField(default=50, verbose_name='Result 2 probability (%)')
    player1odds = models.DecimalField(default=2,max_digits=11, decimal_places=2)
    player2odds = models.DecimalField(default=2,max_digits=11, decimal_places=2)
    canBet = models.BooleanField(default=True)
    winner = models.IntegerField(choices=[(0,'No result'),(1,'Result 1'),(2,'Result 2')], default=0)

    def __str__(self):
        betopen = 'Closed'
        winnerset = 'No result set '
        if self.canBet:
            betopen = 'Open'
        if self.winner != 0:
            winnerset = 'Result set '
        return '{} & {}: {}'.format(betopen, winnerset, self.title)
    class Meta:
        verbose_name_plural = "Custom Matches"

    def save(self,*args,**kwargs):
        old = CustomMatch.objects.filter(pk=self.pk).first()
        if old:
            if old.winner!=self.winner:
                winners = {}
                for bet in CustomBet.objects.filter(match=self.pk).filter(resolved=False):
                    bet.resolved = True
                    if bet.winner == self.winner:
                        p = Points.objects.get(user=bet.user)
                        p.points += bet.payout
                        p.save()
                        winners[p.user.username] = winners.get(p.user.username, 0) + float(bet.payout);
                        bet.won = True

                    bet.save()
                self.canBet = False

                if len(winners) > 0:
                    biggestwinners = "{}<br />".format(self.title, self.player1, self.player2)
                    winnerssorted = sorted(winners.items(), key=lambda x: x[1], reverse=True)
                    index = 0
                    for i in winnerssorted:
                        biggestwinners = "{}{} +{}<br />".format(biggestwinners,i[0],i[1])
                        index += 1
                        # Print at most 10 topwinners
                        if index > 10:
                            break
                    miscdata = MiscData.objects.get_or_create(name="bigwins")[0]
                    miscdata.data = biggestwinners
                    miscdata.save()


        self.player1odds = round(1/(self.player1winchance/100), 2)
        self.player2odds = round(1/(self.player2winchance/100), 2)

        super(CustomMatch,self).save(*args,**kwargs)

class WinnerMatch(models.Model):
    title = models.CharField(max_length=200)
    player1 = models.CharField(max_length=200)
    player2 = models.CharField(max_length=200)
    player1odds = models.DecimalField(default=2,max_digits=11, decimal_places=2)
    player2odds = models.DecimalField(default=2,max_digits=11, decimal_places=2)
    player1winchance = models.IntegerField(default=50, verbose_name='Player 1 win chance (%)')
    bestof = models.IntegerField(choices=[(0,'No betting on score'),(3,'Bo3'),(5,'Bo5'),(7,'Bo7')], default=3)
    canBet = models.BooleanField(default=True)
    winner = models.IntegerField(choices=[(0,'No winner'),(1,'Player 1'),(2,'Player2')], default=0)
    resW0 = models.DecimalField(default=2,max_digits=11, decimal_places=2) #with 99% winchance, we need this many numbers :D
    resW1 = models.DecimalField(default=2,max_digits=11, decimal_places=2)
    resW2 = models.DecimalField(default=2,max_digits=11, decimal_places=2)
    resW3 = models.DecimalField(default=2,max_digits=11, decimal_places=2)
    resL0 = models.DecimalField(default=2,max_digits=11, decimal_places=2)
    resL1 = models.DecimalField(default=2,max_digits=11, decimal_places=2)
    resL2 = models.DecimalField(default=2,max_digits=11, decimal_places=2)
    resL3 = models.DecimalField(default=2,max_digits=11, decimal_places=2)
    p1maps = models.IntegerField(choices=[(0,0),(1,1),(2,2),(3,3),(4,4)], default=0, verbose_name='Map wins: Player 1 (if Bo3+)')
    p2maps = models.IntegerField(choices=[(0,0),(1,1),(2,2),(3,3),(4,4)], default=0, verbose_name='Map wins: Player 2 (if Bo3+)')
    refund = models.BooleanField(default=False, verbose_name='REFUND ALL BETS!')

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
            if self.refund:
                self.canBet = False
                for bet in WinnerBet.objects.filter(match=self.pk):
                    p = Points.objects.get(user=bet.user)
                    p.points += bet.points
                    p.save()
                    bet.delete()

            elif old.winner!=self.winner:
                if self.winner == 0 and old.winner != 0:
                    #undo abort !!!
                    for bet in WinnerBet.objects.filter(match=self.pk).filter(resolved=True):
                        if bet.won == True:
                            p = Points.objects.get(user=bet.user)
                            p.points -= bet.payout
                            p.save()
                            bet.won = False
                        bet.resolved = False
                        bet.save()

                else:
                    winners = {}
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
                            winners[p.user.username] = winners.get(p.user.username, 0) + float(bet.payout);
                            p.save()
                            bet.won = True

                        bet.save()

                    self.canBet = False

                    if len(winners) > 0:
                        biggestwinners = "{} - {} vs {}<br />".format(self.title, self.player1, self.player2)
                        winnerssorted = sorted(winners.items(), key=lambda x: x[1], reverse=True)
                        index = 0
                        for i in winnerssorted:
                            biggestwinners = "{}{} +{}<br />".format(biggestwinners,i[0],i[1])
                            index += 1
                            # Print at most 10 topwinners
                            if index > 10:
                                break
                        miscdata = MiscData.objects.get_or_create(name="bigwins")[0]
                        miscdata.data = biggestwinners
                        miscdata.save()

        #prooooobably want to check that winchance is 1-99.
        #But surely admins know what they are doing!
        self.player1odds = round(1/(self.player1winchance/100), 2)
        self.player2odds = round(1/((100-self.player1winchance)/100), 2)

        wc = self.player1winchance/100
        lc = (100-self.player1winchance)/100

        print("winchance: " + str(wc) + " | " + str(lc))
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
    points = models.DecimalField(default=0,max_digits=15, decimal_places=2)
    payout = models.DecimalField(default=0,max_digits=15, decimal_places=2)
    winner = models.IntegerField(default=0)
    result = models.IntegerField(default=0)
    resolved = models.BooleanField(default=False)
    resultBet = models.BooleanField(default=False)
    won = models.BooleanField(default=False)
    def __str__(self):
        return '{} bet on {}: {} vs {}'.format(self.user.username, self.match.title, self.match.player1, self.match.player2)

class CustomBet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    match = models.ForeignKey(CustomMatch, on_delete=models.CASCADE)
    points = models.DecimalField(default=0,max_digits=15, decimal_places=2)
    payout = models.DecimalField(default=0,max_digits=15, decimal_places=2)
    winner = models.IntegerField(default=0)
    resolved = models.BooleanField(default=False)
    won = models.BooleanField(default=False)
    def __str__(self):
        return '{} bet on {}'.format(self.user.username, self.match.title)
