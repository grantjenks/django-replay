import json

from replay.models import Action

def escape(text):
    "Escape text for string.Template substitution."
    return text.replace('$', '$$')


class RecorderMiddleware(object):
    def process_response(self, request, response):
        "Create Action object based on request and response."
        method = request.method
        data = json.dumps(getattr(request, method))
        files_names = {key: value.name for key, value in request.FILES.items()}
        files = json.dumps(files_names)
        status_code = response.status_code
        redirect = 300 <= status_code < 400
        content = response.content if not redirect else response.url

        try:
            content.decode('utf-8')
        except UnicodeDecodeError:
            content = ''

        Action.objects.create(
            method=method,
            path=escape(request.path),
            data=escape(data),
            files=escape(files),
            status_code=str(status_code),
            content=content,
        )

        return response
