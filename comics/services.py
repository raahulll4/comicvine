import requests
from django.conf import settings

BASE_URL = 'https://comicvine.gamespot.com/api'

def get_headers():
    return {
        'User-Agent': 'Mozilla/5.0'
    }


def get_base_params():
    return {
        'api_key': settings.COMIC_VINE_API_KEY,
        'format': 'json',
    }


def search_volumes(query):
    params = get_base_params()
    params.update({
        'query': query,
        'resources': 'volume',
        'field_list': 'id,name,deck,image,count_of_issues,publisher,start_year',
        'limit': 10,
    })

    response = requests.get(
        f'{BASE_URL}/search/',
        params=params,
        headers=get_headers()
    )
    data = response.json()
    return data.get('results', [])


def get_volume(volume_id):
    params = get_base_params()
    params.update({
        'field_list': 'id,name,deck,image,issues,count_of_issues,publisher,start_year',
    })

    response = requests.get(
        f'{BASE_URL}/volume/4050-{volume_id}/',
        params=params,
        headers=get_headers()
    )
    data = response.json()
    return data.get('results', {})


def get_issue(issue_id):
    params = get_base_params()
    params.update({
        'field_list': 'id,name,issue_number,cover_date,store_date,image,story_arc_credits,site_detail_url',
    })

    response = requests.get(
        f'{BASE_URL}/issue/4000-{issue_id}/',
        params=params,
        headers=get_headers()
    )
    data = response.json()
    return data.get('results', {})


def get_all_issues_for_volume(volume):
    issue_refs = volume.get('issues', [])
    issues = []

    for ref in issue_refs:
        issue = get_issue(ref['id'])
        if issue:
            issues.append(issue)

    issues.sort(key=lambda x: x.get('cover_date') or '9999-99')
    return issues

def get_reading_progress(request, volume_id):
    reading = request.session.get('reading', {})
    return reading.get(str(volume_id), [])


def toggle_issue_read(request, volume_id, issue_id):
    reading = request.session.get('reading', {})
    volume_key = str(volume_id)
    issue_key = str(issue_id)

    if volume_key not in reading:
        reading[volume_key] = []

    if issue_key in reading[volume_key]:
        reading[volume_key].remove(issue_key)
    else:
        reading[volume_key].append(issue_key)

    request.session['reading'] = reading
    request.session.modified = True


def get_all_currently_reading(request):
    reading = request.session.get('reading', {})
    currently_reading = []

    for volume_id, read_issues in reading.items():
        if read_issues:
            volume = get_volume(volume_id)
            if volume:
                total = volume.get('count_of_issues', 0)
                currently_reading.append({
                    'volume': volume,
                    'read_count': len(read_issues),
                    'total': total,
                })

    return currently_reading