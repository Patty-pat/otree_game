from otree.api import Currency as c, currency_range, expect, Bot, SubmissionMustFail
from . import *

class PlayerBot(Bot):
    cases = [ 'norm', 'pros','cons',]  #norm: normal behavior, pros:prosocial behav, cons:selfish behavior

    def play_round(self):
        yield P02Welcome, dict()
        yield Submission(StageDivider, dict(foo=99), check_html=False)
        yield P03InstructionsN, dict()

        yield P04Example, dict()
        

        if self.case == 'norm':
            yield P05ComprehensionCheck, dict(compr1 = 1, compr2 = 0, compr3 = 7, compr4 = 1, compr5 = 0)
        elif self.case == 'pros':
            yield P05ComprehensionCheck, dict(compr1 = 1, compr2 = 0, compr3 = 7, compr4 = 1, compr5 = 0)
        else:
            yield P05ComprehensionCheck, dict(compr1 = 1, compr2 = 0, compr3 = 7, compr4 = 1, compr5 = 0)

        yield P06ComprehensionSuccess, dict(code = 2206)

        
        





