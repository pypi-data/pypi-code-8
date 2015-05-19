from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
import logging

from .forms import PostbackForm
from .models import PostbackLog
from .signals import payment_cancelled, payment_received
from .utils import get_transaction_id

logger = logging.getLogger('touchnet')

@csrf_exempt
def postback(request):
    status = None
    result = None

    if request.method == 'POST':
        form = PostbackForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            transaction_id = get_transaction_id(cleaned_data['EXT_TRANS_ID'])

            if cleaned_data['pmt_status'] == PostbackLog.PAYMENT_SUCCESS:
                signal_results = payment_received.send_robust(sender='touchnet_postback',
                        amount=cleaned_data['pmt_amt'], transaction_id=transaction_id)
            elif cleaned_data['pmt_status'] == PostbackLog.PAYMENT_CANCELLED:
                signal_results = payment_cancelled.send_robust(sender='touchnet_postback',
                        transaction_id=transaction_id)
            signal_exceptions = filter(lambda function_exception: function_exception[1], signal_results)

            # If error during processing
            if signal_exceptions:
                logger.error(signal_exceptions)
                signal_exceptions = [(str(function), str(exception)) for function, exception in signal_exceptions]
                result = {'result': 'error', 'reason': 'processing_exception'}
                status = 500

                PostbackLog(remote_ip=request.META['REMOTE_ADDR'],
                        user_agent=request.META['HTTP_USER_AGENT'],
                        payment_status=cleaned_data['pmt_status'],
                        payment_amount=cleaned_data.get('pmt_amt', None),
                        transaction_id=transaction_id,
                        processed=False,
                        result=json.dumps({'response': result, 'exceptions': signal_exceptions}),
                        post=json.dumps(request.POST)).save()
            # Else successful processing
            else:
                result = {'result': 'success'}
                status = 200

                PostbackLog(remote_ip=request.META['REMOTE_ADDR'],
                        user_agent=request.META['HTTP_USER_AGENT'],
                        payment_status=cleaned_data['pmt_status'],
                        payment_amount=cleaned_data.get('pmt_amt', None),
                        transaction_id=transaction_id,
                        processed=True,
                        result=json.dumps({'response': result}),
                        post=json.dumps(request.POST)).save()

        # Else postback has errors
        else:
            logger.error(dict(form.errors))
            result = {'result': 'error', 'reason': 'form_invalid'}
            status = 400

            PostbackLog(remote_ip=request.META['REMOTE_ADDR'],
                    user_agent=request.META['HTTP_USER_AGENT'],
                    processed=False,
                    result=json.dumps({'response': result, 'form_errors': dict(form.errors)}),
                    post=json.dumps(request.POST)).save()

    # Else not a post request
    else:
        logger.error('method_not_allowed')
        result = {'result': 'error', 'reason': 'method_not_allowed'}
        status = 405

        PostbackLog(remote_ip=request.META['REMOTE_ADDR'],
                user_agent=request.META['HTTP_USER_AGENT'],
                processed=False,
                result=json.dumps({'response': result}),
                post=json.dumps(request.POST)).save()

    return HttpResponse(json.dumps(result), status=status)
