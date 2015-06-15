import os
import tempfile

import coid

from mythicals import form, domain, db

from . import app, DB, request, RequestForm, Response, exc, Index, Link, Id, DecodedId, Resource


class CreditCardVerification(Resource):

    link = Link('credit_card.verification', verification='id')

    id = Id(prefix='CCV-')

    external_id = form.String()

    state = form.String()

    address_matched = form.Boolean()

    postal_code_matched = form.Boolean()

    security_code_matched = form.Boolean()

    code = form.String()

    diagnostics = form.List(form.String())

    class Create(RequestForm):

        id = DecodedId('Verification', default=None)

        external_id = form.String()

        card_number = form.String()

        card_security_code = form.String(default=None)

        address = form.SubForm(domain.CreditCardAddress, default=None)

        params = form.SubForm(domain.CreditCardVerification.Params, default=dict)

    @classmethod
    def create(cls, source, company):
        form = cls.Create(source)
        obj = domain.CreditCardVerification.create(
            company=company.obj, **form
        )
        db.Session.commit()
        obj.inquire()
        db.Session.commit()
        return cls(obj)


CreditCardVerification.bind(DB(domain.CreditCardVerification))


class CreditCardHold(Resource):

    link = Link('credit_card.hold', hold='id')

    id = Id(prefix='CCH-')

    external_id = form.String()

    amount = form.Integer()

    currency = form.String()

    captured_amount = form.Integer()

    state = form.String()

    code = form.String()

    diagnostics = form.List(form.String())

    class Create(RequestForm):

        id = DecodedId('Hold', default=None)

        external_id = form.String()

        card_number = form.String()

        card_security_code = form.String(default=None)

        amount = form.Integer()

        currency = form.String()

        params = form.SubForm(domain.CreditCardHold.Params, default=dict)

    @classmethod
    def create(cls, source, company):
        obj = domain.CreditCardHold.create(
            company=company.obj, **cls.Create(source)
        )
        db.Session.commit()
        obj.open()
        db.Session.commit()
        return cls(obj)


CreditCardHold.bind(DB(domain.CreditCardHold))


class CreditCardSubmission(Resource):

    link = Link('credit_card.submission', submission='id')

    confirmation_link = Link('credit_card.submission.confirmation', submission='id')

    id = Id(prefix='CCS-')

    external_id = form.String()

    trace_id = form.String()

    type = form.String('_type')

    created_at = form.Field()

    location = form.String()

    mime_type = form.String(choices=domain.CreditCardSubmission.mimes.types)

    tally = form.List(form.Field(), 'tally()')

    processed = form.Boolean()

    ops_link = Link('credit_card.submission.ops', submission='id')

    @property
    def ops(self):
        return self.obj.ops

    class Index(Index):

        trace_id = form.String(default=None)

        processed = form.Boolean(default=None)

        external_id = form.String(default=None)

        def filter(self, query):
            if self.after is not None:
                query = query.filter(domain.CreditCardSubmission.updated_at >= self.after)
            if self.before is not None:
                query = query.filter(domain.CreditCardSubmission.updated_at <= self.before)
            if self.processed is not None:
                query = query.filter(domain.CreditCardSubmission.processed == self.processed)
            if self.trace_id is not None:
                query = query.filter(domain.CreditCardSubmission.trace_id == self.trace_id)
            if self.external_id is not None:
                query = query.filter(domain.CreditCardSubmission.external_id == self.external_id)
            return query

    @classmethod
    def create(cls, external_id, company, content_type, stream):
        temp_fd, temp_path = tempfile.mkstemp()
        try:
            os.close(temp_fd)
            with open(temp_path, 'w') as fo:
                fo.write(stream.read())
            obj = domain.CreditCardSubmission.create(
                company=company.obj,
                external_id=external_id,
                location=temp_path,
                mime_type=content_type,
            )
            obj.archive()
            db.Session.commit()
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
        return cls(obj)

    def process(self):
        obj = self.obj.process(coid.Ids(self.registry.id_codecs()))
        db.Session.commit()
        return CreditCardConfirmation(obj)

    def reset(self):
        self.obj.reset()
        return self.refresh()

    def cancel(self):
        db.Session.delete(self.obj)
        db.Session.commit()


