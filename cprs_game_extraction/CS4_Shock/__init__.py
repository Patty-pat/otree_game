from otree.api import *
import math 

doc = """
Forest Game Start With shock - multiple take field version 2
"""


class C(BaseConstants):
    NAME_IN_URL = 'Shooketh2'
    PLAYERS_PER_GROUP = 3
    CENTS = 0.09                        # Factor for payoffs
    STAGE =3
    NUM_ROUNDS = 5
    NUMBER_OF_ROUNDS = NUM_ROUNDS       # rounds in the game, for the instructions
    MIN_TAKE = 0                        # minimum and maximum number of trees allowed to take each round
    MAX_TAKE7 = 7
    MAX_TAKE6 = 6
    MAX_TAKE5 = 5
    MAX_TAKE4 = 4
    MAX_TAKE3 = 3
    MAX_TAKE2 = 2
    MAX_TAKE1 = 1
    MAX_TAKE0 = 0
    MULTIPLIER_TAKE = 2                 # multiplier for trees taken out
    MULTIPLIER_GROUP = 4                # multiplier for trees left in the forest
    MULTIPLIER_SHOCK = 0.5
    INITIAL_TREES = 50
    INITIAL_TREES_OLD = 100
    INCOME = 0
    LIFE_COSTS = 0
    ENDOWMENT = 50
    SHOWUP_FEE = cu(4.00)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    current_trees_after_take = models.FloatField(min=0, max=C.INITIAL_TREES_OLD)
    current_trees = models.FloatField(min=0, max=C.INITIAL_TREES_OLD)
    regrowth = models.FloatField()
    total_group_take = models.IntegerField()
    #stage = models.IntegerField()
    ceiling_group_take = models.IntegerField(min=C.MIN_TAKE, initial=None)


    @staticmethod
    def tree_count_take(group):
        players = group.get_players()
        group_take = [p.participant.take for p in players]
        total_group_take = sum(group_take)
        p1 = group.get_player_by_id(1)
        group.current_trees = p1.participant.current_trees
        p1.participant.current_trees_after_take = group.current_trees - total_group_take
        group.current_trees_after_take = p1.participant.current_trees_after_take
        return(group.current_trees_after_take)
    
    @staticmethod
    def tree_count_regrow(group):
        p1 = group.get_player_by_id(1)
        if p1.participant.current_trees_after_take < 91:
            p1.participant.current_trees = p1.participant.current_trees_after_take + p1.participant.current_trees_after_take/10
        elif p1.participant.current_trees_after_take <= 0:
            p1.participant.current_trees = 0
        else:
            p1.participant.current_trees = C.INITIAL_TREES
        group.current_trees = round(p1.participant.current_trees,2)
        return(group.current_trees)
    
    def update_take_ceiling(group):
        p1= group.get_player_by_id(1)
        if p1.participant.current_trees == C.INITIAL_TREES:
            p1.participant.ceiling_group_take = C.MAX_TAKE7
        elif p1.participant.current_trees >= 21:
            p1.participant.ceiling_group_take = C.MAX_TAKE7
        elif p1.participant.current_trees >= 18:
            p1.participant.ceiling_group_take = C.MAX_TAKE6
        elif p1.participant.current_trees >= 15:
            p1.participant.ceiling_group_take = C.MAX_TAKE5
        elif p1.participant.current_trees >= 12:
            p1.participant.ceiling_group_take = C.MAX_TAKE4
        elif p1.participant.current_trees >=9 :
            p1.participant.ceiling_group_take = C.MAX_TAKE3
        elif p1.participant.current_trees >=6 :
            p1.participant.ceiling_group_take = C.MAX_TAKE2
        elif p1.participant.current_trees >= 3:
            p1.participant.ceiling_group_take = C.MAX_TAKE1
        elif p1.participant.current_trees < 3:
            p1.participant.ceiling_group_take = C.MAX_TAKE0
        elif p1.participant.current_trees == 0:
            p1.participant.ceiling_group_take = C.MIN_TAKE
        group.ceiling_group_take = p1.participant.ceiling_group_take
        return(group.ceiling_group_take)

def shock_occ(label):
    return models.IntegerField(choices=[[0, "Vor der ersten Runde"], [1, "Nach der ersten Runde"], [3, "Kann man pauschal nicht sagen."]], widget=widgets.RadioSelectHorizontal, label=label)

