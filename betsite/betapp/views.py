from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from betapp.models import Points, WinnerMatch, WinnerBet, CustomMatch, CustomBet, MiscData
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
    data['custommatches'] = list(CustomMatch.objects.filter(canBet=True).values())
    winnerbets = WinnerBet.objects.filter(user=request.user)
    custombets = CustomBet.objects.filter(user=request.user)
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
        b['result'] = bet.result
        b['winner'] = match.winner
        b['resolved'] = bet.resolved
        b['payout'] = bet.payout
        b['title'] = match.title
        b['won'] = bet.won
        b['resultBet'] = bet.resultBet
        b['bestof'] = match.bestof
        wbets.append(b)
    cbets = []
    for bet in custombets:
        b = {}
        try:
            match = CustomMatch.objects.get(pk=bet.match.pk)
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
        b['title'] = match.title
        b['won'] = bet.won
        cbets.append(b)

    data['winnerbets'] = wbets
    data['custombets'] = cbets
    return JsonResponse(data)


def streamView(request):
    return render(request, "stream.html")

def streamView2(request):
    return render(request, "stream2.html")

def streamView3(request):
    return render(request, "stream3.html")

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

def bigWinUpdate(request):
    miscdata = MiscData.objects.get_or_create(name="bigwins")[0]
    return JsonResponse({'wins': miscdata.data})

@login_required
def winnerBet(request):
    points = float(request.GET.get('points', '0'))
    match = int(request.GET.get('match', '-1'))
    winner = int(request.GET.get('winner', '0'))
    result = int(request.GET.get('result', '-1'))
    if match == -1 or points <= 0 or (winner == 0 and result == -1):
        return JsonResponse({'good': False, 'msg': 'Puuttellinen veikkauspyyntö.'})
    p = Points.objects.get_or_create(user=request.user)[0]
    if points > p.points:
        #Pyöristetään jos on näin lähellä
        #Desimaalit, never again
        if (points - float(p.points) < 0.02):
            points = float(p.points)
        else:
            return JsonResponse({'good': False, 'msg': 'Ei riittävästi pisteitä.'})
    try:
        match = WinnerMatch.objects.get(pk=match)
    except ObjectDoesNotExist:
        return JsonResponse({'good': False, 'msg': 'Veikkauskohdetta ei löytynyt.'})
    if match.canBet == False:
        return JsonResponse({'good': False, 'msg': 'Veikkauskohde on jo sulkeutunut.'})
    pointsWin = points * float(match.player1odds)
    if winner == 2: pointsWin = points * float(match.player2odds)

    if result != -1: #Oispa array käytettävissäääääääh
        w = 1
        if match.bestof == 3:
            if result == 0: pointsWin = points * float(match.resW0)
            if result == 1: pointsWin = points * float(match.resW1)
            if result == 2: pointsWin = points * float(match.resL1)
            if result == 3: pointsWin = points * float(match.resL0)
            if result > 1: w = 2
        elif match.bestof == 5:
            if result == 0: pointsWin = points * float(match.resW0)
            if result == 1: pointsWin = points * float(match.resW1)
            if result == 2: pointsWin = points * float(match.resW2)
            if result == 3: pointsWin = points * float(match.resL2)
            if result == 4: pointsWin = points * float(match.resL1)
            if result == 5: pointsWin = points * float(match.resL0)
            if result > 2: w = 2
        else:
            if result == 0: pointsWin = points * float(match.resW0)
            if result == 1: pointsWin = points * float(match.resW1)
            if result == 2: pointsWin = points * float(match.resW2)
            if result == 3: pointsWin = points * float(match.resW3)
            if result == 4: pointsWin = points * float(match.resL3)
            if result == 5: pointsWin = points * float(match.resL2)
            if result == 6: pointsWin = points * float(match.resL1)
            if result == 7: pointsWin = points * float(match.resL0)
            if result > 3: w = 2
        bet = WinnerBet(match=match, user=request.user, points=points, payout=pointsWin, winner=w, result=result, resultBet=True)
    else:
        bet = WinnerBet(match=match, user=request.user, points=points, payout=pointsWin, winner=winner, resultBet=False)

    bet.save()
    p.points = float(p.points) - points
    p.save()
    return JsonResponse({'good': True, 'msg': 'Veto rekisteröity.'})

@login_required
def customBet(request):
    points = float(request.GET.get('points', '0'))
    match = int(request.GET.get('match', '-1'))
    winner = int(request.GET.get('winner', '0'))
    if match == -1 or points <= 0 or winner == 0:
        return JsonResponse({'good': False, 'msg': 'Puuttellinen veikkauspyyntö.'})
    p = Points.objects.get_or_create(user=request.user)[0]
    if points > p.points:
        #Pyöristetään jos on näin lähellä
        #Desimaalit, never again
        if (points - float(p.points) < 0.02):
            points = float(p.points)
        else:
            return JsonResponse({'good': False, 'msg': 'Ei riittävästi pisteitä.'})
    try:
        match = CustomMatch.objects.get(pk=match)
    except ObjectDoesNotExist:
        return JsonResponse({'good': False, 'msg': 'Veikkauskohdetta ei löytynyt.'})
    if match.canBet == False:
        return JsonResponse({'good': False, 'msg': 'Veikkauskohde on jo sulkeutunut.'})
    pointsWin = points * float(match.player1odds)
    if winner == 2: pointsWin = points * float(match.player2odds)

    bet = CustomBet(match=match, user=request.user, points=points, payout=pointsWin, winner=winner)

    bet.save()
    p.points = float(p.points) - points
    p.save()
    return JsonResponse({'good': True, 'msg': 'Veto rekisteröity.'})

@login_required
def resetUser(request):
    p = Points.objects.get_or_create(user=request.user)[0]
    p.points = 100
    p.resets = p.resets + 1
    p.save()

    WinnerBet.objects.filter(user=request.user).delete()
    return JsonResponse({'good': True, 'msg': 'Pisteet ja vedot nollattu.'})
