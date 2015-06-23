# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
import mapshop.views as views


from django.conf.urls import patterns, url

urlpatterns = patterns( '',
    url(r'^product/list/all.html$', 'mapshop.views.product_list', name="catalog_all"),
    url(r'^product/list/(?P<slug>[^\.]+).html$', 'mapshop.views.product_list', name="catalog_filter"),
    url(r'^product/detail/(?P<slug>[^\.]+).html$', 'mapshop.views.product_detail', name="product_detail"),
    url(r'^kiosk/list/(?P<order_id>[^\.]+).html$', 'mapshop.views.kiosk_list', name="kiosk_all"),
    url(r'^finish/order/(?P<order_id>[^\.]+)$', 'mapshop.views.finish_order', name="finish_order"),
    url(r'^thanks/$', 'mapshop.views.thanks'),
    

    ##################AJAX REQUESTS############################
    url(r'^add/to/cart/$', 'mapshop.ajax.add_product_to_cart'),
    url(r'^del/from/cart$', 'mapshop.ajax.del_product_from_cart'),
    url(r'^getinfo/kiosk$', 'mapshop.ajax.getinfo_kiosk'),
    url(r'^preorder/save$', 'mapshop.ajax.preorder_save'),
    url(r'^cart/show$', 'mapshop.ajax.cart_show'),


    ##################API REQUESTS############################
    url(r'^api/product/edit$', 'mapshop.api.product_edit'),
    url(r'^api/product/bye$', 'mapshop.api.product_bye'),


)

