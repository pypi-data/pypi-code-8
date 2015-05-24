class MongoAccountBroker(object):
    """
    Mongo implementation of AccountBroker. Each mongo documment has to have:
    {
        account_id:
            {
                account: "Name of the account"
                secret: "some secret string",
                rights: ["someright", "someotherright"],
            },
        ...
    }
    """
    def __init__(self, database, collection=None):
        self.accounts = database
        self.collection = collection

    def get_key(self, account):
        try:
            return self.accounts.db[self.collection].find_one({"account": account})["key"]
        except KeyError:
            return None

    def has_rights(self, account, rights):
        try:
            account_rights = self.accounts.db[self.collection].find_one({"account": account})["rights"]
        except KeyError:
            return False
        return set(rights).issubset(account_rights)

    def is_active(self, account):
        return self.accounts.db[self.collection].find_one({"account": account}) is not None
