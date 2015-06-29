from . import graft
from facts.conf import settings


@graft
def user_data_info():
    """Returns user data.
    """
    from facts import UserFacts
    user_data = UserFacts(settings.userfacts)
    return user_data.data
