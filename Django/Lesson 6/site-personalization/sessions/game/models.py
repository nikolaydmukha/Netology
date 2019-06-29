from django.db import models


class Player(models.Model):
    player = models.CharField(max_length=256, verbose_name='Идентификатор игрока')

    def __str__(self):
        return self.player


class Game(models.Model):
    number = models.IntegerField(default=False, verbose_name='Загаданное число',)
    author = models.CharField(max_length=256, verbose_name='Идентификатор автора')
    player = models.ManyToManyField(Player, through='PlayerGameInfo', blank=True)
    isActive = models.BooleanField(default=True)


class PlayerGameInfo(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    attempt = models.IntegerField(default=False, verbose_name='Число попыток')
