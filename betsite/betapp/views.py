from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from betapp.models import Points, WinnerMatch, WinnerBet
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

def index(request):
    return render(request, "home.html")

@login_required
def userUpdate(request):
    data = {}
    data['points'] = Points.objects.get_or_create(id=request.user.id)[0].points
    data['winnermatches'] = list(WinnerMatch.objects.filter(canBet=True).values())
    winnerbets = WinnerBet.objects.filter(user=request.user)
    wbets = []
    for bet in winnerbets:
        b = {}
        try:
            match = WinnerMatch.objects.get(pk=bet.match.pk)
        except ObjectDoesNotExist:
            continue
            print("bet exists on non-existent match?????")
        b['player1'] = match.player1
        b['player2'] = match.player2
        b['points'] = bet.points
        b['guess'] = bet.winner
        b['winner'] = match.winner
        b['resolved'] = bet.resolved
        wbets.append(b)
    data['winnerbets'] = wbets
    return JsonResponse(data)

@login_required
def winnerBet(request):
    points = int(request.GET.get('points', '0'))
    match = int(request.GET.get('match', '-1'))
    winner = int(request.GET.get('winner', '0'))
    if match == -1 or points == 0 or winner == 0:
        return HttpResponse("Missing parameters")
    if points > Points.objects.get_or_create(id=request.user.id)[0].points:
        return HttpResponse("Not enough points")
    try:
        match = WinnerMatch.objects.get(pk=match)
    except ObjectDoesNotExist:
        return HttpResponse("No such match")
    if match.canBet == False:
        return HttpResponse("Closed")
    pointsWin = int(points * match.player1odds)
    if winner == 2: pointsWin = int(points * match.player2odds)
    bet = WinnerBet(match=match, user=request.user, points=pointsWin, winner=winner)
    bet.save()
    p = Points.objects.get(id=request.user.id)
    p.points -= points
    p.save()
    return HttpResponse("Success")
