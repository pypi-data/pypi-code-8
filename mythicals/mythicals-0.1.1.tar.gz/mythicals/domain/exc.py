class VerificationNotStaged(Exception):

    def __init__(self, verification):
        super(VerificationNotStaged, self).__init__()
        self.verification = verification


class HoldNotStaged(Exception):

    def __init__(self, hold):
        super(HoldNotStaged, self).__init__()
        self.hold = hold


class HoldNotOpen(Exception):

    def __init__(self, hold):
        super(HoldNotOpen, self).__init__()
        self.hold = hold


class InvalidHoldCaptureAmount(ValueError):

    def __init__(self, hold, amount):
        super(InvalidHoldCaptureAmount, self).__init__()
        self.hold = hold
        self.amount = amount
