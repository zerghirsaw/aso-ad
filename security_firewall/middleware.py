from django.core.cache import cache
from rest_framework.response import Response
from rest_framework import status
from functools import wraps
import os

BLOCK_PREFIX = "blackhole:"
DURATION = int(os.environ.get("THROTTLE_BLOCK_SECONDS", "3600"))

def check_threat_throttle(view_func):
    @wraps(view_func)
    # PERBAIKAN: Menambahkan 'self' untuk kompatibilitas class-based view
    def _wrapped_view(self, request, *args, **kwargs):
        ip = request.META.get('REMOTE_ADDR')
        
        if cache.get(f"{BLOCK_PREFIX}{ip}"):
            return Response({"error": "XDR Blackhole Active. Connection Dropped."}, status=status.HTTP_403_FORBIDDEN)
            
        return view_func(self, request, *args, **kwargs)
    return _wrapped_view

def trigger_blackhole(identifier):
    cache.set(f"{BLOCK_PREFIX}{identifier}", True, DURATION)
