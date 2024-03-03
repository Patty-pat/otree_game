from otree.api import *
import math 


doc = """
Treatment Section
"""


class C(BaseConstants):
    NAME_IN_URL = 'AnticipationRandom'
    PLAYERS_PER_GROUP = 3
    STAGE = 2
    NUM_ROUNDS= 5
    NUMBER_OF_ROUNDS = NUM_ROUNDS
    MIN_TAKE = 0 
    MAX_TAKE = 7
    MULTIPLIER_TAKE = 2
    MULTIPLIER_GROUP = 4
    MULTIPLIER_SHOCK = 0.5
    MIN_SHOCK_PROB = 0.20               #redundant
    MAX_SHOCK_PROB = 0.80
    INITIAL_TREES = 100
    INCOME = 0 
    LIFE_COSTS = 0 
    ENDOWMENT = 50
    SHOWUP_FEE = cu(4.00)
    CENTS = 0.09


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    current_trees_after_take = models.FloatField(min=0, max=C.INITIAL_TREES)
    current_trees = models.FloatField(min=0, max=C.INITIAL_TREES)
    regrowth = models.FloatField()
    total_group_take = models.IntegerField()
    high_probability = models.BooleanField() #initial=False
    is_shock_group = models.BooleanField(choices=[True, False]) #initial=False, 
    shock_probability_high = models.FloatField(min=0, max=1)
    shock_probability_low = models.FloatField(min=0, max=1)

    @staticmethod
    def tree_count_take(group):
        players = group.get_players()
        group_take = [p.participant.take for p in players]
        total_group_take = sum(group_take)
        p1 = group.get_player_by_id(1)
        group.current_trees = round(p1.participant.current_trees,2)
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
    
def round_which(label):
    return models.IntegerField(choices=[[0, "Runde 1"], [1, "Runde 5"], [2, "Kann man pauschal nicht sagen."]], widget=widgets.RadioSelectHorizontal, label=label)

def my_field(label):
    return models.IntegerField(choices=[[1, "Ja"], [0, "Nein"], [2, "Kann man pauschal nicht sagen."]], 
                               widget=widgets.RadioSelectHorizontal, label=label)
def percent(label):
    return models.IntegerField(choices= [[0, "20%"], [1, "50%"], [3, "80%"]], widget=widgets.RadioSelectHorizontal, label = label)

class Player(BasePlayer):
    take = models.IntegerField(min=C.MIN_TAKE, max=C.MAX_TAKE, label="Wie viele Bäume möchten Sie entnehmen?")
    balance = models.IntegerField(label="Ihr Kontostand: ")
    points = models.IntegerField()
    stage_points = models.FloatField()
    player_history_take = models.IntegerField()
    potential_payoff = models.CurrencyField()
    compr1 = round_which(label="1. Falls ein Waldbrand eintritt, in welcher Runde tritt er ein?")
    compr2 = my_field("2. Falls ein Waldbrand eintritt, wird der Schock zu Beginn der Runde eintreten bevor der Wald nachwachsen konnte? ")
    compr3 = percent(label= "3. Falls ein Waldbrand eintritt, um wie viel Prozent wird die Anzahl der verbliebenen Bäume reduziert?")
    compr4 = my_field("4. Wirkt sich der Waldbrand auf die Anzahl Ihrer Punkte aus, die Sie am Ende erhalten?")
    num_failed_attempts = models.IntegerField(initial=0)


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

def creating_session(subsession):
    for p in subsession.get_players():
        p.participant.app_payoffs = {}
        p.participant.points_in_stage = {}
        p.participant.take_history = []
        p.participant.high_probability = ()
        p.participant.is_shock_group = ()
    # high/low probability groups equal split
    if subsession.round_number==1:
        import itertools
        high_probability = itertools.cycle([True, False]) 
        for g in subsession.get_groups():
            g.high_probability = next(high_probability)
            p1 = g.get_player_by_id(1)
            p1.participant.high_probability = g.high_probability
            players = g.get_players()
            for p in players:
                p.participant.high_probability = g.high_probability
                print("Group " + str(g.id_in_subsession) + ", Player " + str(p.id_in_group) + ": " + str(p.participant.high_probability))
    else:
        for g in subsession.get_groups():
            g.high_probability = g.in_round(g.round_number - 1).high_probability
            p1 = g.get_player_by_id(1)
            p1.participant.high_probability = g.high_probability
            for p in g.get_players():
                p.participant.high_probability = g.high_probability
                
    if subsession.round_number==5:
        import random
        for g in subsession.get_groups():
            if g.high_probability ==True:
                shock_probability_high = round(random.uniform(0, 1),2)
                g.shock_probability_high = shock_probability_high
                p1 = g.get_player_by_id(1)
                p1.participant.shock_probability_high = g.shock_probability_high
                if g.shock_probability_high <= C.MAX_SHOCK_PROB:
                    g.is_shock_group = True
                else:
                    g.is_shock_group = False
            else:
                shock_probability_low = round(random.uniform(0, 1),2)
                g.shock_probability_low = shock_probability_low
                p1 = g.get_player_by_id(1)
                p1.participant.shock_probability_low = g.shock_probability_low
                players = g.get_players()
                if g.shock_probability_low <= C.MAX_SHOCK_PROB:
                    g.is_shock_group = False
                else:
                    g.is_shock_group = True

            for p in g.get_players():
                p.participant.is_shock_group = g.is_shock_group
                print("Group " + str(g.id_in_subsession) + ", Player " + str(p.id_in_group) + ": " + str(p.participant.is_shock_group))

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

