# RedditAuth

If it wasn't clear from the name, RedditAuth is a Django application for Reddit OAuth2 authentication. It includes a custom Authentication system, complete with - 
 - Custom User model `RedditUser`
 - Custom Authentication Backend `RedditBackend`

Detailed documentation is in the "docs" directory.

## Quick start

1. Add "redditauth" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'redditauth',
    ]

2. Include the polls URLconf in your project urls.py like this::
```python
url(r'^redditauth/', include('redditauth.urls')),
```

3. Run `python manage.py migrate` to create the polls models.

4. Start the development server and visit http://127.0.0.1:8000/redditauth/
   to see the app in action.
