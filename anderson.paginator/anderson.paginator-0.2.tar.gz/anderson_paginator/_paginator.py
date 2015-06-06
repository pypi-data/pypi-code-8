'''
Created on 2014. 7. 9.

@author: a141890
'''
from django.core.paginator import Paginator

class AndersonPaginator(Paginator):
    def __init__(self, objects, current_page, per_page, page_range, *args, **kwargs):
        super(AndersonPaginator, self).__init__(objects, per_page, *args, **kwargs)
        self.current_page = current_page
        self.per_page = per_page
        self.range = page_range
        self.start_page = current_page - current_page % page_range + 1

    def page_range(self):
        return range(self.start_page,
                     min(self.start_page + self.range, self.num_pages + 1))

    def total_page(self):
        return self.count / self.per_page

    def has_previous(self):
        return self.start_page > self.range

    def previous(self):
        return max(self.start_page - self.range, 1)

    def has_next(self):
        return self.start_page / self.range < self.total_page() / self.range

    def next(self):
        return min(self.total_page(), self.start_page + self.range)