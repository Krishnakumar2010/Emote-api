"""
Vercel Serverless Function Entry Point
For deploying Free Fire Emote API to Vercel
"""

# Import the main application
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from index import app

# Vercel serverless function handler
def handler(request):
    """Main handler for Vercel serverless functions"""
    return app(request.environ, lambda status, headers: None)

# Export for Vercel
app_handler = app
