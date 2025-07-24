from django.shortcuts import render, redirect

# Create your views here.
from .models import SurveyEntry
from django.db.models import Sum

DROPDOWNS = [
    'Trenching S1 Normal soil (1.2m)', 'Trenching S2 Hard soil (1m)',
    'Trenching S3 Soft Rock (0.5m)', 'Trenching S4 Hard Rock (0.5m)',
    'T/boring [Soil Road, Entrance] (PVC/HDPE)',
    'T/boring [Asp Road, F.S] (GI Pipe)',
    'Alphalt Cutting', 'Bridge/Culvert (PVC/HDPE)',
    'Bridge/Culvert (GI Pipe)', 'Swampy Area',
    'Erosion Area', 'Railway Crossing'
]

user_session = {}

def landing_page(request):
    return render(request, 'landing.html')

def index(request):
    if request.method == 'POST':
        state = request.POST.get('state')
        segment_id = request.POST.get('segment_id')
        route_id = request.POST.get('route_id')
        
        if not request.session.session_key:
            request.session.save()
            
        user_session[request.session.session_key] = {
            'state': state, 
            'segment_id': segment_id, 
            'route_id': route_id
        }
        return redirect('input_form')
    return render(request, 'index.html')

def input_form(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        value = float(request.POST.get('value'))
        sess = user_session.get(request.session.session_key, {})
        
        SurveyEntry.objects.create(
            state=sess.get('state', ''),
            segment_id=sess.get('segment_id', ''),
            route_id=sess.get('route_id', ''),
            category=category,
            value=value
        )
    
    values = SurveyEntry.objects.filter(
        segment_id=user_session.get(request.session.session_key, {}).get('segment_id', '')
    )
    return render(request, 'input_form.html', {
        'dropdowns': DROPDOWNS, 
        'values': values
    })

def summary(request):
    sess = user_session.get(request.session.session_key, {})
    entries = SurveyEntry.objects.filter(segment_id=sess.get('segment_id', ''))
    totals = entries.values('category').annotate(total=Sum('value'))
    return render(request, 'summary.html', {'totals': totals})