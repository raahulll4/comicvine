from django.shortcuts import render, redirect
from . import services

def search(request):
    currently_reading = services.get_all_currently_reading(request)
    return render(request, 'comics/search.html', {'currently_reading': currently_reading})


def results(request):
    query = request.GET.get('q', '').strip()

    if not query:
        return render(request, 'comics/search.html', {'error': 'Please enter a search term'})

    volumes = services.search_volumes(query)
    return render(request, 'comics/results.html', {'volumes': volumes, 'query': query})


def timeline(request, volume_id):
    volume = services.get_volume(volume_id)

    if not volume:
        return render(request, 'comics/search.html', {'error': 'Volume not found'})

    issues = services.get_all_issues_for_volume(volume)
    read_issues = services.get_reading_progress(request, volume_id)

    return render(request, 'comics/timeline.html', {
        'volume': volume,
        'issues': issues,
        'read_issues': read_issues,
        'volume_id': volume_id,
    })


def toggle_issue(request, volume_id, issue_id):
    if request.method == 'POST':
        services.toggle_issue_read(request, volume_id, issue_id)
    return redirect('timeline', volume_id=volume_id)