from otree.api import *
from CS2_Forest import C as C_FOREST


doc = """
Questionnaire After Experiment
"""


class C(BaseConstants):
    NAME_IN_URL = 'CS5_Quest'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 1
    USE_POINTS = False
    MAX_TREES_TAKE = C_FOREST.MAX_TAKE * C_FOREST.NUM_ROUNDS # maximum trees a player could take over the 5 rounds of the game
    MAX_TREES_GROUP_TAKE = C_FOREST.MAX_TAKE * C_FOREST.NUM_ROUNDS * C_FOREST.PLAYERS_PER_GROUP # maximum trees a group of 3 could take over the 5 rounds of the game
    SHOWUP_FEE = cu(4.00)



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass

# DEFINE FUNCTIONS FOR SCALES
def likert_0_10(label):
    return models.IntegerField(
        choices=[[0, "0"], [1, "1"], [2, "2"], [3, "3"], [4, "4"], [5, "5"], [6, "6"], [7, "7"], [8, "8"], [9, "9"], [10, "10"]],
        label=label,
        widget=widgets.RadioSelectHorizontal
        )

def likert_1_10(label):
    return models.IntegerField(
        choices=[[1, "1"], [2, "2"], [3, "3"], [4, "4"], [5, "5"], [6, "6"], [7, "7"], [8, "8"], [9, "9"], [10, "10"]],
        label=label,
        widget=widgets.RadioSelectHorizontal
        )

def likert_1_7(label):
    return models.IntegerField(label=label,
        choices=[1, 2, 3, 4,
                 5, 6, 7],
                 widget=widgets.RadioSelectHorizontal
    )


'''def behavior_string(part):
    return models.LongStringField(label=f"Was ist Ihrer Meinung nach in Teil {part}, in dem <b>kein</b> Klimaschock eingetreten ist, die optimale Entnahme an Bäumen, die jedem Gruppenmitglied den höchsten Gewinn bringt?")
'''
'''
def yesno(label):
    return models.IntegerField(label=label, choices=[[1, "Ja"], [0, "Nein"],
                                                     # [99, "Weiß nicht/Keine Angabe"]
                                                     ], widget=widgets.RadioSelectHorizontal)'''