CreditCardSubmission.bind(DB(domain.CreditCardSubmission))


class CreditCardConfirmation(Resource):

    link = Link('credit_card.submission.confirmation', submission='submission.id')

    id = Id(prefix='CON-')

    submission_link = Link('credit_card.submission', submission='submission.id')

    submission_id = Id('submission.id', resource='CreditCardSubmission')

    @property
    def submission(self):
        return CreditCardSubmission(self.obj.submission)

    submission_external_id = form.String('submission.external_id')

    created_at = form.Field()

    code = form.String()

    diagnostics = form.List(form.String())


class CreditCardSettlement(Resource):

    link = Link('credit_card.settlement', settlement='id')

    id = Id(prefix='CCT-')

    created_at = form.DateTime()

    ops_link = Link('credit_card.settlement.ops', settlement='id')

    @property
    def ops(self):
        return self.obj.ops

    tally = form.List(form.Field(), 'tally()')

    class Create(RequestForm):

        after = form.DateTime(format='iso8601', default=None)

        before = form.DateTime(format='iso8601', default=None)

        type = form.String(choices=domain.CreditCardOp.types, default=None)

        trace_id = form.String(default=None)

        limit = form.Integer(default=None)

        def __call__(self, query):
            if self.after is not None:
                query = query.filter(domain.CreditCardOp.updated_at >= self.after)
            if self.before is not None:
                query = query.filter(domain.CreditCardOp.updated_at <= self.before)
            if self.type is not None:
                query = query.filter(domain.CreditCardOp._type == self.type)
            if self.trace_id is not None:
                query = query.filter(domain.CreditCardOp.trace_id == self.trace_id)
            if self.limit is not None:
                query = query.limit(self.limit)
            return query

    @classmethod
    def create(cls, source, company):
        query = cls.Create(request.args)(
            company.credit_card_ops
            .filter(~domain.CreditCardOp.has_settlement)
        )
        obj = domain.CreditCardSettlement.create(query)
        db.Session.commit()
        return cls(obj)

    class Index(Index):

        trace_id = form.String(default=None)

        def filter(self, query):
            if self.after is not None:
                query = query.filter(domain.CreditCardSettlement.created_at >= self.after)
            if self.before is not None:
                query = query.filter(domain.CreditCardSettlement.created_at <= self.before)
            if self.trace_id is not None:
                query = query.filter(domain.CreditCardSettlement.trace_id == self.trace_id)
            return query


CreditCardSettlement.bind(DB(domain.CreditCardSettlement))


class CreditCardOp(Resource):

    link = Link('credit_card.op', op='id')

    id = Id(prefix='CCO-')

    external_id = form.String()

    type = form.String('_type')

    state = form.String()

    created_at = form.DateTime()

    confirmed = form.Boolean()

    settled = form.Boolean()

    code = form.String()

    diagnostics = form.List(form.String())

    class Index(Index):

        after = form.DateTime(format='iso8601', default=None)

        before = form.DateTime(format='iso8601', default=None)

        type = form.String(choices=domain.CreditCardOp.types, default=None)

        confirmed = form.Boolean(default=None)

        settled = form.Boolean(default=None)

        trace_id = form.String(default=None)

        executed = form.Boolean(default=None)

        def filter(self, query):
            if self.after is not None:
                query = query.filter(domain.CreditCardOp.updated_at >= self.after)
            if self.before is not None:
                query = query.filter(domain.CreditCardOp.updated_at <= self.before)
            if self.trace_id is not None:
                query = query.filter(domain.CreditCardOp.trace_id == self.trace_id)
            if self.executed is not None:
                query = query.filter(domain.CreditCardOp.executed == self.executed)
            if self.type is not None:
                query = query.filter(domain.CreditCardOp._type <= self.type)
            if self.settled is not None:
                query = query.filter(domain.CreditCardOp.settled == self.settled)
            if self.confirmed is not None:
                query = query.filter(domain.CreditCardOp.confirmed == self.confirmed)
            return query

    def execute(self):
        self.obj()
        db.Session.commit()
        self.refresh()


