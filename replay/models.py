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

class Action(models.Model):
    name = models.TextField(blank=True, default='')
    method = models.CharField(max_length=8, choices=HTTP_METHODS)
    path = models.TextField()
    data = models.TextField()
    files = models.TextField()
    status_code = models.CharField(max_length=3)
    content = models.TextField(blank=True)

    def __str__(self):
        fields = (self.id, self.method, self.path)
        return self.name or '<Action: %s %s %s>' % fields

class Validator(models.Model):
    action = models.ForeignKey(Action)
    order = models.FloatField(default=1.0)
    pattern = models.TextField()

    def __str__(self):
        return self.pattern[:78]

class Scenario(models.Model):
    name = models.TextField(unique=True)
    priority = models.FloatField(default=1.0)

    def __str__(self):
        return self.name

class Step(models.Model):
    scenario = models.ForeignKey(Scenario)
    order = models.FloatField(default=1.0)
    action = models.ForeignKey(Action)

    def __str__(self):
        return '<Step: %s>' % self.id
