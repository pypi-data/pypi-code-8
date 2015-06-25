from . import graft
from facts.conf import settings


@graft
def generate():
    from facts import UserFacts
    user_data = UserFacts(settings.userfacts)
    return user_data.data
