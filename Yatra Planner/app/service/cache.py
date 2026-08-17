from datetime import datetime, timedelta

_cache = {}

def get_cache(key: str):

    if key not in _cache:
        return None

    cached_item = _cache[key]

    if datetime.now() - cached_item['timestamp'] > timedelta(
        seconds=cached_item['ttl']
    ):

        del _cache[key]
        return None
    return cached_item['data']


def set_cache(key: str, data, ttl: int):

    _cache[key] = {
        'data': data,
        'timestamp': datetime.now(),
        'ttl': ttl
    }


def clear_cache():
    _cache.clear()

def get_cache_stats():

    return {
        "total_entries": len(_cache),
        "keys": list(_cache.keys())
    }