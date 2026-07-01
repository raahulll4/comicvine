# Comic-Vine

A Django web app for browsing and tracking your comic book reading progress using the Comic Vine API. Search for any comic volume, view its issues in a timeline, and track what you've read - with quick links to find issues on GetComics.

## Features

- Search for comic volumes via the Comic Vine API
- View all issues for a volume in a timeline layout
- Mark issues as read and track progress across volumes
- Modal issue view with cover art, story arc info, and external links
- Tie-in issue detection
- Links to GetComics for both volumes and individual issues

## Setup

1. Clone the repo:
```bash
   git clone https://github.com/raahulll4/comicarc.git
   cd comicarc
```

2. Install dependencies:
```bash
   pip install -r requirements.txt
```

3. Create a `.env` file in the project root:

```
COMIC_VINE_API_KEY=your_key_here
```

4. Run migrations:
```bash
   python manage.py migrate
```

5. Start the server:
```bash
   python manage.py runserver
```

6. Visit `http://127.0.0.1:8000`