CreditCardOp.bind(DB(domain.CreditCardOp))


@app.route(
    '/credit_card/verifications/<CreditCardVerification:verification>',
    methods=['GET'],
    endpoint='credit_card.verification',
)
def show_verification(verification):
    request.authorize(verification, 'show')
    encode_type, encode = request.accept_encoder()
    return Response(
        status=200, response=encode(verification), content_type=encode_type,
    )


@app.route(
    '/credit_card/verifications',
    endpoint='credit_card.verify',
    methods=['POST'],
)
def create_verification():
    request.authorize(CreditCardVerification, 'create')
    encode_type, encode = request.accept_encoder()
    source = request.content_source()
    verification = CreditCardVerification.create(source, request.company)
    return Response(
        status=201, response=encode(verification), content_type=encode_type,
    )


@app.route(
    '/credit_card/holds/<CreditCardHold:hold>',
    methods=['GET'],
    endpoint='credit_card.hold',
)
def show_hold(hold):
    request.authorize(hold, 'show')
    encode_type, encode = request.accept_encoder()
    return Response(
        status=200, response=encode(hold), content_type=encode_type,
    )


@app.route(
    '/credit_card/holds',
    endpoint='credit_card.hold.open',
    methods=['POST'],
)
def open_hold():
    request.authorize(CreditCardHold, 'create')
    source = request.content_source()
    encode_type, encode = request.accept_encoder()
    hold = CreditCardHold.create(source, request.company)
    return Response(
        status=201, response=encode(hold), content_type=encode_type,
    )


@app.route(
    '/credit_card/submissions/<external_id>',
    methods=['POST'],
    endpoint='credit_card.submission.create',
)
def create_submission(external_id):
    request.authorize(CreditCardSubmission, 'create')
    encode_type, encode = request.accept_encoder()
    submission = CreditCardSubmission.create(
        external_id, request.company, request.content_type, request.stream
    )
    return Response(
        status=201, response=encode(submission), content_type=encode_type,
    )

@app.route(
    '/credit_card/submissions',
    methods=['GET'],
    endpoint='credit_card.submissions',
)
def index_submissions():
    request.authorize(CreditCardSubmission, 'index')
    encode_type, encode = request.accept_encoder()
    query = request.company.credit_card_submissions
    page = CreditCardSubmission.Index(request.args)(query)
    return Response(
        status=200, response=encode(page), content_type=encode_type,
    )


@app.route(
    '/credit_card/submissions/<CreditCardSubmission:submission>',
    methods=['GET'],
    endpoint='credit_card.submission',
)
def show_submission(submission):
    request.authorize(submission, 'show')
    encode_type, encode = request.accept_encoder()
    return Response(
        status=200, response=encode(submission), content_type=encode_type,
    )


@app.route(
    '/credit_card/submissions/<CreditCardSubmission:submission>/ops',
    methods=['GET'],
    endpoint='credit_card.submission.ops',
)
def submission_ops(submission):
    request.authorize(CreditCardOp, 'index', submission)
    encode_type, encode = request.accept_encoder()
    page = CreditCardOp.Index(request.args)(submission.ops)
    return Response(
        status=200, response=encode(page), content_type=encode_type,
    )

@app.route(
    '/credit_card/submissions/<CreditCardSubmission:submission>/confirmation',
    methods=['GET'],
    endpoint='credit_card.submission.confirmation',
)
def show_confirmation(submission):
    if not submission.processed:
        raise exc.NotFound()
    request.authorize(submission.confirmation, 'show', submission)
    encode_type, encode = request.accept_encoder()
    return Response(
        status=200, response=encode(submission.confirmation), content_type=encode_type,
    )


