from . import http, sftp, pilo, Query, QueryIndex, ResourceMixin, Enum, ConfirmationCodes


Codes = Enum([
    'UNKNOWN',
    'DECLINED',
    'LOCKED',
])


class Verify(pilo.Form, ResourceMixin):

    external_id = pilo.fields.String()

    card_number = pilo.fields.String()

    address = pilo.fields.SubForm.from_fields(
        street=pilo.fields.String(nullable=True, optional=True),
        region=pilo.fields.String(nullable=True, optional=True),
        city=pilo.fields.String(nullable=True, optional=True),
        postal_code=pilo.fields.String(nullable=True, optional=True),
        country_code=pilo.fields.String(nullable=True, optional=True),
    )

    card_security_code = pilo.fields.String(default=None)

    params = pilo.fields.Dict(
        pilo.fields.String(), pilo.fields.Field(), default=None
    )


class OpenHold(pilo.Form, ResourceMixin):

    external_id = pilo.fields.String()

    card_number = pilo.fields.String()

    card_security_code = pilo.fields.String(default=None)

    amount = pilo.fields.Integer()

    currency = pilo.fields.String()

    params = pilo.fields.Dict(
        pilo.fields.String(), pilo.fields.Field(), default=None
    )


class Verification(pilo.Form, ResourceMixin):

    link = pilo.fields.String()

    id = pilo.fields.String()

    external_id = pilo.fields.String()

    address_matched = pilo.fields.Boolean(nullable=True)

    postal_code_matched = pilo.fields.Boolean(nullable=True)

    security_code_matched = pilo.fields.Boolean(nullable=True)

    states = Enum([
        'STAGED',
        'ACCEPTED',
        'REJECTED',
    ])

    state = pilo.fields.String(choices=states)

    @property
    def is_accepted(self):
        return self.state == self.states.ACCEPTED

    code = pilo.fields.String(choices=Codes)

    diagnostics = pilo.fields.List(pilo.fields.String())

    @classmethod
    def inquire(cls, **kwargs):
        source = http.post(
            '/credit_card/verifications', data=Verify(**kwargs)
        )
        return cls(source)


class Hold(pilo.Form, ResourceMixin):

    link = pilo.fields.String()

    id = pilo.fields.String()

    external_id = pilo.fields.String()

    amount = pilo.fields.Integer()

    currency = pilo.fields.String()

    captured_amount = pilo.fields.Integer()

    states = Enum([
        'STAGED',
        'OPEN',
        'CAPTURED',
        'VOIDED',
        'REJECTED',
    ])

    state = pilo.fields.String(choices=states)

    code = pilo.fields.String(choices=Codes)

    diagnostics = pilo.fields.List(pilo.fields.String())

    @classmethod
    def open(cls, **kwargs):
        source = http.post('/credit_card/holds', data=OpenHold(**kwargs))
        return cls(source)


class OpIndex(QueryIndex):

    after = pilo.fields.Datetime(format='iso8601', optional=True)

    before = pilo.fields.Datetime(format='iso8601', optional=True)

    confirmed = pilo.fields.Boolean(optional=True)

    settled = pilo.fields.Boolean(optional=True)

    executed = pilo.fields.Boolean(optional=True)

    trace_id = pilo.fields.String(optional=True)


OpStates = Enum([
    'STAGED',
    'EXECUTING',
    'SUCCEEDED',
    'FAILED',
    'CANCELED',
])


OpTypes = Enum([
    'CAPTURE_HOLD',
    'REVERSE_HOLD_CAPTURE',
    'VOID_HOLD',
    'CREDIT',
])


class Op(pilo.Form, ResourceMixin):

    @classmethod
    def query(cls, **filters):
        return Query('/credit_card/ops', Op, OpIndex(filters))

    link = pilo.fields.String()

    id = pilo.fields.String()

    external_id = pilo.fields.String()

    types = OpTypes

    type = pilo.fields.String(choices=types)

    states = OpStates

    state = pilo.fields.String(choices=OpStates)

    confirmed = pilo.fields.Boolean()

    settled = pilo.fields.Boolean()

    codes = Codes

    code = pilo.fields.String(choices=codes)

    diagnostics = pilo.fields.List(pilo.fields.String())

    def __call__(self):
        return self.execute()

    def execute(self):
        return self.map(http.put(self.link), reset=True, error='raise')


class OpSubmission(pilo.Form):

    external_id = pilo.fields.String()

    code = pilo.fields.String(optional=True)

    diagnostics = pilo.fields.List(pilo.fields.String(), optional=True)


class CaptureHoldSubmission(OpSubmission):

    hold_id = pilo.fields.String()

    amount = pilo.fields.Integer()


class ReverseHoldCaptureSubmission(OpSubmission):

    hold_id = pilo.fields.String()

    amount = pilo.fields.Integer()


class VoidHoldSubmission(OpSubmission):

    hold_id = pilo.fields.String()


class CreditSubmission(OpSubmission):

    card_number = pilo.fields.String()

    card_security_code = pilo.fields.String(default=None)

    amount = pilo.fields.Integer()

    currency = pilo.fields.String()


