# -*- coding: utf8 -*-
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.db.models.aggregates import Max, Min
import random

# 获取表中指定字段最大记录的值
def get_max_value(model,field_name):
    obj =  model.objects.aggregate(Max(field_name))
    if obj:
        vaule = obj['%s__max'% field_name]
    else:
        vaule = 1
    return vaule

# 获取表中指定字段最小记录的值
def get_min_value(model,field_name):
    obj =  model.objects.aggregate(Min(field_name))
    if obj:
        vaule = obj['%s__min'% field_name]
    else:
        vaule = 1
    return vaule



#根据id随机获取一条记录
def get_random_record(model,filter_dict={},id_field_name='id'):
#     max_id = get_max_value(model,id_field_name)
#     min_id = get_min_value(model,id_field_name)
#     random_id = random.randint(min_id,max_id)
#     filter_dict['%s__gte'%id_field_name] = random_id
#     print filter_dict
    id_list = model.objects.filter(**filter_dict).values_list(id_field_name,flat=True)
    if id_list:
        random_id = random.choice(id_list)
        filter_data = {id_field_name:random_id}
        records = model.objects.filter(**filter_data)
        if records:
            return records[0]
        
        
def one_page_records(records,page,max_num=500):
    paginator = Paginator(records, max_num)
    try:
        results = paginator.page(page)
    except (EmptyPage, InvalidPage):
        results = paginator.page(paginator.num_pages)  
    return results