class Instructions(Page):
    template_name = "CS3_Anti1/CS3_IntroductionRandom.html"

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number==1

class P03InstructionsA(Page):
    template_name = "CS3_Anti1/P03InstructionsA.html"

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number==1

class CS3Example(Page):
    template_name = "CS3_Anti1/CS3_Example.html"

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number==1
    
    @staticmethod
    def js_vars(player: Player):
        return dict(INITIAL_TREES = C.INITIAL_TREES)


class P05ComprehensionCheckA(Page):
    template_name = "CS3_Anti1/P05ComprehensionCheckA.html"
    
    form_model = "player"
    form_fields = ["compr1", "compr2", "compr3", "compr4"]

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number==1

    @staticmethod
    def error_message(player: Player, values):
        solutions = dict(compr1 = 1, compr2 = 0, compr3 = 1, compr4 = 1)
        names = dict(compr1 = "Frage 1", compr2 = "Frage 2", compr3 = "Frage 3", compr4 = "Frage 4")
        errors = {name: 'Falsch:' for name in solutions if values[name] != solutions[name]}
        if errors:
            player.num_failed_attempts += 1
            error_names = [names[name] for name in errors.keys()]
            return("Bitte korrigieren Sie die Fehler:", error_names)
    

class Forest1ShockRund5(Page):
    template_name = "CS3_Anti1/CS3_Forest1_ShockRund5.html"

    form_model = "player"
    form_fields = ["take"]
    
    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        p1 = group.get_player_by_id(1)
        group.current_trees = round(p1.participant.current_trees,2)
        if player.round_number == 1:
            player.balance = C.ENDOWMENT
        else:
            player.balance = player.in_round(player.round_number-1).balance

    @staticmethod
    def js_vars(player):
        group = player.group
        p1 = group.get_player_by_id(1)
        return dict(
            current_trees = math.floor(p1.participant.current_trees),
            INITIAL_TREES = C.INITIAL_TREES
        )
        
    @staticmethod
    def before_next_page(player: Player, timeout_happened = False):
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
    template_name = "CS3_Anti1/CS3_Forest2_regrowth.html"

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        p1 = group.get_player_by_id(1)
        group.current_trees_after_take = round(p1.participant.current_trees_after_take,2)
        group.current_trees = round(p1.participant.current_trees,2)
        #trees_depicted = floor(p1.participant.current_trees)
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
            INITIAL_TREES = C.INITIAL_TREES,
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
            p.stage_points = round(p.balance +  p1.participant.current_trees * C.MULTIPLIER_GROUP/C.PLAYERS_PER_GROUP, 2)
            p.potential_payoff = cu(C.CENTS * p.stage_points)
            print(p.potential_payoff)
            p.participant.app_payoffs[__name__] = p.potential_payoff
            p.participant.points_in_stage[__name__] = p.stage_points
            p.participant.take_history.append(p.player_history_take) ##### I removed an if statement - it's obsolete because I'm referring to the apps by name in the end
            print("HISTORY:", p.participant.take_history)

    
class Results(Page):
    template_name = "CS3_Anti1/CS3_Results_ShockRund5.html"

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
        if group.is_shock_group == True:
            player.stage_points = round(player.balance +  p1.participant.current_trees * C.MULTIPLIER_SHOCK * C.MULTIPLIER_GROUP/C.PLAYERS_PER_GROUP, 2)
            return dict(
                total_player_take = player.player_history_take,
                total_group_history_take = sum(group_history_take),
                current_stage = C.STAGE,                
                trees_after_shock = round(group.current_trees * C.MULTIPLIER_SHOCK, 2),
                stage_value = round(group.current_trees * C.MULTIPLIER_GROUP,2),
                stage_value_aftershock = round(group.current_trees * C.MULTIPLIER_SHOCK * C.MULTIPLIER_GROUP,2),
                trees_stage_value = round((group.current_trees * C.MULTIPLIER_GROUP)/2, 2),
                trees_stage_value_aftershock = round((group.current_trees * C.MULTIPLIER_SHOCK * C.MULTIPLIER_GROUP)/2, 2),
                stage_share = round(group.current_trees * C.MULTIPLIER_GROUP / C.PLAYERS_PER_GROUP, 2),
                stage_share_aftershock = round(group.current_trees * C.MULTIPLIER_SHOCK * C.MULTIPLIER_GROUP / C.PLAYERS_PER_GROUP, 2)
            )
        else:
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
        return dict(next_stage = C.STAGE + 1)

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS
    
        
page_sequence = [
    Gather, 
    #Instructions,
    P03InstructionsA,
    #CS3Example,
    P05ComprehensionCheckA,
    Forest1ShockRund5, 
    ForestWaitPage, 
    Forest2_regrowth, 
    ResultsWaitPage, 
    Results,
    RoundWaitPage,
    StageDividerNext
]

