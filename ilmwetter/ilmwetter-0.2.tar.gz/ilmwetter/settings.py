# -*- coding: utf-8 -*-
BOT_NAME = 'ilmwetter'

SPIDER_MODULES = ['ilmwetter.spiders']
NEWSPIDER_MODULE = 'ilmwetter.spiders'
METAREFRESH_ENABLED = False
DEFAULT_ITEM_CLASS = 'ilmwetter.items.IlmwetterItem'

ITEM_PIPELINES = {
    'ilmwetter.pipelines.IlmwetterPipeline': 100
}
