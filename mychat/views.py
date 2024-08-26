# example/views.py
from datetime import datetime

from django.http import HttpResponse

def index(request):
    now = datetime.now()
    html = f'''
    <html>
        <body>
            <h1>Hello from Vercel!</h1>
            <h1>Hello from Vercel!</h1>
            <h1>Hello from Vercel!</h1>
            <h1>Hello from Vercel!</h1>
            <h1>Hello from Vercel!</h1>
            <p>The mychats time is { now }.</p>
        </body>
    </html>
    '''
    return HttpResponse(html)