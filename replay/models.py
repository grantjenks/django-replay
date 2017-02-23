"""Django Replay Models

* Remember to use dumpdata and loaddata!
* Do not make actions into templates/generics without great care! Some data
  like files may be deleted because they are stored outside the database.

"""

from django.db import models

HTTP_METHODS = (
    ('GET', 'GET'),
    ('POST', 'POST'),
)

class Scenario(models.Model):
    name = models.TextField(unique=True)
    priority = models.FloatField(
        default=1.0,
        help_text='Scenarios are run in ascending priority.',
    )

    def __str__(self):
        return self.name

class Action(models.Model):
    scenario = models.ForeignKey(Scenario, null=True, blank=True, default=None)
    order = models.FloatField(
        default=1.0,
        help_text='Actions are run in ascending order.',
    )
    name = models.TextField(blank=True, default='')
    method = models.CharField(max_length=8, choices=HTTP_METHODS)
    path = models.TextField()
    data = models.TextField(
        help_text='HTTP parameters in JSON format. Supports string templating.'
        ' Example: $name or $(name).',
    )
    files = models.TextField(
        help_text='Uploaded files in JSON format. Key and value pairs'
        ' correspond to filename and file-path pairs. Supports string'
        ' templating. Example: $name and $(name).',
    )
    status_code = models.CharField(max_length=3)
    content = models.TextField(blank=True)

    def __str__(self):
        fields = (self.id, self.method, self.path)
        value = self.name or '<Action: %s %s %s>' % fields
        return value[:68]

class Validator(models.Model):
    action = models.ForeignKey(Action, related_name='validators')
    order = models.FloatField(
        default=1.0,
        help_text='Validators are run in ascending order.',
    )
    pattern = models.TextField(
        help_text='Matched against HTTP response. Supports regular'
        ' expressions. Symbolic group names are stored and may be'
        ' used for string templating. Example: (?P&lt;name&gt;pattern)',
    )

    def __str__(self):
        return self.pattern[:68]
