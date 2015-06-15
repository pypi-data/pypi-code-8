import os
import tempfile

import coid

from mythicals import form, domain, db

from . import app, request, RequestForm, Response, exc, Index, DB, Resource, Id, Link


class BankAccountSubmission(Resource):

    link = Link('bank_account.submission', submission='id')

    confirmation_link = Link('bank_account.submission.confirmation', submission='id')

    id = Id(prefix='BAS-')

    external_id = form.String()

    type = form.String('_type')

    created_at = form.Field()

    location = form.String()

    mime_type = form.String(choices=domain.BankAccountSubmission.mimes.types)

    tally = form.List(form.Field(), 'tally()')

    processed = form.Boolean()

    trace_id = form.String()

    ops_link = Link('bank_account.submission.ops', submission='id')

    @property
    def ops(self):
        return self.obj.ops

    class Index(Index):

        trace_id = form.String(default=None)

        processed = form.Boolean(default=None)

        external_id = form.String(default=None)

        def filter(self, query):
            if self.after is not None:
                query = query.filter(domain.BankAccountSubmission.updated_at >= self.after)
            if self.before is not None:
                query = query.filter(domain.BankAccountSubmission.updated_at <= self.before)
            if self.processed is not None:
                query = query.filter(domain.BankAccountSubmission.processed == self.processed)
            if self.trace_id is not None:
                query = query.filter(domain.BankAccountSubmission.trace_id == self.trace_id)
            if self.external_id is not None:
                query = query.filter(domain.BankAccountSubmission.external_id == self.external_id)
            return query

    @classmethod
    def create(cls, external_id, content_type, stream, company):
        temp_fd, temp_path = tempfile.mkstemp()
        try:
            os.close(temp_fd)
            with open(temp_path, 'w') as fo:
                fo.write(stream.read())
            obj = domain.BankAccountSubmission.create(
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
        return BankAccountConfirmation(obj)

    def reset(self):
        self.obj.reset()
        return self.refresh()

    def cancel(self):
        db.Session.delete(self.obj)
        db.Session.commit()


BankAccountSubmission.bind(DB(domain.BankAccountSubmission))


class BankAccountConfirmation(Resource):

    link = Link('bank_account.submission.confirmation', submission='submission.id')

    id = Id(prefix='CON-')

    submission_link = Link('bank_account.submission', submission='submission.id')

    submission_id = Id('submission.id', resource='BankAccountSubmission')

    @property
    def submission(self):
        return BankAccountSubmission(self.obj.submission)

    submission_external_id = form.String('submission.external_id')

    created_at = form.Field()

    code = form.String()

    diagnostics = form.List(form.String())


class BankAccountSettlement(Resource):

    link = Link('bank_account.settlement', settlement='id')

    id = Id(prefix='BAT-')

    created_at = form.DateTime(format='iso8601')

    ops_link = Link('bank_account.settlement.ops', settlement='id')

    @property
    def ops(self):
        return self.obj.ops

    tally = form.List(form.Field(), 'tally()')

    class Create(RequestForm):

        after = form.DateTime(format='iso8601', default=None)

        before = form.DateTime(format='iso8601', default=None)

        type = form.String(choices=domain.BankAccountOp.types, default=None)

        trace_id = form.String(default=None)

        limit = form.Integer(default=None)

        def  __call__(self, query):
            if self.after is not None:
                query = query.filter(domain.BankAccountOp.updated_at >= self.after)
            if self.before is not None:
                query = query.filter(domain.BankAccountOp.updated_at <= self.before)
            if self.type is not None:
                query = query.filter(domain.BankAccountOp._type == self.type)
            if self.trace_id is not None:
                query = query.filter(domain.BankAccountOp.trace_id == self.trace_id)
            if self.limit is not None:
                query = query.limit(self.limit)
            return query

    @classmethod
    def create(cls, source, company):
        query = cls.Create(source)(
            company.bank_account_ops
            .filter(~domain.BankAccountOp.has_settlement)
        )
        obj = domain.BankAccountSettlement.create(query)
        db.Session.commit()
        return cls(obj)

    class Index(Index):

        trace_id = form.String(default=None)

        def filter(self, query):
            if self.after is not None:
                query = query.filter(domain.BankAccountSettlement.created_at >= self.after)
            if self.before is not None:
                query = query.filter(domain.BankAccountSettlement.created_at <= self.before)
            if self.trace_id is not None:
                query = query.filter(domain.BankAccountSettlement.trace_id == self.trace_id)
            return query


BankAccountSettlement.bind(DB(domain.BankAccountSettlement))


class BankAccountOp(Resource):

    link = Link('bank_account.op', op='id')

    id = Id(prefix='BAO-')

    external_id = form.String()

    type = form.String('_type', choices=domain.BankAccountOp.types)

    state = form.String()

    created_at = form.DateTime(format='iso8601')

    confirmed = form.Boolean()

    settled = form.Boolean()

    code = form.String()

    diagnostics = form.List(form.String())

    class Index(Index):

        after = form.DateTime(format='iso8601', default=None)

        before = form.DateTime(format='iso8601', default=None)

        type = form.String(choices=domain.BankAccountOp.types, default=None)

        confirmed = form.Boolean(default=None)

        settled = form.Boolean(default=None)

        trace_id = form.String(default=None)

        def filter(self, query):
            if self.after is not None:
                query = query.filter(domain.BankAccountOp.updated_at >= self.after)
            if self.before is not None:
                query = query.filter(domain.BankAccountOp.updated_at <= self.before)
            if self.type is not None:
                query = query.filter(domain.BankAccountOp._type == self.type)
            if self.settled is not None:
                query = query.filter(domain.BankAccountOp.settled == self.settled)
            if self.confirmed is not None:
                query = query.filter(domain.BankAccountOp.confirmed == self.confirmed)
            if self.trace_id is not None:
                query = query.filter(domain.BankAccountOp.trace_id == self.trace_id)
            return query

    def execute(self):
        self.obj()
        db.Session.commit()
        self.refresh()


BankAccountOp.bind(DB(domain.BankAccountOp))


@app.route(
    '/bank_account/submissions/<external_id>',
    methods=['POST'],
    endpoint='bank_account.submission.create',
)
def create_submission(external_id):
    request.authorize(BankAccountSubmission, 'create')
    encode_type, encode = request.accept_encoder()
    submission = BankAccountSubmission.create(
        external_id, request.content_type, request.stream, request.company,
    )
    return Response(
        status=201, response=encode(submission), content_type=encode_type,
    )

@app.route(
    '/bank_account/submissions',
    methods=['GET'],
    endpoint='bank_account.submissions',
)
def index_submissions():
    request.authorize(BankAccountSubmission, 'index')
    encode_type, encode = request.accept_encoder()
    page = BankAccountSubmission.Index(request.args)(
        request.company.bank_account_submissions
    )
    return Response(
        status=200, response=encode(page), content_type=encode_type,
    )


@app.route(
    '/bank_account/submissions/<BankAccountSubmission:submission>',
    methods=['GET'],
    endpoint='bank_account.submission',
)
def show_submission(submission):
    request.authorize(submission, 'show')
    encode_type, encode = request.accept_encoder()
    return Response(
        status=200, response=encode(submission), content_type=encode_type,
    )


@app.route(
    '/bank_account/submissions/<BankAccountSubmission:submission>/ops',
    methods=['GET'],
    endpoint='bank_account.submission.ops',
)
def submission_ops(submission):
    request.authorize(BankAccountOp, 'index', submission)
    encode_type, encode = request.accept_encoder()
    page = BankAccountOp.Index(request.args)(submission.ops)
    return Response(
        status=200, response=encode(page), content_type=encode_type,
    )

@app.route(
    '/bank_account/submissions/<BankAccountSubmission:submission>/confirmation',
    methods=['GET'],
    endpoint='bank_account.submission.confirmation',
)
def submission_confirmation(submission):
    if not submission.processed:
        raise exc.NotFound()
    request.authorize(submission.confirmation, 'show')
    encode_type, encode = request.accept_encoder()
    return Response(
        status=200, response=encode(submission.confirmation), content_type=encode_type,
    )


@app.route(
    '/bank_account/submissions/<BankAccountSubmission:submission>/confirmation',
    methods=['POST'],
    endpoint='bank_account.submission.process',
)
def process_submission(submission):
    request.authorize(submission, 'process')
    encode_type, encode = request.accept_encoder()
    confirmation = submission.process()
    return Response(
        status=201, response=encode(confirmation), content_type=encode_type,
    )


@app.route(
    '/bank_account/submissions/<BankAccountSubmission:submission>/confirmation',
    methods=['DELETE'],
    endpoint='bank_account.submission.reset',
)
def reset_submission(submission):
    request.authorize(submission, 'reset')
    encode_type, encode = request.accept_encoder()
    submission.reset()
    return Response(
        status=200, response=encode(submission), content_type=encode_type,
    )


@app.route(
    '/bank_account/submissions/<BankAccountSubmission:submission>',
    methods=['DELETE'],
    endpoint='bank_account.submission.cancel',
)
def cancel_submission(submission):
    request.authorize(submission, 'cancel')
    submission.cancel()
    return Response(status=204)


@app.route(
    '/bank_account/settlements',
    methods=['POST'],
    endpoint='bank_account.settlement.create',
)
def create_settlement():
    request.authorize(BankAccountSettlement, 'create')
    encode_type, encode = request.accept_encoder()
    settlement = BankAccountSettlement.create(
        request.args, company=request.company
    )
    return Response(
        status=201, response=encode(settlement), content_type=encode_type,
    )


@app.route(
    '/bank_account/settlements',
    methods=['GET'],
    endpoint='bank_account.settlements',
)
def index_settlements():
    encode_type, encode = request.accept_encoder()
    query = request.company.bank_account_settlements
    page = BankAccountSettlement.Index(request.args)(query)
    return Response(
        status=200, response=encode(page), content_type=encode_type,
    )


@app.route(
    '/bank_account/settlements/<BankAccountSettlement:settlement>',
    methods=['GET'],
    endpoint='bank_account.settlement',
)
def show_settlement(settlement):
    request.authorize(settlement, 'show')
    encode_type, encode = request.accept_encoder()
    return Response(
        status=200, response=encode(settlement), content_type=encode_type,
    )


@app.route(
    '/bank_account/settlements/<BankAccountSettlement:settlement>/ops',
    methods=['GET'],
    endpoint='bank_account.settlement.ops',
)
def index_settlement_ops(settlement):
    request.authorize(BankAccountOp, 'index', settlement)
    encode_type, encode = request.accept_encoder()
    page = BankAccountOp.Index(request.args)(settlement.ops)
    return Response(
        status=200, response=encode(page), content_type=encode_type,
    )


@app.route(
    '/bank_account/ops',
    methods=['GET'],
    endpoint='bank_account.ops',
)
def index_ops():
    request.authorize(BankAccountOp, 'index')
    encode_type, encode = request.accept_encoder()
    query = request.company.bank_account_ops
    page = BankAccountOp.Index(request.args)(query)
    return Response(
        status=200, response=encode(page), content_type=encode_type,
    )


@app.route(
    '/bank_account/ops/<BankAccountOp:op>',
    methods=['GET'],
    endpoint='bank_account.op',
)
def show_op(op):
    request.authorize(op, 'show')
    encode_type, encode = request.accept_encoder()
    return Response(
        status=200, response=encode(op), content_type=encode_type,
    )


@app.route(
    '/bank_account/ops/<BankAccountOp:op>',
    methods=['PUT'],
    endpoint='bank_account.op.execute',
)
def execute_op(op):
    request.authorize(op, 'execute')
    encode_type, encode = request.accept_encoder()
    op.execute()
    return Response(
        status=200, response=encode(op), content_type=encode_type,
    )
