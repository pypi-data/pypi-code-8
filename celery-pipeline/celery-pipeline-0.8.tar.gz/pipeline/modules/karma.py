
from pipeline.actions import action, TaskResult
from pipeline.tasks import TaskResult
from pipeline.command import CommandResult
import logging

logger = logging.getLogger(__name__)


import requests
import json
import base64
import re

class Team(object):
    samurai_fighters = "Samurai Fighters"
    a_team = "A Team"
    usual_suspects = "Usual Suspects"
    djangsters = "Djangsters"
    rangers = "NY Rangers"
    islanders = "Islanders"
    scrum_bags = "Scrum Bags"
    think_kites = "Think Kites"
    falcons = "Falcons"
    param = "Param"
    killer_instinct = "Killer Instinct"
    core = "Core"
    others = "Others"
    fugu = "Fugu"
    cms = "CMS"

class GitUsers(object):

    #E001868
    #E001861

    user_dict = {
        "mike" : Team.samurai_fighters,
        "kulawansad" : Team.islanders,
        "yusuf-samiwala" : Team.others,
        "denzil-tarakan" : Team.usual_suspects,
        "E002070" : Team.scrum_bags, #"Macie"
        "veeravap" : Team.scrum_bags,
        "revanth-yesireddy" : Team.djangsters,
        "sushma-sharma" : Team.a_team,
        "ashish-gore" : Team.a_team,
        "DT2" : Team.others,
        "ananya-thakur":  Team.others,
        "patricia-byrne": Team.core,
        "andrew-keym" : Team.others,
        "phani-mallampalli" : Team.usual_suspects,
        "letor" : Team.islanders,
        "ganesh-adike" : Team.a_team,
        "madhava-challa" : Team.samurai_fighters,
        "Chaitanya" : Team.usual_suspects,
        "ravis" : Team.a_team,
        "jilesh-lakhani" : Team.others,
        "krishna-akkala" : Team.others,
        "praveen-pothana" : Team.others,
        "Miteshkumar-patel" : Team.think_kites,
        "alok-shelar" : Team.param,
        "amit-jain" : Team.think_kites,
        "kotlyav" : Team.islanders,
        "vikram-singam" : Team.samurai_fighters,
        "perminder-singh" : Team.islanders,
        "greg" : Team.djangsters,
        "E002327" : Team.others,
        "E001682" : Team.others,
        "rajesh-rana" : Team.others,
        "E002369" : Team.others,
        "Venkat-Vege" : Team.others,
        "nagarar" : Team.others,
        "kamlesh-vaishnav" : Team.others,
        "deepak-gahlot" : Team.others,
        "vijay-pahuja" : Team.others,
        "E002412" : Team.others,
        "E002411" : Team.others,
        "DRS" : Team.others,
        "akshay-vats" : Team.others,
        "anil-sharma" : Team.others,
        "Rajanikanth-Susarapu" : Team.scrum_bags,
        "Sean" : Team.usual_suspects,
        "ENVISAGE" : Team.others,
        "nader-abdelsadek" : Team.islanders,
        "john-o-shea" : Team.others,
        "E002015" : Team.others, #Shanta
        "E002515" :Team.others,
        "ravi-meesala" : Team.islanders,
        "Kapil-Bhatia" : Team.others,
        "shounak-de" : Team.core,
        "arun-chintam" : Team.core,
        "john-clements" : Team.core,
        "craig-bateman" : Team.core,
        "E002524" : Team.core,
        "Shanthosh-Stanislaus" : Team.others,
        "pavan-athota" : Team.others,
        "mike-miklancic" : Team.others,
        "Nicholas-Dunnaway" : Team.cms,
        "dan-heilman" : Team.others,
        "isakovn" : Team.others,
        "E002593" : Team.others,
        "Thomas-Kahnoski" : Team.others,
        "Willis-Godwin" : Team.others,
        "nick-maly" : Team.others,
        "patelm" : Team.others,
        "Charlee-Li"  : Team.others,
        "andrew-baird" : Team.others,
        "slava-filonenko"  : Team.others,
        "manish-kumar": Team.think_kites,
        "mikhail-starovoytov": Team.cms,
        "tommy-han": Team.islanders,
        "taras-kudla": Team.usual_suspects,
        "ajit-pai": Team.falcons,
        "miki725": Team.djangsters,
        "Dmitriy-Rozentul": Team.others,
        "Shreeyansh-Jain": Team.falcons,
        "khaled-porlin": Team.a_team,
        "sachin-jat": Team.think_kites,
        "Irene": Team.others,
        "naveen-reddy": Team.think_kites,
        "aniket-shelar": Team.think_kites,
        "agamdua": Team.samurai_fighters,
        "sundeep": Team.think_kites,
        "zaheer-shaik": Team.others,
        "kirt-gittens": Team.a_team,
        "milind": Team.djangsters,
        "Vimal-Jayachandran": Team.think_kites,
        "kumar-varadarajulu": Team.falcons,
        "thukaram-hulugappa": Team.cms,
        "Mark-Churney": Team.islanders,
        "scott-overholser": Team.others,
        "tony-mack": Team.falcons,
        "william-freeman": Team.fugu,
        "darrel-bonner": Team.others,
        "ram-chauhan": Team.others,
        "stephen-castle": Team.scrum_bags,
        "Abhishek-Sharma": Team.others,
        "ashok-vijay": Team.others,
        "Malarmannan-Polappan": Team.others,
        "timothy-chi": Team.others,
        "srinivas-thatipathy": Team.falcons,
        "arvind-singh": Team.others,
        "amninder": Team.scrum_bags,
        "miguel-molina": Team.others,
        "rajesh-kumar": Team.falcons,
        "Purandar-Palagala": Team.others,
    }

result = {}
def karma_rules(review_comment):
    """
    rules to increase or decrease score
    #blocker - minus
    :+1: - plus
    +1 - plus
    thank - plus
    #karma+
    #karma-
    #karma++
    #karma--
    """
    up_score_search_items = [(":+1:", "+1"), "thank"]
    down_score_search_items = ["#blocker"]

    score = 0
    analysis_dict = {}

    for item in up_score_search_items:
        if isinstance(item, tuple):
            for tuple_item in item:
                if tuple_item in review_comment:
                    analysis_dict[tuple_item] = analysis_dict.get(tuple_item, 0) + 1
                    score += 1
                    break
        else:
            if item in review_comment:
                analysis_dict[item] = analysis_dict.get(item, 0) + 1
                score += 1

    for item in down_score_search_items:
        if item in review_comment:
            analysis_dict[item] = analysis_dict.get(item, 0) + 1
            score -= 1

    karma_match = re.findall(r"#karma[\+\-]*", review_comment)

    for item in karma_match:
        for c in item:
            if c == "+":
                analysis_dict["#karma_plus"] = analysis_dict.get("#karma_minus", 0) + 1
                score += 1
            elif c == "-":
                analysis_dict["#karma_minus"] = analysis_dict.get("#karma_minus", 0) + 1
                score -= 1

    return score, analysis_dict


def update_result(team, new_score, analysis_dict, result):

    result[team]["score"] = new_score

    if "analysis" not in result[team]:
        result[team]["analysis"] = {}

    a_dict = result[team]["analysis"]
    for k, v in analysis_dict.iteritems():
        value = a_dict.get(k, 0) + v
        result[team]["analysis"][k] = value


@action(name='karmabot')
def karmabot(self, retval, source):
    if type(source) == 'PrBuilderStatusSource':
        return TaskResult(True)  #hack
    from pipeline.command import CommandResult
    return CommandResult(True, output=karma_rules(source.body))

