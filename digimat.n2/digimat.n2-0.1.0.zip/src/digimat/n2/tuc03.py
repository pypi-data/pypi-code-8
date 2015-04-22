from n2 import N2Device

class TUC03(N2Device):
    def onInit(self):
        self.alias(self.InternalFloat(12), 'ambiance')

    def onPing(self):
        if self['ambiance'].readCurrentValue() is not None:
            return True

    def ambiance(self):
        return self.item('ambiance').readCurrentValue()


