"""
This file illustrates several techniques:
- how to store user object (session + user) in Alice
- how to extract intents from Yandex native NLU
"""

import dialogic


class ExampleDialogManager(dialogic.dialog_manager.BaseDialogManager):
    def respond(self, ctx):
        if ctx.source != dialogic.SOURCES.ALICE:
            return dialogic.dialog.Response('Простите, но я работаю только в Алисе.')
        suggests = []#['меня зовут иван', 'как меня зовут', 'сколько было сессий', 'повтори']
        uo = ctx.user_object
        if 'user' not in uo:
            uo['user'] = {}
        if 'session' not in uo:
            uo['session'] = {}

        intents = ctx.yandex.request.nlu.intents
        if ctx.session_is_new():
            uo['user']['sessions'] = uo['user'].get('sessions', 0) + 1
            text = 'Доброго времени суток! Навык "Семейный разговор" активирован.'
        else:
            d = {
                    'больно' : 'Ребёнку больно.',
                    'упал' : 'Ой, ребенок упал. Будьте осторожны и предложите ему помощь.',
                    'порезался' : 'Кажется, ребенок порезался. Необходимо обработать ранку и дать утешение.',
                    'завтракать' : 'Ребенок хочет завтракать. Время для восстановления сил!',
                    'обедать' : 'Ребенок хочет обедать. Не забудьте про разнообразное питание!',
                    'ужинать' : 'Ребенок хочет ужинать. Важно закончить день с полезным ужином.',
                    'есть' : 'Ребенок просит есть. Предложите что-то вкусное!',
                    'фрукты' :'Ребенок хочет фруктов. Время для витаминов и полезных веществ!',
                    'помощь' : 'Ребенок просит помощи. Объясните, что случилось и как вы можете помочь.',
                    'подойти' :'Ребенок просит вас подойти к нему. Обратите внимание на него.',
                    'попить' : 'Ребенок просит попить. Важно поддерживать гидратацию!',
                    'гулять' : 'Ребенок хочет погулять. Свежий воздух всегда полезен.',
                    'помочь сделать поделку' : 'Ребенок просит помочь сделать поделку. Проявите креативность и поддержите идею!',
                    'лепить из пластилина' : 'Ребенок хочет лепить из пластилина. Предложите скатывать мелкие шарики и создавать что-то новое!',
                    'рисовать' : 'Ребенок хочет рисовать. Дайте ему возможность выразить свою фантазию!',
                    'приготовить еду сам' : 'Ребенок хочет приготовить еду сам. Старайтесь контролировать процесс и объяснять, как правильно работать с кухонными инструментами.',
                    'а' : 'Ребенок кричит «ААА». Попробуйте успокоить его и выяснить, что случилось.',
                    'играть' :'Ребенок хочет играть. Найдите время для веселых игр и развлечений!',
                    'спать' : 'Ребенок хочет спать. Важно соблюдать режим сна и создавать уютную обстановку для отдыха.',
                    'проснулся' :'Ребенок проснулся. Поздравляем с новым днем! Подготовьте завтрак и план на день.',
                    'мама': 'Ребёнок зовёт маму.',
                    'папа': "Ребёнок зовёт папу."
            }
            tokens = ctx.yandex.request.nlu.tokens
            text = f'Неизвестная ситуация. Текст, который навык смог различить в речи: \n \
                            {data["request"]["original_utterance"]}'
            for key in d.keys():
                if key in tokens:
                    text = d[key]
                    break
        uo['session']['last_phrase'] = text
        return dialogic.dialog_manager.Response(user_object=uo, text=text, suggests=suggests)


if __name__ == '__main__':
    connector = dialogic.dialog_connector.DialogConnector(
        dialog_manager=ExampleDialogManager(),
        alice_native_state=True,
    )
    server = dialogic.server.flask_server.FlaskServer(connector=connector)
    server.parse_args_and_run()