class Submit(pilo.Form):

    external_id = pilo.fields.String()

    # capture hold

    capture_hold_count = pilo.fields.Integer()

    @capture_hold_count.compute
    def capture_hold_count(self):
        return len(self.capture_holds)

    def capture_hold(self, **kwargs):
        v = CaptureHoldSubmission(kwargs)
        self.capture_holds.append(v)
        return v

    capture_holds = pilo.fields.List(
        pilo.fields.SubForm(CaptureHoldSubmission), default=list
    )

    # reverse hold capture

    reverse_hold_capture_count = pilo.fields.Integer()

    @reverse_hold_capture_count.compute
    def reverse_hold_capture_count(self):
        return len(self.reverse_hold_captures)

    def reverse_hold_capture(self, **kwargs):
        v = ReverseHoldCaptureSubmission(kwargs)
        self.reverse_hold_captures.append(v)
        return v

    reverse_hold_captures = pilo.fields.List(
        pilo.fields.SubForm(ReverseHoldCaptureSubmission), default=list
    )

    # void hold

    void_hold_count = pilo.fields.Integer()

    @void_hold_count.compute
    def void_hold_count(self):
        return len(self.void_holds)

    def void_hold(self, **kwargs):
        v = VoidHoldSubmission(kwargs)
        self.void_holds.append(v)
        return v

    void_holds = pilo.fields.List(
        pilo.fields.SubForm(VoidHoldSubmission), default=list
    )

    credit_count = pilo.fields.Integer()

    @credit_count.compute
    def credit_count(self):
        return len(self.credits)

    def credit(self, **kwargs):
        v = CreditSubmission(kwargs)
        self.credits.append(v)
        return v

    credits = pilo.fields.List(
        pilo.fields.SubForm(CreditSubmission), default=list
    )

    def __call__(self):
        data = type(self)(self)
        response = http.post(
            '/credit_card/submissions/' + self.external_id, data=data,
        )
        return Submission(response)

    def upload(self):
        data = type(self)(self)
        with sftp.connect():
            return sftp.upload(data.external_id, data, 'credit_card')

    @classmethod
    def download(cls, external_id):
        with sftp.connect():
            src = sftp.download(external_id, 'credit_card/submissions')
        return cls(src)


class Confirmation(pilo.Form):

    link = pilo.fields.String()

    id = pilo.fields.String()

    submission_link = pilo.fields.String()

    submission_id = pilo.fields.String()

    submission_external_id = pilo.fields.String()

    created_at = pilo.fields.Datetime(format='iso8601')

    codes = ConfirmationCodes

    code = pilo.fields.String(choices=ConfirmationCodes)

    diagnostics = pilo.fields.List(pilo.fields.String())


class SubmissionIndex(QueryIndex):

    trace_id = pilo.fields.String(optional=True)

    after = pilo.fields.Datetime(format='iso8601', optional=True)

    before = pilo.fields.Datetime(format='iso8601', optional=True)

    processed = pilo.fields.Boolean(optional=True)

    external_id = pilo.fields.String(optional=True)


class Submission(pilo.Form, ResourceMixin):

    link = pilo.fields.String()

    confirmation_link = pilo.fields.String()

    id = pilo.fields.String()

    external_id = pilo.fields.String()

    created_at = pilo.fields.Datetime(format='iso8601')

    processed = pilo.fields.Boolean()

    ops_link = pilo.fields.String()

    @property
    def ops(self):
        return Query(self.ops_link, Op, OpIndex())

    @classmethod
    def get(self, id):
        return Submission(http.get(
            '/credit_card/submissions/{}'.format(id),
        ))

    @classmethod
    def query(cls, **filters):
        return Query(
            '/credit_card/submissions', Submission, SubmissionIndex(filters),
        )

    def confirmation(self):
        return Confirmation(http.get(self.confirmation_link))

    def process(self):
        return Confirmation(http.post(self.confirmation_link))

    def reset(self):
        http.delete(self.confirmation_link)

    def cancel(self):
        http.delete(self.link)


class Settle(pilo.Form):

    after = pilo.fields.Datetime(format='iso8601', optional=True)

    before = pilo.fields.Datetime(format='iso8601', optional=True)

    trace_id = pilo.fields.String(optional=True)

    type = pilo.fields.String(optional=True)

    limit = pilo.fields.Integer(optional=True)

    def __call__(self):
        params = type(self)(self)
        source = http.post('/credit_card/settlements', params=params)
        return Settlement(source)


class SettlementIndex(QueryIndex):

    after = pilo.fields.Datetime(format='iso8601', optional=True)

    before = pilo.fields.Datetime(format='iso8601', optional=True)

    trace_id = pilo.fields.String(optional=True)


class Settlement(pilo.Form):

    link = pilo.fields.String()

    id = pilo.fields.String()

    created_at = pilo.fields.Datetime(format='iso8601')

    ops_link = pilo.fields.String()

    @property
    def ops(self):
        return Query(self.ops_link, Op, OpIndex())

    @classmethod
    def query(self, **filters):
        return Query(
            '/credit_card/settlements', Settlement, SettlementIndex(filters),
        )
