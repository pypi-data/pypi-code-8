
class CakeTypes(object):

    def __init__(self):
        self.TextType = "TEXT"
        self.NumericType = "NUM"
        self.RealType = "REAL"
        self.IntegerType = "INT"


class CakeModel(object):

    def __init__(self):
        super(CakeModel, self).__init__()
        self.types = CakeTypes()


class Client(CakeModel):

    def __init__(self):
        super(Client, self).__init__()
        self.nombre = self.types.TextType
        self.edad = self.types.IntegerType


class Table(object):

    def __init__(self, model):
        super(Table, self).__init__()
        self.model = model
        self.properties = {}

    def create_table(self):
        pass

    def disect_model(self):

        table_name = self.model.__class__.__name__
        self.properties[table_name] = {}
        for key in self.model.__dict__.keys():
            if not isinstance(self.model.__dict__[key], CakeTypes):
                # print "Key:" + key + " Value: " + self.model.__dict__[key]
                self.properties[table_name][key] = self.model.__dict__[key]
        print self.properties



t = Table(Client())
t.disect_model()
