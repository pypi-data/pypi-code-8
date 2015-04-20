__author__ = 'hvishwanath'

import yaml
from models import *

class PlanParser(object):

    @classmethod
    def parse(cls, planfile):
        y = yaml.safe_load(file(planfile))
        return CAMPPlan.create_from_dict(y)



