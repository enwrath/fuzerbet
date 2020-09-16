from django.contrib import admin
from betapp.models import WinnerMatch, Points, WinnerBet
# Register your models here.

class WinnerMatchAdmin(admin.ModelAdmin):
    exclude = ('player1odds','player2odds','resL0','resL1','resL2','resL3','resW0','resW1','resW2','resW3')

admin.site.register(WinnerMatch, WinnerMatchAdmin)
admin.site.register(Points)
admin.site.register(WinnerBet)
