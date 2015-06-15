import os
import tempfile

import coid

from mythicals import form, domain, db

from . import app, DB, Index, Id, Link, Resource, RequestForm, request, exc, Response


class Merchant(Resource):

    link = Link('merchant', merchant='id')

    id = Id(prefix='MR-')

    external_id = form.String()

    created_at = form.DateTime()

    state = form.String()

    class Index(Index):

        trace_id = form.String(default=None)


Merchant.bind(DB(domain.Merchant))


class MerchantSubmission(Resource):

    link = Link('merchant.submission', submission='id')

    confirmation_link = Link('merchant.submission.confirmation', submission='id')

    id = Id(prefix='MRS-')

    external_id = form.String()

    type = form.String('_type')

    created_at = form.Field()

    location = form.String()

    mime_type = form.String(choices=domain.MerchantSubmission.mimes.types)

    tally = form.List(form.Field(), 'tally()')

    processed = form.Boolean()

    trace_id = form.String()

    ops_link = Link('merchant.submission.ops', submission='id')

    @property
    def ops(self):
        return self.obj.ops

    class Index(Index):

        trace_id = form.String(default=None)

        processed = form.Boolean(default=None)

        def filter(self, query):
            if self.after is not None:
                query = query.filter(domain.MerchantSubmission.updated_at >= self.after)
            if self.before is not None:
                query = query.filter(domain.MerchantSubmission.updated_at <= self.before)
            if self.processed is not None:
                query = query.filter(domain.MerchantSubmission.processed == self.processed)
            if self.trace_id is not None:
                query = query.filter(domain.MerchantSubmission.trace_id == self.trace_id)
            return query

    @classmethod
    def create(cls, external_id, content_type, stream, company):
        temp_fd, temp_path = tempfile.mkstemp()
        try:
            os.close(temp_fd)
            with open(temp_path, 'w') as fo:
                fo.write(stream.read())
            obj = domain.MerchantSubmission.create(
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
        return MerchantConfirmation(obj)

    def reset(self):
        self.obj.reset()
        return self.refresh()

    def cancel(self):
        db.Session.delete(self.obj)
        db.Session.commit()


MerchantSubmission.bind(DB(domain.MerchantSubmission))


class MerchantConfirmation(Resource):

    link = Link('merchant.submission.confirmation', submission='submission.id')

    id = Id(prefix='CON-')

    submission_link = Link('merchant.submission', submission='submission.id')

    submission_id = Id('submission.id', resource='MerchantSubmission')

    @property
    def submission(self):
        return MerchantSubmission(self.obj.submission)

    submission_external_id = form.String('submission.external_id')

    created_at = form.Field()

    code = form.String()

    diagnostics = form.List(form.String())


class MerchantSettlement(Resource):

    link = Link('merchant.settlement', settlement='id')

    id = Id(prefix='MRT-')

    created_at = form.DateTime()

    ops_link = Link('merchant.settlement.ops', settlement='id')

    @property
    def ops(self):
        return self.obj.ops

    tally = form.List(form.Field(), 'tally()')

    class Index(Index):

        trace_id = form.String(default=None)

        def filter(self, query):
            if self.after is not None:
                query = query.filter(domain.MerchantSettlement.updated_at >= self.after)
            if self.before is not None:
                query = query.filter(domain.MerchantSettlement.updated_at <= self.before)
            if self.trace_id is not None:
                query = query.filter(domain.MerchantSettlement.trace_id == self.trace_id)
            return query

    class Create(RequestForm):

        after = form.DateTime(format='iso8601', default=None)

        before = form.DateTime(format='iso8601', default=None)

        type = form.String(choices=domain.MerchantOp.types, default=None)

        trace_id = form.String(default=None)

        limit = form.Integer(default=None)

        def __call__(self, query):
            if self.after is not None:
                query = query.filter(domain.MerchantOp.updated_at >= self.after)
            if self.before is not None:
                query = query.filter(domain.MerchantOp.updated_at <= self.before)
            if self.type is not None:
                query = query.filter(domain.MerchantOp._type == self.type)
            if self.trace_id is not None:
                query = query.filter(domain.MerchantOp.trace_id == self.trace_id)
            if self.limit is not None:
                query = query.limit(self.limit)
            return query

    @classmethod
    def create(cls, source, company):
        query = cls.Create(request.args)(
            company.merchant_ops
            .filter(~domain.MerchantOp.has_settlement)
        )
        obj = domain.MerchantSettlement.create(query)
        db.Session.commit()
        return cls(obj)


MerchantSettlement.bind(DB(domain.MerchantSettlement))


class MerchantOp(Resource):

    link = Link('merchant.op', op='id')

    id = Id(prefix='MRO-')

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

        type = form.String(choices=domain.MerchantOp.types, default=None)

        confirmed = form.Boolean(default=None)

        settled = form.Boolean(default=None)

        trace_id = form.String(default=None)

        def filter(self, query):
            if self.after is not None:
                query = query.filter(domain.MerchantOp.updated_at >= self.after)
            if self.before is not None:
                query = query.filter(domain.MerchantOp.updated_at <= self.before)
            if self.type is not None:
                query = query.filter(domain.MerchantOp._type <= self.type)
            if self.settled is not None:
                query = query.filter(domain.MerchantOp.settled == self.settled)
            if self.confirmed is not None:
                query = query.filter(domain.MerchantOp.confirmed == self.confirmed)
            if self.trace_id is not None:
                query = query.filter(domain.MerchantOp.trace_id == self.trace_id)
            return query

    def execute(self):
        self.obj()
        db.Session.commit()
        self.refresh()


MerchantOp.bind(DB(domain.MerchantOp))


@app.route(
    '/merchant/submissions/<external_id>',
    endpoint='merchant.submission.create',
    methods=['POST'],
)
def submit(external_id):
    request.authorize(MerchantSubmission, 'create')
    encode_type, encode = request.accept_encoder()
    submission = MerchantSubmission.create(
        external_id, request.content_type, request.stream, request.company
    )
    return Response(
        status=201, response=encode(submission), content_type=encode_type,
    )


@app.route(
    '/merchant/submissions/<MerchantSubmission:submission>/confirmation',
    methods=['POST'],
    endpoint='merchant.submission.process',
)
def process(submission):
    request.authorize(submission, 'process')
    encode_type, encode = request.accept_encoder()
    confirmation = submission.process()
    return Response(
        status=201, response=encode(confirmation), content_type=encode_type,
    )


@app.route(
    '/merchant/submissions/<MerchantSubmission:submission>/confirmation',
    methods=['DELETE'],
    endpoint='merchant.submission.reset',
)
def reset(submission):
    request.authorize(submission, 'reset')
    encode_type, encode = request.accept_encoder()
    submission.reset()
    return Response(
        status=200, response=encode(submission), content_type=encode_type,
    )


@app.route(
    '/merchant/submissions/<MerchantSubmission:submission>',
    methods=['DELETE'],
    endpoint='merchant.submission.cancel',
)
def cancel(submission):
    request.authorize(submission, 'cancel')
    submission.cancel()
    return Response(status=204)


@app.route(
    '/merchant/submissions', methods=['GET'], endpoint='merchant.submissions',
)
def index_submissions():
    request.authorize(MerchantSubmission, 'cancel')
    encode_type, encode = request.accept_encoder()
    page = MerchantSubmission.Index(request.args)(
        request.company.merchant_submissions
    )
    return Response(
        status=200, response=encode(page), content_type=encode_type,
    )


@app.route(
    '/merchant/submissions/<MerchantSubmission:submission>',
    methods=['GET'],
    endpoint='merchant.submission',
)
def show_submission(submission):
    request.authorize(submission, 'show')
    encode_type, encode = request.accept_encoder()
    return Response(
        status=200, response=encode(submission), content_type=encode_type,
    )


@app.route(
    '/merchant/submissions/<MerchantSubmission:submission>/ops',
    methods=['GET'],
    endpoint='merchant.submission.ops',
)
def index_submission_ops(submission):
    request.authorize(MerchantOp, 'index', submission)
    encode_type, encode = request.accept_encoder()
    page = MerchantOp.Index(request.args)(submission.ops)
    return Response(
        status=200, response=encode(page), content_type=encode_type,
    )


@app.route(
    '/merchant/submissions/<MerchantSubmission:submission>/confirmation',
    methods=['GET'],
    endpoint='merchant.submission.confirmation',
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
    '/merchant/settlements',
    methods=['POST'],
    endpoint='merchant.settlement.create',
)
def create_settlement():
    request.authorize(MerchantSettlement, 'create')
    encode_type, encode = request.accept_encoder()
    settlement = MerchantSettlement.create(request.args, company=request.company)
    return Response(
        status=201, response=encode(settlement), content_type=encode_type,
    )


@app.route(
    '/merchant/settlements',
    methods=['GET'],
    endpoint='merchant.settlements',
)
def index_settlements():
    request.authorize(MerchantSettlement, 'index')
    encode_type, encode = request.accept_encoder()
    page = MerchantSettlement.Index(request.args)(
        request.company.merchant_settlements
    )
    return Response(
        status=200, response=encode(page), content_type=encode_type,
    )


@app.route(
    '/merchant/settlements/<MerchantSettlement:settlement>',
    methods=['GET'],
    endpoint='merchant.settlement',
)
def show_settlement(settlement):
    request.authorize(settlement, 'show')
    encode_type, encode = request.accept_encoder()
    return Response(
        status=200, response=encode(settlement), content_type=encode_type,
    )


@app.route(
    '/merchant/settlements/<MerchantSettlement:settlement>/ops',
    methods=['GET'],
    endpoint='merchant.settlement.ops',
)
def index_settlement_ops(settlement):
    request.authorize(MerchantOp, 'index', settlement)
    encode_type, encode = request.accept_encoder()
    page = MerchantOp.Index(request.args)(settlement.ops)
    return Response(
        status=200, response=encode(page), content_type=encode_type,
    )


@app.route(
    '/merchant/ops',
    methods=['GET'],
    endpoint='merchant.ops',
)
def index_ops():
    request.authorize(MerchantOp, 'index')
    encode_type, encode = request.accept_encoder()
    page = MerchantOp.Index(request.args)(request.company.merchant_ops)
    return Response(
        status=200, response=encode(page), content_type=encode_type,
    )


@app.route(
    '/merchant/ops/<MerchantOp:op>',
    methods=['GET'],
    endpoint='merchant.op',
)
def show_op(op):
    request.authorize(op, 'show')
    encode_type, encode = request.accept_encoder()
    return Response(
        status=200, response=encode(op), content_type=encode_type,
    )


@app.route(
    '/merchant/ops/<MerchantOp:op>',
    methods=['PUT'],
    endpoint='merchant.op.execute',
)
def execute_op(op):
    request.authorize(op, 'execute')
    encode_type, encode = request.accept_encoder()
    op.execute()
    return Response(
        status=200, response=encode(op), content_type=encode_type,
    )
