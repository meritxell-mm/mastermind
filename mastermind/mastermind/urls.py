from django.urls import include, path

urlpatterns = [
    path('mastermind/', include('game.urls'))
]
