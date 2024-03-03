from otree.api import *


doc = """
Introduction to CS_Game Rule
"""


class C(BaseConstants):
    NAME_IN_URL = 'Introduction'
    PLAYERS_PER_GROUP = None
    STAGE = 1
    NUM_ROUNDS = 1
    NUMBER_OF_ROUNDS = 5                # rounds in the game, for the instructions
    NUM_CUBICLES = 24                   # maximum cubicle number
    INITIAL_TREES = 100
    ENDOWMENT = 50
    INCOME = 0
    LIFE_COSTS = 0
    MULTIPLIER_TAKE = 2                 # multiplier for trees taken out
    SHOWUP_FEE = cu(4.00)
    CENTS = 9 ########## not necessary and different from the other apps! Hardcoded in Instructions.html!



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


def my_field(label):
    return models.IntegerField(choices=[[1, "Ja"], [0, "Nein"], [2, "Kann man pauschal nicht sagen."]], 
                               widget=widgets.RadioSelectHorizontal, label=label)

class Player(BasePlayer):
    code = models.IntegerField() # for ComprehensionSuccess
    #cubicle = models.IntegerField(min=1, max=C.NUM_CUBICLES, label = "Bitte tragen Sie hier Ihre Kabinennummer ein:")
    compr1 = my_field("1. Erhalten Sie Punkte für die Anzahl der Bäume, die am Ende der 5. Runde im Wald stehen?")
    compr2 = my_field("2. Hängt die Anzahl der Bäume am Ende der 5. Runde nur von Ihren Entscheidungen ab? ")
    compr3 = models.IntegerField(label="3. Bis zu wie viele Bäume kann jedes Gruppenmitglied in jeder Runde maximal entnehmen?")
    compr4 = my_field("4. Können Sie frei entscheiden, wie viele Bäume Sie in jeder Runde entnehmen wollen (unter der Beschränkung aus der vorherigen Frage)?")
    compr5 = my_field("5. Kann der Wald größer als 100 Bäume werden?")
    num_failed_attempts = models.IntegerField(initial=0)

#FUNCTIONS
# PAGES
class P01Code(Page):
    form_model = "player"
    form_fields = ["code"]

    @staticmethod
    def error_message(player: Player, values):
        if values["code"] != 2206:
            return("Sie haben den falschen Code eingegeben.")


class CS1_Welcome(Page):
    pass
    #form_model = "player"
    #form_fields = ["cubicle"]
    

class StageDivider(Page):
    template_name = "_templates/global/StageDividerPage.html"
    timeout_seconds = 5

    @staticmethod
    def vars_for_template(player: Player):
        return dict(next_stage = 1)


class Gather(WaitPage):
    pass


class P03InstructionsN(Page):
    pass


class CS1_Example(Page):
    @staticmethod
    def js_vars(player: Player):
        return dict(INITIAL_TREES = C.INITIAL_TREES)


class P05ComprehensionCheck(Page):
    form_model = "player"
    form_fields = ["compr1", "compr2", "compr3", "compr4", "compr5"]

    @staticmethod
    def error_message(player: Player, values):
        solutions = dict(compr1 = 1, compr2 = 0, compr3 = 7, compr4 = 1, compr5 = 0)
        names = dict(compr1 = "Frage 1", compr2 = "Frage 2", compr3 = "Frage 3", compr4 = "Frage 4", compr5 = "Frage 5")
        errors = {name: 'Falsch:' for name in solutions if values[name] != solutions[name]}
        if errors:
            player.num_failed_attempts += 1
            error_names = [names[name] for name in errors.keys()]
            return("Bitte korrigieren Sie die Fehler:", error_names)


class P06ComprehensionSuccess(Page):
    form_model = "player"
    form_fields = ["code"]

    @staticmethod
    def error_message(player: Player, values):
        if values["code"] != 2206:
            return("Sie haben den falschen Code eingegeben.")


page_sequence = [
    #P01Code,
    CS1_Welcome,
    StageDivider,
    #Gather, ######## doesn't seem necessary!
    P03InstructionsN,
    CS1_Example,
    P05ComprehensionCheck,
    P06ComprehensionSuccess
]
