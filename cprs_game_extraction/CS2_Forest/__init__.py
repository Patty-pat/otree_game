from otree.api import *
import math

doc = """
Baseline Game
"""


class C(BaseConstants):
    NAME_IN_URL = 'CS2_Forest'
    PLAYERS_PER_GROUP = 3
    STAGE = 1                           # FIRST APP IN OUR CLIMATE SHOCK GAME
    NUM_ROUNDS = 5
    NUMBER_OF_ROUNDS = NUM_ROUNDS       # THIS IS ONLY FOR THE INSTRUCTION PAGE
    MIN_TAKE = 0                        # MIN MAX OF TREES ALLOWED TO BE CUT IN EACH ROUND
    MAX_TAKE = 7
    MULTIPLIER_TAKE = 2
    MULTIPLIER_GROUP = 4
    INITIAL_TREES = 100
    INCOME = 0 
    LIFE_COSTS = 0 
    ENDOWMENT = 50
    SHOWUP_FEE = cu(4.00)
    CENTS = 0.09                        # FACTOR OF PAYOFF IN CURRENCY


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    current_trees_after_take = models.FloatField(min=0, max=C.INITIAL_TREES)
    current_trees = models.FloatField(min=0, max=C.INITIAL_TREES)
    regrowth = models.FloatField()
    total_group_take = models.IntegerField()

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
        else:
            p1.participant.current_trees = C.INITIAL_TREES
        group.current_trees = round(p1.participant.current_trees,2)
        return(group.current_trees)
    

class Player(BasePlayer):
    take = models.IntegerField(min=C.MIN_TAKE, max=C.MAX_TAKE, label="Wie viele Bäume möchten Sie entnehmen?")
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

class Forest1(Page):
    template_name = "CS2_Forest/CS2_Forest1.html"

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
            player.balance = player.in_round(player.round_number - 1).balance
    
    @staticmethod
    def js_vars(player):        #This allows passing data from Python to JavaScript
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


class Forest2_regrowth(Page):
    template_name = "CS2_Forest/CS2_Forest2_regrowth.html"

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
            previous_group = group.in_round(group.round_number -1)
            current_trees_before = previous_group.current_trees
        group.regrowth = round(group.current_trees - group.current_trees_after_take, 2)
        group.total_group_take = sum([p.participant.take for p in group.get_players()])
        player.balance = player.set_balance(player)
        player.points = C.MULTIPLIER_TAKE*player.take
        return dict(current_trees_before = current_trees_before, change = player.points + C.INCOME - C.LIFE_COSTS)
    
    @staticmethod
    def js_vars(player):
        group = player.group
        p1 = group.get_player_by_id(1)
        if group.round_number==1:
            previous_group = group
            ctb = C.INITIAL_TREES       # ctb: current trees before
        else:
            previous_group = group.in_round(group.round_number -1)
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
            p.stage_points = round(p.balance +  p1.participant.current_trees * C.MULTIPLIER_GROUP/C.PLAYERS_PER_GROUP,2)
            p.potential_payoff = cu(C.CENTS * p.stage_points)
            print(p.potential_payoff)
            p.participant.app_payoffs[__name__] = p.potential_payoff
            p.participant.points_in_stage[__name__] = p.stage_points
            p.participant.take_history.append(p.player_history_take) ##### I removed an if statement - it's obsolete because I'm referring to the apps by name in the end
            print("HISTORY:", p.participant.take_history)


class Results(Page):
    template_name = "CS2_Forest/CS2_Results.html"

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
    Forest1, 
    ForestWaitPage, 
    Forest2_regrowth, 
    ResultsWaitPage, 
    Results, 
    RoundWaitPage, 
    StageDividerNext
]