# -*- coding: utf-8 -*-
MIN_SUMM = 10 # минимальная сумма заказа, влияющая на ссылку продолжения заказа в корзине
EMAIL_REPLY = 'noreply@pressa.ru' # отправитель уведомлений
######DEV MODE##################
API_CREATE_USER = 'http://localhost:8008/api/create/user' # create user on the site-integrator
API_BILLING_PAGE = 'http://localhost:8008/api/billing?sum={{sum}}&ms_order_id={{ms_order_id}}' # redirect to the site-integrator's billing page
API_SUCCESS_PAYMENT = 'http://localhost:8008/api/success/payment' # request from site-integrator about successfull payment

######PROD MODE##################
#API_CREATE_USER = 'http://pressa.ru/mapshopapi/create/user' # create user on the site-integrator
#API_BILLING_PAGE = 'http://pressa.ru/ru/billing/payment?sum={{sum}}&ms_order_id={{ms_order_id}}' # redirect to the site-integrator's billing page
#API_SUCCESS_PAYMENT = 'http://pressa.ru/mapshopapi/success/payment' # request from site-integrator about successfull payment
