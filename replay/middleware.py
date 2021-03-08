import json

from replay.models import Action
from django.conf import settings
from django.http import StreamingHttpResponse

MAX_CONTENT_SIZE = 1024 * 1024  # 1M

def escape(text):
    "Escape text for string.Template substitution."
    return text.replace('$', '$$')


class RecorderMiddleware(object):
    """Record request passing through the middleware

    settings.REPLAY_MAX_SIZE configure how much of the response content is stored

    settings.REPLAY_ACTION_FILTER is a function receiving an action
    and returning True if it must be saved, False if it should be skipped.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.max_content_size = getattr(settings, "REPLAY_MAX_SIZE", MAX_CONTENT_SIZE)
        self.action_filter = getattr(settings, "REPLAY_ACTION_FILTER", lambda action: True)

    def __call__(self, request):
        "Create Action object based on request and response."
        kwargs = {'indent': 4, 'separators': (',', ': ')}
        method = request.method
        reqParams = request.POST if method == "POST" else request.GET
        data = json.dumps(reqParams, **kwargs)
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
            content = "--STREAMED--"  # we do not register streamed content for now

        action = Action(
            method=method,
            path=escape(request.path),
            data=escape(data),
            files=escape(files),
            status_code=str(status_code),
            content=content,
        )

        if self.action_filter(action):
            action.save()

        return response
