from __future__ import absolute_import
from agms.response.response import Response
from agms.util.parser import Parser
from agms.exception.invalid_request_exception import InvalidRequestException


class ReportResponse(Response):
    """
    A class representing AGMS Report Response objects.
    """

    def __init__(self, response, op):
        self._response = None
        self._op = op
        
        response = response['soap:Envelope']['soap:Body'][op + 'Response'][op + 'Result']
        response = Parser(response).parse()

        if self._op == 'TransactionAPI':
            self._mapping = {
                'id': 'id',
                'transactionid': 'transaction_id',
                'transactiontype': 'transaction_type',
                'paymenttype': 'payment_type',
                'amount': 'amount',
                'orderdescription': 'order_description',
                'orderid': 'order_id',
                'ponumber': 'po_number',
                'tax': 'tax_amount',
                'shipping': 'shipping_amount',
                'tipamount': 'tip_amount',
                'ccnumber': 'cc_number',
                'ccexpdate': 'cc_exp_date',
                'checkname': 'ach_name',
                'checkaba': 'ach_routing_number',
                'checkaccount': 'ach_account_number',
                'accountholdertype': 'ach_business_or_personal',
                'accounttype': 'ach_checking_or_savings',
                'seccode': 'ach_sec_code',
                'safeaction': 'safe_action',
                'responsesafeid': 'safe_id',
                'clerkid': 'clerk_id',
                'firstname': 'first_name',
                'lastname': 'last_name',
                'company': 'company_name',
                'address1': 'address',
                'address2': 'address_2',
                'city': 'city',
                'state': 'state',
                'zip': 'zip',
                'country': 'country',
                'phone': 'phone',
                'fax': 'fax',
                'email': 'email',
                'website': 'website',
                'shippingfirstname': 'shipping_first_name',
                'shippinglastname': 'shipping_last_name',
                'shippingcompany': 'shipping_company_name',
                'shippingaddress1': 'shipping_address',
                'shippingaddress2': 'shipping_address_2',
                'shippingcity': 'shipping_city',
                'shippingstate': 'shipping_state',
                'shippingzip': 'shipping_zip',
                'shippingcountry': 'shipping_country',
                'shippingemail': 'shipping_email',
                'shippingphone': 'shipping_phone',
                'shippingfax': 'shipping_fax',
                'shippingcarrier': 'shipping_carrier',
                'trackingnumber': 'shipping_tracking',
                'ipaddress': 'ip_address',
                'customfield1': 'custom_field_1',
                'customfield2': 'custom_field_2',
                'customfield3': 'custom_field_3',
                'customfield4': 'custom_field_4',
                'customfield5': 'custom_field_5',
                'customfield6': 'custom_field_6',
                'customfield7': 'custom_field_7',
                'customfield8': 'custom_field_8',
                'customfield9': 'custom_field_9',
                'customfield10': 'custom_field_10',
                'cardpresent': 'card_present',
                'cardtype': 'card_type',
                'receipttype': 'receipt_type',
                'responsestatuscode': 'response_code',
                'responsestatusmsg': 'response_message',
                'responsetransid': 'response_transaction_id',
                'responseauthcode': 'authorization_code',
                'transactiondate': 'transaction_date',
                'createdate': 'date_created',
                'moddate': 'date_last_modified',
                'createuser': 'created_by',
                'moduser': 'modified_by',
                'useragent': 'user_agent',
            }
            
            arr = response['transactions']['transaction']
            if arr:
                self._response = arr
            else:
                self._response = {}
        elif self._op == 'QuerySAFE':
            self._mapping = {
                'ID': 'id',
                'MerchantID': 'merchant_id',
                'CustomerID': 'customer_id',
                'TransactionID': 'transaction_id',
                'TransactionType': 'transaction_type',
                'PaymentType': 'payment_type',
                'Amount': 'amount',
                'OrderDescription': 'order_description',
                'OrderID': 'order_id',
                'PONumber': 'po_number',
                'Tax': 'tax_amount',
                'Shipping': 'shipping_amount',
                'TipAmount': 'tip_amount',
                'CCNumber': 'cc_number',
                'CCExpDate': 'cc_exp_date',
                'CheckName': 'ach_name',
                'CheckABA': 'ach_routing_number',
                'CheckAccount': 'ach_account_number',
                'AccountHolderType': 'ach_business_or_personal',
                'AccountType': 'ach_checking_or_savings',
                'SecCode': 'ach_sec_code',
                'SAFEAction': 'safe_action',
                'ResponseSafeID': 'safe_id',
                'ClerkID': 'clerk_id',
                'FirstName': 'first_name',
                'LastName': 'last_name',
                'Company': 'company',
                'Address1': 'address',
                'Address2': 'address_2',
                'City': 'city',
                'State': 'state',
                'Country': 'country',
                'Zip': 'zip',
                'Phone': 'phone',
                'Fax': 'fax',
                'Email': 'email',
                'Website': 'web_site',
                'Shipping': 'shipping',
                'ShippingFirstName': 'shipping_first_name',
                'ShippingLastName': 'shipping_last_name',
                'ShippingCompany': 'shipping_company_name',
                'ShippingAddress1': 'shipping_address',
                'ShippingAddress2': 'shipping_address_2',
                'ShippingCity': 'shipping_city',
                'ShippingState': 'shipping_state',
                'ShippingZip': 'shipping_zip',
                'ShippingCountry': 'shipping_country',
                'ShippingEmail': 'shipping_email',
                'ShippingPhone': 'shipping_phone',
                'ShippingFax': 'shipping_fax',
                'ShippingCarrier': 'shipping_carrier',
                'TrackingNumber': 'shipping_tracking',
                'IPAddress': 'ip_address',
                'CustomField1': 'custom_field_1',
                'CustomField2': 'custom_field_2',
                'CustomField3': 'custom_field_3',
                'CustomField4': 'custom_field_4',
                'CustomField5': 'custom_field_5',
                'CustomField6': 'custom_field_6',
                'CustomField7': 'custom_field_7',
                'CustomField8': 'custom_field_8',
                'CustomField9': 'custom_field_9',
                'CustomField10': 'custom_field_10',
                'CardPresent': 'card_present',
                'CardType': 'card_type',
                'ReceiptType': 'receipt_type',
                'ResponseStatusCode': 'response_code',
                'ResponseStatusMsg': 'response_message',
                'ResponseTransID': 'response_transaction_id',
                'ResponseAuthCode': 'authorization_code',
                'TransactionDate': 'transaction_date',
                'Active': 'active',
                'Type': 'type',
                'Internal': 'internal',
                'CreateDate': 'date_created',
                'ModDate': 'date_last_modified',
                'CreateUser': 'created_by',
                'ModUser': 'modified_by',
                'UserAgent': 'user_agent',
            }
            arr = response['saferecords']['saferecord']
            if arr:
                self._response = arr
            else:
                self._response = {}

        else:
            raise InvalidRequestException('Invalid op in Response.')

    def to_array(self):
        # Override toArray method to handle array response
        response = []
        if self._response:
            for result in self._response:
                response.append(self._map_response(result))
        return response