class Player(BasePlayer):
    # Behavior during the experiment: Page ExpBeh
    optimumN = models.IntegerField(label="Wie viele Bäume sollte Ihrer Meinung nach in <b>Teil 1</b> jedes Gruppenmitglied jede Runde entnehmen, damit die Gesamtauszahlung der Gruppe am höchsten ist?",
                                  choices=[0,1,2,3,4,5,6,7], widget=widgets.RadioSelectHorizontal)
    optimumA = models.IntegerField(label="Wie viele Bäume sollte Ihrer Meinung nach in <b>Teil 2</b> (wo die Möglichkeit eines Waldbrandes am Ende der 5. Runde bestand) jedes Gruppenmitglied jede Runde entnehmen, damit die Gesamtauszahlung der Gruppe am höchsten ist?",
                                  choices=[0,1,2,3,4,5,6,7], widget=widgets.RadioSelectHorizontal)

    optimumS = models.IntegerField(label="Wie viele Bäume sollte Ihrer Meinung nach in <b>Teil 3</b> (wo ein Waldbrand zu Beginn eingetreten ist) jedes Gruppenmitglied jede Runde entnehmen, damit die Gesamtauszahlung der Gruppe am höchsten ist?",
                                  choices=[0,1,2,3,4,5,6,7], widget=widgets.RadioSelectHorizontal)

    # Optimal strategy & social appropriateness: Page ExpBehSocial
    strategy = models.IntegerField(choices=[[0, "In 0 Runden genau 3 Bäume entnehmen"],
                                            [1, "In 1 Runde genau 3 Bäume entnehmen"],
                                            [2, "In 2 Runden genau 3 Bäume entnehmen"],
                                            [3, "In 3 Runden genau 3 Bäume entnehmen"],
                                            [4, "In 4 Runden genau 3 Bäume entnehmen"],
                                            [5, "In allen 5 Runden genau 3 Bäume entnehmen"]], 
                                            label="Was meinen Sie: Was <b>sollte</b> ein Gruppenmitglied machen?",
                                            widget=widgets.RadioSelect)
    soc_approp_pos = models.IntegerField(choices=[[0, "Sehr sozial unangemessen"],
                                                  [1, "Einigermaßen sozial unangemessen"],
                                                  [2, "Einigermaßen sozial angemessen"],
                                                  [4, "Sehr sozial angemessen"]],
                                         label="Nehmen Sie an, dass ein Gruppenmitglied in einer Runde <b>genau</b> 3 Bäume entnommen hat. Was meinen Sie: Wie würde die Mehrheit dies betrachten?",
                                         widget=widgets.RadioSelect)
    soc_approp_neg = models.IntegerField(choices=[[0, "Sehr sozial unangemessen"],
                                                  [1, "Einigermaßen sozial unangemessen"],
                                                  [2, "Einigermaßen sozial angemessen"],
                                                  [4, "Sehr sozial angemessen"]],
                                         label="Nehmen Sie an, dass ein Gruppenmitglied in einer Runde <b>mehr als</b> 3 Bäume entnommen hat. Was meinen Sie: Wie würde die Mehrheit dies betrachten?",
                                         widget=widgets.RadioSelect)
    slider_guess = models.FloatField(max=100, # label not automatically shown, thus repeated in HTML
        label="Neben Ihnen haben bereits andere Personen an dieser Studie teilgenommen. Wenn man sich alle Entscheidungen dieser Personen anschaut, was glauben Sie: Wie oft wurden genau 3 Bäume entnommen?")
    
    # Environmental Attitude: EAI - SECTION
    eai_1 = likert_1_7(label= "Ich mache sehr gerne Ausfl&uuml;ge in die Natur, zum Beispiel in den Wald oder auf die Felder.")
    eai_2 = likert_1_7(label= "Ich finde es langweilig, Zeit in der Natur zu verbringen. ")
    eai_3 = likert_1_7(label= "Regierungen sollten den Verbrauch von Rohstoffen kontrollieren, damit sie so lange wie möglich halten. ")
    eai_4 = likert_1_7(label= "Ich bin dagegen, dass Regierungen die Verwendung von Rohstoffen kontrollieren und regulieren, um deren Lebensdauer zu verlängern. ")
    eai_5 = likert_1_7(label= "Ich würde gerne einer Umweltschutzgruppe beitreten und aktiv mitarbeiten.")
    eai_6 = likert_1_7(label= "Ich würde mich nicht in einer Umweltschutzgruppe engagieren.")
    eai_7 = likert_1_7(label= "Einer der wichtigsten Gründe, Seen und Flüsse sauber zu halten, besteht darin, den Menschen die Möglichkeit zu geben, Wassersport zu betreiben.")
    eai_8 = likert_1_7(label= "Wir müssen Flüsse und Seen sauber halten, um die Umwelt zu schützen, und nicht um den Menschen die Möglichkeit zu geben, Wassersport zu betreiben.")
    eai_9 = likert_1_7(label= "Die moderne Wissenschaft wird nicht in der Lage sein, unsere Umweltprobleme zu lösen. ")
    eai_10 = likert_1_7(label= "Die moderne Wissenschaft wird unsere Umweltprobleme lösen.")
    eai_11 = likert_1_7(label= "Der Mensch missbraucht die Umwelt massiv. ")
    eai_12 = likert_1_7(label= "Ich glaube nicht, dass die Umwelt durch den Menschen massiv missbraucht wurde. ")
    eai_13 = likert_1_7(label= "Ein wilder und natürlicher Garten ist mir lieber als ein gepflegter und geordneter Garten. ")
    eai_14 = likert_1_7(label= "Ein gepflegter und geordneter Garten ist mir viel lieber als ein wilder und natürlicher Garten. ")
    eai_15 = likert_1_7(label= "Ich gehöre nicht zu den Menschen, die sich bemühen, die natürlichen Ressourcen zu erhalten. ")
    eai_16 = likert_1_7(label= "Wann immer möglich, versuche ich, natürliche Ressourcen zu schonen. ")
    eai_17 = likert_1_7(label= "Der Mensch wurde geschaffen oder hat sich dazu entwickelt, den Rest der Natur zu beherrschen. ")
    eai_18 = likert_1_7(label= "Ich glaube nicht, dass der Mensch geschaffen wurde oder sich dazu entwickelt hat, den Rest der Natur zu beherrschen. ")
    eai_19 = likert_1_7(label= "Der Schutz von Arbeitsplätzen ist wichtiger als der Schutz der Umwelt. ")
    eai_20 = likert_1_7(label= "Der Schutz der Umwelt ist wichtiger als der Schutz von Arbeitsplätzen. ")
    eai_21 = likert_1_7(label= "Es macht mich traurig, zu sehen, wie Wälder für die Landwirtschaft gerodet werden.")
    eai_22 = likert_1_7(label= "Es macht mich nicht traurig zu sehen, wie die natürliche Umwelt zerstört wird. ")
    eai_23 = likert_1_7(label= "Familien sollten ermutigt werden, sich auf zwei Kinder oder weniger zu beschränken. ")
    eai_24 = likert_1_7(label= "Eine Familie sollte so viele Kinder haben, wie sie möchte, solange sie diese angemessen versorgen kann. ")

    # CC - Section 
    q30 = models.IntegerField(label="Wie besorgt sind Sie hinsichtlich Klimaschocks?", 
                              choices=[[1, "Sehr besorgt"], [2, "Etwas besorgt"], [3, "Nicht sehr besorgt"], [4, "Überhaupt nicht besorgt"]], widget=widgets.RadioSelect)
    q32 = models.IntegerField(label="Wie sehr werden Ihrer Meinung nach Klimaschocks den Menschen in Ihrem Wohnort schaden?", 
                              choices=[[1, "Überhaupt nicht"], [2, "Wenig"], [3, "Relativ stark"], [4, "Sehr stark"]], widget=widgets.RadioSelect)
    q33 = models.IntegerField(label="Glauben Sie, dass Klimaschocks hauptsächlich...", 
                              choices=[[1, "auf menschliche Aktivitäten zurückzuführen sind"], [2, "auf natürliche Ursachen zurückzuführen sind"]], widget=widgets.RadioSelect)
    q59 = models.IntegerField(label="Ist Ihrer Meinung nach die in letzter Zeit gestiegene Wahrscheinlichkeit von Klimaschocks vor allem...", 
                              choices=[[1, "eine Folge menschlicher Aktivitäten"], [2, "eine Folge natürlicher Ursachen"]], widget=widgets.RadioSelect)
    
    # GPS questions
    # Page GPS1 - Q71
    gps71 = likert_0_10(label="")

    # Page GPS2 - Q72
    gps72_a = likert_0_10(label="Wie sehr wären Sie bereit auf etwas, das für Sie heute Nutzen bringt, zu verzichten, um dadurch in Zukunft mehr zu profitieren?")
    gps72_b = likert_0_10(label="Wie sehr wären Sie bereit, jemanden zu bestrafen, der <i>Sie</i> unfair behandelt, selbst wenn dies für Sie negative Konsequenzen haben würde?")
    gps72_c = likert_0_10(label="Wie sehr wären Sie bereit, jemanden zu bestrafen, der <i>andere</i> unfair behandelt, selbst wenn dies für Sie Kosten verursachen würde?")
    gps72_d = likert_0_10(label="Wie sehr wären Sie bereit, für einen guten Zweck zu geben, ohne etwas als Gegenleistung zu erwarten.")

    # Page GPS3 - Q73
    gps73_a = likert_0_10(label="Wenn mir jemand einen Gefallen tut, bin ich bereit ihn zu erwidern.")
    gps73_b = likert_0_10(label="Wenn ich sehr ungerecht behandelt werde, räche ich mich bei der ersten Gelegenheit, selbst wenn Kosten entstehen, um das zu tun.")
    gps73_c = likert_0_10(label="Ich vermute, dass Leute nur die besten Absichten haben.")
    #gps73_d = likert_0_10(label="Ich bin gut in Mathematik.")
    #gps73_e = likert_0_10(label="Ich neige dazu, Aufgaben zu verschieben, auch wenn ich weiß, dass es besser wäre sie gleich zu tun.")

    # Page GPS4 - Q105
    posrec1 = models.BooleanField(choices=[[True, "Ja"], [False, "Nein"]], label="")
    posrec1_ifyes = models.IntegerField(
        choices=[[5, "Das Geschenk im Wert von 5 Euro"],
                 [10, "Das Geschenk im Wert von 10 Euro"],
                 [15, "Das Geschenk im Wert von 15 Euro"],
                 [20, "Das Geschenk im Wert von 20 Euro"],
                 [25, "Das Geschenk im Wert von 25 Euro"],
                 [30, "Das Geschenk im Wert von 30 Euro"]],
                 blank=True,
                 label=""
                 )
    # Page GPS5 - Q106
    altruism1 = models.CurrencyField(min=0, max=1000, label="Stellen Sie sich die folgende Situation vor: Heute haben Sie unerwartet 1000 Euro erhalten. Wie viel von dem Geld würden Sie für einen guten Zweck spenden?", blank=True)
    altruism1_noanswer = models.IntegerField(choices=[[99999, "Weiß nicht/Keine Angabe"]], widget=widgets.RadioSelect, label="", blank=True)

    # CS - Section
    q13 = models.IntegerField(label="Im folgenden Abschnitt werden wir Ihnen Fragen zu Ihren persönlichen Erfahrungen mit Klimaschocks stellen. Wenn Sie aus persönlichen Gründen diese Fragen nicht beantworten möchten, können Sie diesen Abschnitt überspringen.", 
                              choices=[[1, "Weiter"], [0, "Überspringen"]], widget=widgets.RadioSelect)
    q14 = models.IntegerField(label="Haben Sie persönlich in der Vergangenheit klimabedingte Schocks oder extreme Wetterereignisse erlebt?", 
                              choices=[[1, "Ja"], [0, "Nein"]], widget=widgets.RadioSelect)
    q15 = models.IntegerField(label="Wie besorgt sind Sie über die möglichen Auswirkungen von Klimaschocks auf Ihren Wohnort?", 
                              choices=[[0, "Überhaupt nicht besorgt"], [1, "Wenig besorgt"],[2, "Ziemlich besorgt"], [3, "Extrem besorgt"]], widget=widgets.RadioSelect)
    q18 = models.FloatField(min=0, max=100, label="Wie hoch schätzen Sie die Wahrscheinlichkeit (in Prozent) ein, dass Ihr Ort einen Klimaschock erfahren wird? ")

    q19 = models.IntegerField(label="Bitte geben Sie an, welche klimabedingten Schocks oder extremen Wetterereignisse Sie erlebt haben.", 
                              choices=[[1, "Weiter"], [2, "Überspringen"]], widget=widgets.RadioSelect)
    q20 = models.IntegerField(label="Haben Sie jemals an einem Ort gelebt, an dem natürliche Ressourcen entnommen werden?", 
                              choices=[[1, "Ja"], [0, "Nein"]], widget=widgets.RadioSelect)
    q21 = models.IntegerField(label="Haben Sie jemals an einem Ort gelebt, an dem natürliche Ressourcen entnommen werden?", 
                              choices=[[1, "Ja"], [0, "Nein"],[3, "Nicht sicher"]], widget=widgets.RadioSelect)
    q23 = models.IntegerField(label="Die Entnahme von Ressourcen hat erhebliche Auswirkungen auf die Umwelt.", 
                              choices=[[0, "Stimme überhaupt nicht zu"], [1, "Stimme nicht zu"],[2, "Neutral"], [3, "Stimme zu"],[4, "Stimme voll und ganz zu"]], widget=widgets.RadioSelect)

    # AB - Section
    q11 = models.IntegerField(label="Ich glaube, dass individuelle Maßnahmen zur Erhaltung der Umwelt wichtig sind.", 
                              choices=[[1, "Weiter"], [0, "Überspringen"]], widget=widgets.RadioSelect)
    q12 = models.IntegerField(label="Ich glaube, dass nur von Gruppen durchgeführte Aktionen wie NGOs oder kommunale Initiativen echte Auswirkungen auf die Umwelt haben.", 
                              choices=[[1, "Weiter"], [0, "Überspringen"]], widget=widgets.RadioSelect)
    
    # Demographic questions: Page Demographics
    age = models.IntegerField(min=18, max=99, label="Wie alt sind Sie?")
    gender = models.IntegerField(choices=[[0, 'Männlich'], [1, 'Weiblich'], [2, 'Divers']], label='Was ist Ihr Geschlecht?', widget=widgets.RadioSelectHorizontal)
    highest_ed = models.StringField(label="Was ist Ihr höchster Bildungsabschluss?",choices=['Ohne Schulabschluss', 
                                             'Schulabschluss', 
                                             'Ausbildung',
                                             'Bachelor-Abschluss',
                                             'Master-Abschluss',
                                             'Promotion (PhD.)',
                                             'Sonstige'])
    study_field = models.StringField(label="Spezifizieren Sie Ihr Studienfach:",choices=[[1, "Hat einen Bezug zu natürlichen Ressourcen"], [2, "Hat keinen Bezug zu natürlichen Ressourcen"], [3, "Unsicher, ob ein Zusammenhang besteht"], [4, "Ich studiere nicht/habe nicht studiert"]])
    subject_of_studies = models.StringField( ############# necessary question?
        choices=['Kein Studium',
                 'Geisteswissenschaften',
                 'Sozialwissenschaften',
                 'Psychologie',
                 'Wirtschaftswissenschaften',
                 'Rechtswissenschaften',
                 'Biologie',
                 'Medizin',
                 'Agrar- oder Ernährungswissenschaften',
                 'Naturwissenschaften',
                 'Ingenieurswissenschaften',
                 #'Mathematik, Informatik, Naturwissenschaften oder Ingenieurswissenschaften',
                 #'Sozial- oder Geisteswissenschaften',
                 #'Rechts- oder Wirtschaftswissenschaften',
                 #'Agrar- oder Ernährungswissenschaften',
                 'Andere'
                 ],
        label='Falls Sie studieren/studiert haben, in welcher Fachrichtung?')
    social_position = likert_1_10 (label= "Wählen Sie die Zahl, deren Position am ehesten Ihre Position auf dieser Leiter widerspiegelt.")


    # Page Lab
    lab_xp = models.StringField(label="Wie oft haben Sie bereits im BonnEconLab an Studien teilgenommen?",
                                 choices = [[0, "noch nie"], [1, "einmal"], [2, "zwei- bis fünfmal"], [6, "sechsmal oder öfter"], [99, "Weiß nicht/Keine Angabe"]])
    ############# lab_xp sinnvolle Intervalle???
    why_exp = models.LongStringField(label="Was, denken Sie, möchten wir mit dieser Studie erforschen?", blank=True)

    app_to_pay = models.StringField()
    paid_stage = models.IntegerField()
    stage_points = models.FloatField()


