import json

from replay.models import Action


def escape(text):
    """Escape text for string.Template substitution."""
    return text.replace('$', '$$')


class RecorderMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """Create Action object based on request and response."""
        json_dump_kwargs = {'indent': 4, 'separators': (',', ': ')}
        method = request.method
        data = json.dumps(getattr(request, method), **json_dump_kwargs)
        files_names = {key: value.name for key, value in request.FILES.items()}
        files = json.dumps(files_names, **json_dump_kwargs)
        response = self.get_response(request)
        status_code = response.status_code
        redirect = 300 <= status_code < 400
        response_content = response.content
        try:
            response_content.decode('utf-8')
        except UnicodeDecodeError:
            response_content = ''
        content = response_content if not redirect else response.url
        Action.objects.create(
            method=method,
            path=escape(request.path),
            data=escape(data),
            files=escape(files),
            status_code=str(status_code),
            content=content,
        )
        return response
