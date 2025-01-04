import re


def index(environ, start_response):
    """This function will be mounted on "/" and display a link
    to the hello world page."""
    start_response('200 OK', [('Content-Type', 'text/html')])
    return ['''
        This is Index page
''']


def hello(environ, start_response):
    """Like the example above, but it uses the name specified in the
URL."""
    # get the name from the url if it was specified there.
    args = environ.get('myapp.url_args')
    if args:
        subject = re.escape(args[0])
    else:
        subject = 'World'
    start_response('200 OK', [('Content-Type', 'text/html')])
    return ['''Hello %(subject)s
            Hello %(subject)s!

''' % {'subject': subject}]


def not_found(environ, start_response):
    """Called if no URL matches."""
    start_response('404 NOT FOUND', [('Content-Type', 'text/plain')])
    return ['Not Found']


# map urls to functions
urls = [
    (r'^$', index),
    (r'^hello/?$', hello),
    (r'hello/(.+)$', hello),
]


def application(start_response, environ):
    """
    The main WSGI application. Dispatch the current request to
    the functions from above and store the regular expression
    captures in the WSGI environment as  `myapp.url_args` so that
    the functions from above can access the url placeholders.

    If nothing matches call the `not_found` function.
    """

    path = environ['PATH_INFO'].strip('/')
    for url_pattern, view in urls:
        match = re.search(url_pattern, path)
        if match is not None:
            environ['myapp.url_args'] = match.groups()
            return view(environ, start_response)

    return not_found(environ, start_response)
