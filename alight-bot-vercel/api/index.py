import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot import webhook
import json

async def handler(request):
    """Vercel panggil ini"""
    return await webhook(request)

# Buat export biar Vercel bisa panggil
handler.__name__ = "handler"