# PAGES
class CS5Intro(Page):
    pass

class ExpBehOptimumNAS(Page): # behavior during the experiment; ask this first so they remember?
    form_model = "player"
    form_fields = ["optimumN","optimumA", "optimumS"] ##### add social appropriateness here?


class ExpBehSocial(Page):
    form_model = "player"
    form_fields = ["strategy", "soc_approp_pos", "soc_approp_neg", "slider_guess"]

class GPS1(Page):
    form_model = "player"
    form_fields = ["gps71"]


class GPS2(Page):
    form_model = "player"
    form_fields = ["gps72_a", "gps72_b", "gps72_c", "gps72_d"]


class GPS3(Page):
    form_model = "player"
    form_fields = ["gps73_a", "gps73_b","gps73_c"] 


class GPS4(Page):
    form_model = "player"
    form_fields = ["posrec1", "posrec1_ifyes"]
        
class GPS5(Page):
    form_model = "player"
    form_fields = ["altruism1"]

class EnvAtt(Page):
    form_model = "player"
    form_fields = ["eai_1",
                   "eai_24",
                   "eai_19",
                   "eai_13",
                   "eai_14",
                   "eai_5",
                   "eai_23",
                   "eai_16",
                   "eai_7",
                   "eai_18",
                   "eai_9",
                   "eai_10",
                   "eai_4",
                   "eai_12",
                   "eai_3",
                   "eai_15",
                   "eai_2",
                   "eai_18",
                   "eai_20",
                   "eai_6",
                   "eai_21",
                   "eai_11",
                   "eai_22",
                   "eai_17",
                   "eai_8",
                   ]

