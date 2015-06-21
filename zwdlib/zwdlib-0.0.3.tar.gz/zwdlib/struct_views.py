# -*- coding: utf8 -*-
from django.core.paginator import Paginator, InvalidPage, EmptyPage


# 普通分页显示
def normal_paging(target_list, page, num=30):
    paginator = Paginator(target_list, num) 
    total_page = paginator.num_pages
    
    # If page request (9999) is out of range, deliver last page of results.
    try:
        current_data = paginator.page(page)
    except (EmptyPage, InvalidPage):
        current_data = paginator.page(total_page)
    return current_data
