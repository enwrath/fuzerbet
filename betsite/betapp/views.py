from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from betapp.models import Points, WinnerMatch, WinnerBet
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

def index(request):
    return render(request, "home.html")

def ranking(request):
    return render(request, "ranking.html")

@login_required
def userUpdate(request):
    data = {}
    data['points'] = Points.objects.get_or_create(user=request.user)[0].points
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
        b['payout'] = bet.payout
        wbets.append(b)
    data['winnerbets'] = wbets
    return JsonResponse(data)


def streamView(request):
    return render(request, "stream.html")

def streamUpdate(request):
    data = {}
    match = WinnerMatch.objects.latest('id')
    data['player1'] = match.player1
    data['player2'] = match.player2
    data['player1odds'] = match.player1odds
    data['player2odds'] = match.player2odds
    bets = WinnerBet.objects.filter(match=match)
    p1 = 0
    p2 = 0
    for bet in bets:
        if bet.winner == 1:
            p1 += bet.points
        else:
            p2 += bet.points
    data['player1points'] = p1
    data['player2points'] = p2
    return JsonResponse(data)

def rankingUpdate(request):
    rankings = []
    p = Points.objects.order_by('-points')
    for po in p:
        rankings.append({'name': po.user.username, 'points': po.points})
    return JsonResponse({'rankings': rankings})

@login_required
def winnerBet(request):
    points = int(request.GET.get('points', '0'))
    match = int(request.GET.get('match', '-1'))
    winner = int(request.GET.get('winner', '0'))
    if match == -1 or points <= 0 or winner == 0:
        return HttpResponse("Missing parameters")
    p = Points.objects.get_or_create(user=request.user)[0]
    if points > p.points:
        return HttpResponse("Not enough points")
    try:
        match = WinnerMatch.objects.get(pk=match)
    except ObjectDoesNotExist:
        return HttpResponse("No such match")
    if match.canBet == False:
        return HttpResponse("Closed")
    pointsWin = int(points * match.player1odds)
    if winner == 2: pointsWin = int(points * match.player2odds)
    bet = WinnerBet(match=match, user=request.user, points=points, payout=pointsWin, winner=winner)
    bet.save()
    p.points -= points
    p.save()
    return HttpResponse("Success")
