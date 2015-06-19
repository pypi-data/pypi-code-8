# -*- coding: utf-8 -*-


from ip2location.Provider.taobao import TaoBaoProvider

def get_location(ip):
    ret = []
    providers = [
        TaoBaoProvider,
    ]
    for each_provider in providers:
        ret.append(
            each_provider().query(ip)
        )
    return ret
