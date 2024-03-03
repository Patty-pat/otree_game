from os import environ

SESSION_CONFIGS = [
        dict(
        name='ClimateShockFinal',
        app_sequence=["CS1_Intro",
                      "CS2_Forest",
                      "CS3_Anti1",
                      "CS4_Shock",
                      "CS5_Quest",
                      ],
        num_demo_participants=3,
        #use_browser_bots=True,
    ),
        dict(
        name='Intro',
        app_sequence=["CS1_Intro"],
        num_demo_participants=3,
        #use_browser_bots=True,
    ),
        dict(
        name='Forest',
        app_sequence=["CS2_Forest"],
        num_demo_participants=3,
        #use_browser_bots=True,
    ),
        dict(
        name='Anti1',           #Method 1 randomizing
        app_sequence=["CS3_Anti1"],
        num_demo_participants=3,
        #use_browser_bots=True,
    ),
        dict(
        name='Shock',
        app_sequence=["CS4_Shock"],
        num_demo_participants=3,
        #use_browser_bots=True,
    ),
        dict(
        name="Questionnaire", ###### for testing the Questionnaires app. Comment out the ExpBeh parts and the ResultsWaitPage in the app!
        app_sequence=["CS5_Quest"],
        num_demo_participants = 1,
        #use_browser_bots=True,
    )
]

ROOMS = [
        dict(
        name = 'LoFo',
        display_name = 'Lost Forest',
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00,
    participation_fee= 0.00,
    doc=""
)

PARTICIPANT_FIELDS = ["take",
                      "take_history",
                      "current_trees_after_take",
                      "current_trees",
                      "balance",
                      "points_in_stage", # dict of the points earned in each stage
                      "app_payoffs", # dict of payoffs to draw from randomly at the end
                      "game_payoff", # payoff without the show-up fee
                      "high_probability", # role for randomization: Each group plays in anticipation part
                      "is_shock_group",
                      "group_id",
                      "covid_okay",
                      "ceiling_group_take",
                      "take_ceiling",
                      ]
SESSION_FIELDS = ["is_shock_group", # role for randomization: Each group plays for shock no shock in anticipation
                  "high_probability", # role for randomization: Each group plays in anticipation part
                  "shock_probability_high",
                  "shock_probability_low",
                  "group_id",
                  "ceiling_group_take"
                  ]


# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'de'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'EUR'
USE_POINTS = False

ADMIN_USERNAME = 'admin52'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '9422566282351'