class CC(Page):
    form_model = "player"
    form_fields = ["q30", "q32", "q33", "q59"]

class CS(Page):
    form_model = "player"
    form_fields = ["strategy","q13", "q14", "q15", "q18","q19","q20","q21", "q23"]

class AB(Page):
    form_model = "player"
    form_fields = ["q11", "q12"]

class Demographics(Page):
    form_model = "player"
    form_fields = ["age", #"age_noanswer",
                   "gender",
                   'highest_ed',
                   #"subject_of_studies",
                   "study_field",
                   "social_position"
                   ]

class Lab(Page):
    form_model = "player"
    form_fields = ["lab_xp", "why_exp"]


class ResultsWaitPage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        import random
        apps = ["CS2_Forest", "CS3_Anti1", "CS4_Shock"] #or CS3_Anti2
        print(apps)
        app_to_pay = random.choice(apps)
        print("APP TO PAY:", app_to_pay)
        players = group.get_players()
        for p in players:
            participant = p.participant
            participant.game_payoff = participant.app_payoffs[app_to_pay]
            p.app_to_pay = app_to_pay
            p.paid_stage = round(apps.index(app_to_pay) + 1)
            p.stage_points = round(p.participant.points_in_stage[app_to_pay],2)
            participant.payoff = participant.game_payoff + C.SHOWUP_FEE

class ThankYou(Page):
    pass


class Results(Page):
    pass


page_sequence = [
                CS5Intro,
                ResultsWaitPage, 
                ExpBehOptimumNAS, # KEEP
                ExpBehSocial,   # Keep
                GPS1,
                GPS2,
                GPS3,
                #GPS4,
                #GPS5,
                EnvAtt,         # KEEP
                CC,
                #CS,            # DROP
                Demographics,   # Keep add ladder , REMOVE AVERAGE INCOME
                Lab,
                ThankYou,
                Results]