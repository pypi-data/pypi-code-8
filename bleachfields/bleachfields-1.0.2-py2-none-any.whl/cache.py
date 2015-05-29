from repoze.lru import CacheMaker

cache_maker = CacheMaker()


def lru_cache(maxsize, timeout=None):
  if timeout is None:
    return cache_maker.lrucache(maxsize=maxsize)
  return cache_maker.expiring_lrucache(maxsize=maxsize, timeout=timeout)