@app.route(
    '/credit_card/submissions/<CreditCardSubmission:submission>/confirmation',
    methods=['POST'],
    endpoint='credit_card.submission.process',
)
def process_submission(submission):
    request.authorize(submission, 'process')
    encode_type, encode = request.accept_encoder()
    confirmation = submission.process()
    return Response(
        status=201, response=encode(confirmation), content_type=encode_type,
    )


@app.route(
    '/credit_card/submissions/<CreditCardSubmission:submission>/confirmation',
    methods=['DELETE'],
    endpoint='credit_card.submission.reset',
)
def reset_submission(submission):
    request.authorize(submission, 'reset')
    encode_type, encode = request.accept_encoder()
    submission.reset()
    return Response(
        status=200, response=encode(submission), content_type=encode_type,
    )


@app.route(
    '/credit_card/submissions/<CreditCardSubmission:submission>',
    methods=['DELETE'],
    endpoint='credit_card.submission.cancel',
)
def cancel_submission(submission):
    request.authorize(submission, 'cancel')
    submission.cancel()
    return Response(status=204)


@app.route(
    '/credit_card/settlements',
    methods=['POST'],
    endpoint='credit_card.settlement.create',
)
def create_settlement():
    request.authorize(CreditCardSettlement, 'create')
    encode_type, encode = request.accept_encoder()
    settlement = CreditCardSettlement.create(request.args, company=request.company)
    return Response(
        status=201, response=encode(settlement), content_type=encode_type,
    )


@app.route(
    '/credit_card/settlements',
    methods=['GET'],
    endpoint='credit_card.settlements',
)
def index_settlements():
    request.authorize(CreditCardSettlement, 'index')
    encode_type, encode = request.accept_encoder()
    page = CreditCardSettlement.Index(request.args)(
        request.company.credit_card_settlements
    )
    return Response(
        status=200, response=encode(page), content_type=encode_type,
    )


@app.route(
    '/credit_card/settlements/<CreditCardSettlement:settlement>',
    methods=['GET'],
    endpoint='credit_card.settlement',
)
def settlement(settlement):
    request.authorize(settlement, 'show')
    encode_type, encode = request.accept_encoder()
    return Response(
        status=200, response=encode(settlement), content_type=encode_type,
    )


@app.route(
    '/credit_card/settlements/<CreditCardSettlement:settlement>/ops',
    methods=['GET'],
    endpoint='credit_card.settlement.ops',
)
def settlement_ops(settlement):
    request.authorize(CreditCardOp, 'index', settlement)
    encode_type, encode = request.accept_encoder()
    page = CreditCardOp.Index(request.args)(settlement.ops)
    return Response(
        status=200, response=encode(page), content_type=encode_type,
    )


@app.route(
    '/credit_card/ops',
    methods=['GET'],
    endpoint='credit_card.ops',
)
def ops():
    request.authorize(CreditCardOp, 'index')
    encode_type, encode = request.accept_encoder()
    page = CreditCardOp.Index(request.args)(request.company.credit_card_ops)
    return Response(
        status=200, response=encode(page), content_type=encode_type,
    )


@app.route(
    '/credit_card/ops/<CreditCardOp:op>',
    methods=['GET'],
    endpoint='credit_card.op',
)
def show_op(op):
    request.authorize(op, 'show')
    encode_type, encode = request.accept_encoder()
    return Response(
        status=200, response=encode(op), content_type=encode_type,
    )


@app.route(
    '/credit_card/ops/<CreditCardOp:op>',
    methods=['PUT'],
    endpoint='credit_card.op.execute',
)
def execute_op(op):
    request.authorize(op, 'execute')
    encode_type, encode = request.accept_encoder()
    op.execute()
    return Response(
        status=200, response=encode(op), content_type=encode_type,
    )
