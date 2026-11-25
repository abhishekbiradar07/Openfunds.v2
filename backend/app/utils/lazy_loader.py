"""Lazy loader for ML models to optimize memory and startup time on free hosting"""


class LazyLoader:
    """Lazy load resources only when needed"""
    
    def __init__(self, loader_func):
        self.loader_func = loader_func
        self._resource = None
    
    def __call__(self, *args, **kwargs):
        if self._resource is None:
            self._resource = self.loader_func(*args, **kwargs)
        return self._resource
    
    def reset(self):
        """Reset the loaded resource"""
        self._resource = None
