import json

from replay.models import Action
from django.conf import settings
from django.http import StreamingHttpResponse

MAX_CONTENT_SIZE = 1024 * 1024  # 1M

def escape(text):
    "Escape text for string.Template substitution."
    return text.replace('$', '$$')


class RecorderMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        self.max_content_size = getattr(settings, "REPLAY_MAX_SIZE", MAX_CONTENT_SIZE)

    def __call__(self, request):
        "Create Action object based on request and response."
        kwargs = {'indent': 4, 'separators': (',', ': ')}
        reqDataAttr = "POST" if method == "POST" else "GET"
        data = json.dumps(getattr(request, reqDataAttr), **kwargs)
        files_names = {key: value.name for key, value in request.FILES.items()}
        files = json.dumps(files_names, **kwargs)
        response = self.get_response(request)
        status_code = response.status_code
        redirect = 300 <= status_code < 400
        if not isinstance(response, StreamingHttpResponse):
            response_content = response.content[:self.max_content_size]
            try:
                response_content.decode('utf-8')
            except UnicodeDecodeError:
                response_content = ''
            content = response_content if not redirect else response.url
        else:
            content = "--STREAMED--"

        Action.objects.create(
            method=method,
            path=escape(request.path),
            data=escape(data),
            files=escape(files),
            status_code=str(status_code),
            content=content,
        )

        return response
