from django.utils.deprecation import MiddlewareMixin


class TrailingSlashMiddleware(MiddlewareMixin):
    """
    Middleware that adds a trailing slash to the request path internally,
    without performing a redirect.
    """

    def process_request(self, request):
        if not request.path.endswith("/"):
            request.path_info = request.path + "/"
