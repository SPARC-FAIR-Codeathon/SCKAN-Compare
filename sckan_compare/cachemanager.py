"""
API output cache manager for SckanCompare package.

License: Apache License 2.0
"""

import time
import diskcache


class CacheManager(object):
    """
    A class for managing a disk-based cache with expiration for cached data.

    Parameters
    ----------
    cache_directory : str
        Path to the directory for storing cache data.
    max_cache_days : int
        Maximum number of days a cached entry is considered valid.

    Attributes
    ----------
    cache : diskcache.Cache
        Disk cache object for storing data.
    max_cache_days : int
        Maximum number of days a cached entry is considered valid.

    Methods
    -------
    __init__(cache_directory, max_cache_days):
        Initialize the CacheManager class.
    create_disk_cache(directory):
        Create a disk cache object.
    get_cached_data(key):
        Retrieve cached data associated with a given key.
    cache_data(key, data):
        Cache data with an associated key.
    invalidate_old_cache_entries():
        Remove cached entries that have expired.
    """

    def __init__(self, cache_directory, max_cache_days):
        """
        Initialize CacheManager object.

        Parameters
        ----------
        cache_directory : str
            The directory path where the cache will be stored.
        max_cache_days : int
            Maximum number of days to keep cached data.
        """
        self.cache = self.create_disk_cache(cache_directory)
        self.max_cache_days = max_cache_days

    def create_disk_cache(self, directory):
        """
        Create a disk cache instance.

        Parameters
        ----------
        directory : str
            The directory path where the cache will be stored.

        Returns
        -------
        diskcache.Cache
            The disk cache instance.
        """
        cache = diskcache.Cache(directory)
        return cache

    def get_cached_data(self, key):
        """
        Get cached data using a specified key.

        Parameters
        ----------
        key : str
            The cache key.

        Returns
        -------
        tuple or None
            A tuple containing cached timestamp and data, or None if not found.
        """
        return self.cache.get(key)

    def cache_data(self, key, data):
        """
        Cache data using a specified key.

        Parameters
        ----------
        key : str
            The cache key.
        data : any
            The data to be cached.
        """
        self.cache.set(key, (time.time(), data))

    def invalidate_old_cache_entries(self):
        """
        Invalidate old cache entries based on the maximum cache days.
        """
        now = time.time()
        for key in list(self.cache):
            cached_time, _ = self.cache.get(key)
            if (now - cached_time) > (self.max_cache_days * 86400):
                self.cache.pop(key)
