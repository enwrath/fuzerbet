from django.contrib import admin
from betapp.models import WinnerMatch, Points, WinnerBet
# Register your models here.

class WinnerMatchAdmin(admin.ModelAdmin):
    exclude = ('player1odds','player2odds')

admin.site.register(WinnerMatch, WinnerMatchAdmin)
admin.site.register(Points)
admin.site.register(WinnerBet)
