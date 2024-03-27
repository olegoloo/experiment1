from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'testapp'
    PLAYERS_PER_GROUP = 4
    NUM_ROUNDS = 1



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):

    def drugone(group):
        return group.get_player_by_id(1)

    def drugtwo(group):
        return group.get_player_by_id(2)

    def drugthree(group):
        return group.get_player_by_id(3)

    def drugfour(group):
        return group.get_player_by_id(4)

    def sum_offer(group):
        return (group.get_player_by_id(1).offer
                + group.get_player_by_id(2).offer
                + group.get_player_by_id(2).offer)

    def ost(group):
        if (group.sum_offer()) > 450:
            return (f'Оставшиеся средства будут получены случайным игроком. Остаток ${group.sum_offer() - 450} '
                    f'будет получен случайным игроком.')
        else:
            return (" ")

    def results(group):
        if (group.get_player_by_id(1).offer
                + group.get_player_by_id(2).offer
                + group.get_player_by_id(2).offer) > 450:
            return ('Отлично! Вам удалось набрать минимально необходимую сумму. '
                    'Пострадавшему удалось вернуть все потерянные средства.')
        else:
            return ('К сожалению, необходимую сумму набрать не удалось. Все вложенные средства сгорели,'
                    ' пострадавшему не удалось вернуть потерянные средства.')


class Player(BasePlayer):
    name = models.StringField(label="Имя", blank=True, initial="не указана")
    surname = models.StringField(label="Фамилия", blank=True, initial="не указана")
    age = models.IntegerField(label='Укажите свой возраст', blank=True, initial=5)
    gender = models.StringField(label="Укажите ваш пол",
                                choices=['Мужчина', 'Женщина'],
                                widget=widgets.RadioSelect, blank=True)
    program = models.StringField(label="Если вы учитесь в НИУ ВШЭ, напишите свою программу, если нет, "
                                       "оставьте поле пустым.", blank=True, initial="не указана")

    balance = models.IntegerField(initial=1000)
    porog_small = models.IntegerField(initial=450)

    offer = models.IntegerField(label='Размер пожертвования:', min=0, max=1000)



    def role(self):
        if self.id_in_group == 1:
            return 'Донор'
        elif self.id_in_group == 2:
            return 'Донор'
        elif self.id_in_group == 3:
            return 'Донор'
        else:
            return 'Пострадавший'


    def set_payoff(self):
        if self.id_in_group != 4:
            return self.balance - self.offer
        else:
            return (self.balance + self.get_others_in_group()[0].offer
                    + self.get_others_in_group()[1].offer + self.get_others_in_group()[2].offer)

    def sum_offer(self):
        return (self.get_others_in_group()[0].offer
                    + self.get_others_in_group()[1].offer
                + self.get_others_in_group()[2].offer)

class MyPage(Page):
    form_model = 'player'


class ResultsWaitPage(WaitPage):
    pass


class MyPageResults(Page):
    def is_displayed(self):
        return self.id_in_group != 4
    form_model = 'player'
    form_fields = ['offer']


class MyPageResultsrecip(Page):
    def is_displayed(self):
        return self.id_in_group == 4


class PageDonor(Page):
    form_model = 'player'
    form_fields = ['offer']

    def is_displayed(self):
        return self.id_in_group != 4


class PageRecipient(Page):

    def is_displayed(self):
        return self.id_in_group == 4




class ChoiseWaitPage(WaitPage):
    def is_displayed(self):
        return self.id_in_group == 4


class RecipientResult(Page):
    def is_displayed(self):
        return self.id_in_group == 4


class DonorResult(Page):
    def is_displayed(self):
        return self.id_in_group != 4


class FinalPage(Page):
    form_model = 'group'




page_sequence = [MyPage, ResultsWaitPage, MyPageResults, MyPageResultsrecip,
                 ChoiseWaitPage, DonorResult, ResultsWaitPage, FinalPage]
