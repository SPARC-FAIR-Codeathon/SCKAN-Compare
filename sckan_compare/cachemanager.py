import time
import diskcache


class CacheManager:
    def __init__(self, cache_directory, max_cache_days):
        self.cache = self.create_disk_cache(cache_directory)
        self.max_cache_days = max_cache_days

    def create_disk_cache(self, directory):
        cache = diskcache.Cache(directory)
        return cache

    def get_cached_data(self, key):
        return self.cache.get(key)

    def cache_data(self, key, data):
        self.cache.set(key, (time.time(), data))

    def invalidate_old_cache_entries(self):
        now = time.time()
        for key in list(self.cache):
            cached_time, _ = self.cache.get(key)
            if (now - cached_time) > (self.max_cache_days * 86400):
                self.cache.pop(key)