def trees_start(label):
    return models.IntegerField(choices=[[0, "100 Bäumen"], [1, "50 Bäumen"], [3, "30 Bäumen"]], widget=widgets.RadioSelectHorizontal, label=label)

def yes_no(label):
    return models.IntegerField(choices=[[1, "Ja"], [0, "Nein"], [2, "Kann man pauschal nicht sagen."]], widget=widgets.RadioSelectHorizontal, label=label)

def max_take(label):
    return models.IntegerField(choices=[[0, "0 Bäume"],[1, "Von 0 bis 1 Baum"], [2, "Von 0 bis 2 Bäume"], [3, "Von 0 bis 3 Bäume"], [4, "Von 0 bis 4 Bäume"],[5, "Von 0 bis 5 Bäume"], [6, "Von 0 bis 6 Bäume"], [7, "Von 0 bis 7 Bäume"]], widget=widgets.RadioSelect, label=label)

class Player(BasePlayer):
    compr1 = shock_occ(label="1. Wann tritt der Waldbrand ein?")
    compr2 = trees_start(label="2. Mit vielen Bäumen im Wald startet die erste Runde?")
    compr3 = yes_no(label="3. Kann der Wald größer als 50 Bäume werden?")
    compr4 = max_take(label="4. Wenn nur 3 Bäume im Wald vorhanden sind, wie viele Bäume darf jedes Gruppenmitglied entnehmen?")
    num_failed_attempts = models.IntegerField(initial=0)
    take_max7 = models.IntegerField(min=C.MIN_TAKE, max=C.MAX_TAKE7, label="Wie viele Bäume möchten Sie entnehmen?")
    take_max6 = models.IntegerField(min=C.MIN_TAKE, max=C.MAX_TAKE6, label="Wie viele Bäume möchten Sie entnehmen?")
    take_max5 = models.IntegerField(min=C.MIN_TAKE, max=C.MAX_TAKE5, label="Wie viele Bäume möchten Sie entnehmen?")
    take_max4 = models.IntegerField(min=C.MIN_TAKE, max=C.MAX_TAKE4, label="Wie viele Bäume möchten Sie entnehmen?")
    take_max3 = models.IntegerField(min=C.MIN_TAKE, max=C.MAX_TAKE3, label="Wie viele Bäume möchten Sie entnehmen?")
    take_max2 = models.IntegerField(min=C.MIN_TAKE, max=C.MAX_TAKE2, label="Wie viele Bäume möchten Sie entnehmen?")
    take_max1 = models.IntegerField(min=C.MIN_TAKE, max=C.MAX_TAKE1, label="Wie viele Bäume möchten Sie entnehmen?")
    take_max0 = models.IntegerField(min=C.MIN_TAKE, max=C.MAX_TAKE0, label="Wie viele Bäume möchten Sie entnehmen?")
    take = models.IntegerField(min=C.MIN_TAKE, max=C.MAX_TAKE7, initial=None)
    balance = models.IntegerField(label="Ihr Kontostand: ")
    points = models.IntegerField()
    stage_points = models.FloatField()
    player_history_take = models.IntegerField()
    potential_payoff = models.CurrencyField()

    @staticmethod
    def set_balance(player):
        player_history = player.in_all_rounds()
        player_history_take = [p.take for p in player_history]
        total_player_take = sum(player_history_take)
        player.player_history_take = total_player_take
        total_player_income = C.INCOME*player.round_number
        total_player_costs = C.LIFE_COSTS*player.round_number
        player.balance = C.ENDOWMENT + total_player_income - total_player_costs + C.MULTIPLIER_TAKE*total_player_take
        return player.balance

    @staticmethod
    def update_takes(player):
        group = player.group
        p1 = group.get_player_by_id(1)
        group.current_trees = p1.participant.current_trees
        round_number = player.round_number
        if round_number == 1:
            player.take = player.take_max7
        elif round_number >1:
            if group.current_trees >=21:
                player.take = player.take_max7
            elif group.current_trees >=18:
                player.take = player.take_max6
            elif group.current_trees >=15:
                player.take = player.take_max5
            elif group.current_trees >=12:
                player.take = player.take_max4
            elif group.current_trees >=9:
                player.take = player.take_max3
            elif group.current_trees >=6:
                player.take = player.take_max2
            elif group.current_trees >=3:
                player.take = player.take_max1
            elif group.current_trees < 3:
                player.take = player.take_max0
        return(player.take)

