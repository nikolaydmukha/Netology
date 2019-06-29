from django.shortcuts import render
from .models import PlayerGameInfo, Player, Game


def show_home(request):
    context = {}
    request.session.modified = True
    request.session["player_id"] = request.session.session_key  # player_id = идентификатору сессии(session_key)

    # Если пришло число, то надо создать игру
    if request.method == 'POST' and 'number' in request.POST:
        request.session["game_id"] = request.POST['number']
        # Создадим игру
        insert_data = Game(number=request.POST['number'], author=request.session["player_id"])
        insert_data.save()
    elif request.method == 'POST' and 'find_number' in request.POST:
        # Счётчик попыток
        if 'attempts' not in request.session:
            request.session['attempts'] = 0
        request.session['attempts'] += 1
        hidden_number = Game.objects.get(isActive=True)
        if int(request.POST['find_number']) > int(hidden_number.number):
            context = {
                'message': 'Ваше число больше загаданного!',
                'color': 'red',
            }
        elif int(request.POST['find_number']) < int(hidden_number.number):
            context = {
                'message': 'Ваше число меньше загаданного!',
                'color': 'red',
            }
        else:
            context = {
                'message': f'Вы уагадали число с {request.session["attempts"]} попыток',
                'color': 'green',
            }
            # Вставим данные об игроке(если его еще нет в базе), игре и числе попыток
            is_player_exist = Player.objects.filter(player=request.session["player_id"])
            if not is_player_exist:
                insert_finder_player = Player(player=request.session.session_key)
                insert_finder_player.save()
            # Обновим данные о прошедей игре
            insert_finished_data_game = PlayerGameInfo(player=Player.objects.get(player=request.session["player_id"]),
                                                       game=Game.objects.get(number=hidden_number.number, isActive=True),
                                                       attempt=request.session['attempts'])
            insert_finished_data_game.save()
            # Пометим игру, как завершенную
            update_game = Game.objects.filter(isActive=True)
            update_game.update(isActive=False)
            # Обнулим счётчик
            request.session['attempts'] = 0
    else:
        # Выясним, есть ли активные игры
        active_game = Game.objects.filter(isActive=True)
        if not active_game:
            context = {
                'active_game': False,
            }
        else:
            for act_game in active_game:
                # Если player_id == id создателя игры, то для него должны вывести загулшку "Вы загадали.."
                if request.session["player_id"] == act_game.author:
                    # Получим информацию об игре, которую отгадали, и выведеёс инф. о ней автору
                    finished_game = PlayerGameInfo.objects.filter(game__author=request.session["player_id"],
                                                                  game__number=request.session["game_id"])
                    print("OPAOPAOPAOPAOAP====> ", finished_game)
                    context = {
                        'game_id': act_game.number,
                    }
                else:
                    context = {
                        'active_game': True,
                    }
    request.session.save()
    return render(
        request,
        'home.html',
        context
    )
