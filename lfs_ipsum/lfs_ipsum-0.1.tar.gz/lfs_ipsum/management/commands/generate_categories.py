# django imports
from django.core.management.base import BaseCommand
from lfs.catalog.models import Category


class Command(BaseCommand):
    args = ''
    help = 'Generates categories for LFS'

    def handle(self, *args, **options):
        for i in range(0, 10):
            c = Category(name="Category %s" % i, slug="category-%s" % i)
            c.save()
            for j in range(0, 3):
                sc = Category(name="Category %s%s" % (i, j), slug="category-%s-%s" % (i, j), parent=c)
                sc.save()
                for k in range(0, 3):
                    ssc = Category(name="Category %s%s%s" % (i, j, k), slug="category-%s-%s-%s" % (i, j, k), parent=sc)
                    ssc.save()