# FUNCTIONS
def creating_session(subsession):
    for p in subsession.get_players():
        p.participant.app_payoffs = {}
        p.participant.points_in_stage = {}
        p.participant.take_history = []


# PAGES

class Gather(WaitPage):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1
    
    @staticmethod
    def after_all_players_arrive(group: Group):
        p1 = group.get_player_by_id(1) 
        p1.participant.current_trees = C.INITIAL_TREES 
        group.current_trees = round(p1.participant.current_trees,2)
        for p in group.get_players():
            p.participant.balance = C.ENDOWMENT
            p.balance = p.participant.balance

class P03InstructionsSFin(Page):
    template_name = "CS4_Shock/P03InstructionsSFin.html"

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number==1


class P05ComprehensionCheckS(Page):
    template_name = "CS4_Shock/P05ComprehensionCheckS.html"

    form_model = "player"
    form_fields = ["compr1", "compr2", "compr3", "compr4"]

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number==1

    @staticmethod
    def error_message(player: Player, values):
        solutions = dict(compr1 = 0, compr2 = 1, compr3 = 1, compr4 = 1)
        names = dict(compr1 = "Frage 1", compr2 = "Frage 2", compr3 = "Frage 3", compr4 = "Frage 4")
        errors = {name: 'Falsch:' for name in solutions if values[name] != solutions[name]}
        if errors:
            player.num_failed_attempts += 1
            error_names = [names[name] for name in errors.keys()]
            return("Bitte korrigieren Sie die Fehler:", error_names)


class InstructionsShock(Page):                      # replaced by InstructionsFin before comprehension                    
    template_name = "CS4_Shock/CS4InstructionsSFin.html"

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number==1

class Forest1(Page):
    template_name = "CS4_Shock/CS4Forest1.html"     #need to translate one sentence

    form_model = "player"
    form_fields = []
    
    @staticmethod
    def get_form_fields(player):
        group = player.group
        p1 = group.get_player_by_id(1)
        group.current_trees = round(p1.participant.current_trees,2)

        if player.round_number == 1:
            #player.take = player.take_max7
            return ["take_max7"]
        elif player.round_number >1:
            if group.current_trees >=21:
                return ["take_max7"]
            elif group.current_trees >=18:
                return ["take_max6"]
            elif group.current_trees >=15:
                return ["take_max5"]
            elif group.current_trees >=12:
                return ["take_max4"]
            elif group.current_trees >=9:
                return ["take_max3"]
            elif group.current_trees >=6:
                return ["take_max2"]
            elif group.current_trees >=3:
                return ["take_max1"]
            elif group.current_trees <3:
                return ["take_max0"]
            else:
                return ["take_max7"]

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        p1 = group.get_player_by_id(1)
        group.current_trees = round(p1.participant.current_trees,2)
        #group.ceiling_group_take = p1.group.ceiling_group_take
        if player.round_number == 1:
            player.balance = C.ENDOWMENT
        else:
            player.balance = player.in_round(player.round_number-1).balance
        if player.round_number == 1:
            group.ceiling_group_take = C.MAX_TAKE7
        elif player.round_number >1:
            if group.current_trees >=21:
                group.ceiling_group_take = C.MAX_TAKE7
            elif group.current_trees >=18:
                group.ceiling_group_take = C.MAX_TAKE6
            elif group.current_trees >=15:
                group.ceiling_group_take = C.MAX_TAKE5
            elif group.current_trees >=12:
                group.ceiling_group_take = C.MAX_TAKE4
            elif group.current_trees >=9:
                group.ceiling_group_take = C.MAX_TAKE3
            elif group.current_trees >=6:
                group.ceiling_group_take = C.MAX_TAKE2
            elif group.current_trees >=3:
                group.ceiling_group_take = C.MAX_TAKE1
            elif group.current_trees <3:
                group.ceiling_group_take = C.MAX_TAKE0
        return dict ( ceiling_group_take = group.ceiling_group_take,)
                         

    @staticmethod
    def js_vars(player):
        group = player.group
        p1 = group.get_player_by_id(1)
        return dict(
            current_trees = math.floor(p1.participant.current_trees),
            INITIAL_TREES = C.INITIAL_TREES_OLD
        )
                
    @staticmethod
    def before_next_page(player: Player, timeout_happened = False):
        player.update_takes(player)
        participant = player.participant
        participant.take = player.take

class ForestWaitPage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group): 
        p1 = group.get_player_by_id(1) 
        p1.participant.current_trees_after_take = group.tree_count_take(group)
        p1.participant.current_trees = group.tree_count_regrow(group)
        print(p1.participant.current_trees_after_take, p1.participant.current_trees)

class Forest2_regrowth(Page):
    template_name = "CS4_Shock/CS4Forest2_regrowth.html"

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        p1 = group.get_player_by_id(1)
        group.current_trees_after_take = round(p1.participant.current_trees_after_take,2)
        group.current_trees = round(p1.participant.current_trees,2)
        if group.round_number==1:
            previous_group = group
            current_trees_before = C.INITIAL_TREES
        else:
            previous_group = group.in_round(group.round_number - 1)
            current_trees_before = previous_group.current_trees
        group.regrowth = round(group.current_trees - group.current_trees_after_take,2)
        group.total_group_take = sum([p.participant.take for p in group.get_players()])
        player.balance = player.set_balance(player)
        player.points = C.MULTIPLIER_TAKE*player.take
        return dict(current_trees_before = current_trees_before,
                    change = player.points + C.INCOME - C.LIFE_COSTS)

    @staticmethod
    def js_vars(player):
        group = player.group
        p1 = group.get_player_by_id(1)
        if group.round_number==1:
            previous_group = group
            ctb = C.INITIAL_TREES
        else:
            previous_group = group.in_round(group.round_number - 1)
            ctb = previous_group.current_trees
        return dict(
            INITIAL_TREES = C.INITIAL_TREES_OLD,
            current_trees_before = math.floor(ctb),
            current_trees_after_take = math.floor(p1.participant.current_trees_after_take),
            current_trees = math.floor(p1.participant.current_trees),
            player_take = player.take,
            round_number = player.round_number
        )
    

class ResultsWaitPage(WaitPage):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number==C.NUM_ROUNDS
    
    @staticmethod
    def after_all_players_arrive(group: Group):
        for p in group.get_players():
            p1 = group.get_player_by_id(1)
            p.stage_points = round(p.balance +  p1.participant.current_trees * C.MULTIPLIER_GROUP/C.PLAYERS_PER_GROUP,2)
            p.potential_payoff = cu(C.CENTS * p.stage_points)
            print(p.potential_payoff)
            p.participant.app_payoffs[__name__] = p.potential_payoff
            p.participant.points_in_stage[__name__] = p.stage_points
            p.participant.take_history.append(p.player_history_take)
            print("HISTORY:", p.participant.take_history)


class Results(Page):
    template_name = "CS4_Shock/CS4Results.html"

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        group_history_take = []
        for q in group.get_players():
            player_history = q.in_all_rounds()
            q.player_history_take = sum([p.take for p in player_history])
            group_history_take.append(q.player_history_take)
            print(q.player_history_take, group_history_take)
        p1 = group.get_player_by_id(1)
        player.stage_points = round(player.balance +  p1.participant.current_trees * C.MULTIPLIER_GROUP/C.PLAYERS_PER_GROUP, 2)
        return dict(
            total_player_take = player.player_history_take,
            total_group_history_take = sum(group_history_take),
            current_stage = C.STAGE,
            stage_value = round(group.current_trees * C.MULTIPLIER_GROUP,2),
            trees_stage_value = round((group.current_trees * C.MULTIPLIER_GROUP)/2, 2),
            stage_share = round(group.current_trees * C.MULTIPLIER_GROUP / C.PLAYERS_PER_GROUP, 2)
        )

class RoundWaitPage(WaitPage):
    pass
    

class StageDividerNext(Page):
    template_name = "_templates/global/StageDividerPage.html"
    timeout_seconds = 5

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        return dict(next_stage = C.STAGE + 1)

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS
    

page_sequence = [
    Gather, 
    P03InstructionsSFin,
    P05ComprehensionCheckS,
    Forest1, 
    ForestWaitPage, 
    Forest2_regrowth, 
    ResultsWaitPage, 
    Results, 
    RoundWaitPage, 
    StageDividerNext]