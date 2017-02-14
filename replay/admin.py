import re
import time

from django import forms
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils.html import format_html, format_html_join
from django.utils.safestring import mark_safe

from replay.models import Action, Validator, Scenario, Step

class ActionAdminForm(forms.ModelForm):
    class Meta:
        model = Action
        fields = []  # Required but ignored.
        widgets = {
            'name': forms.TextInput(attrs={'size': 80}),
            'path': forms.TextInput(attrs={'size': 80}),
        }

class ValidatorInline(admin.StackedInline):
    model = Validator
    extra = 10
    ordering = (
        'order',
        'id',
    )
    fields = (
        'order',
        'pattern',
    )

def create_scenario(modeladmin, request, queryset):
    scenario = Scenario(name='Scenario %s' % time.ctime())
    scenario.save()
    for action in queryset:
        step = Step(scenario=scenario, action=action)
        step.save()
    return redirect('admin:replay_scenario_change', scenario.id)

create_scenario.short_description = 'Create scenario from actions'

def create_validators(modeladmin, request, queryset):
    title_pattern = '<title>(.*?)</title>'

    for action in queryset:
        pattern = None

        if action.status_code.startswith('3'):
            pattern = action.content
        else:
            match = re.search(title_pattern, action.content)
            if match:
                title = match.group(1)
                pattern = re.escape(title)
                if action.name == '':
                    action.name = title
                    action.save()

        if pattern:
            Validator.objects.create(
                action=action,
                pattern=pattern,
            )

create_validators.short_description = 'Create validators automatically'

class ActionAdmin(admin.ModelAdmin):
    actions = [
        create_scenario,
        create_validators,
    ]
    fields = (
        'name',
        ('method', 'path'),
        'data',
        'status_code',
        'content',
    )
    form = ActionAdminForm
    inlines = (
        ValidatorInline,
    )
    list_display = (
        'id',
        'name',
        'method',
        'path',
        'status_code',
    )
    ordering = ('name', 'id')
    save_on_top = True
    search_fields = (
        'name',
        'method',
        'path',
        'status_code',
    )

admin.site.register(Action, ActionAdmin)

class ValidatorAdmin(admin.ModelAdmin):
    fields = (
        'action',
        'order',
        'pattern',
    )
    list_display = (
        'id',
        'action',
        'order',
        '__str__',
    )
    ordering = (
        'action',
        'order',
        'id',
    )
    save_on_top = True
    search_fields = (
        'action__name',
        'action__path',
        'pattern',
    )

admin.site.register(Validator, ValidatorAdmin)

class StepInline(admin.StackedInline):
    model = Step
    extra = 10
    ordering = (
        'order',
        'id',
    )
    fields = (
        'order',
        'action',
        'action_url',
        'action_method',
        'action_path',
        'action_data',
        'action_status_code',
        'action_validators',
    )

    def action_url(self, step):
        return format_html(
            '<a href="{}">{}</a>',
            reverse('admin:replay_action_change', args=(step.action.id,)),
            str(step.action),
        )

    def action_method(self, step):
        return step.action.method

    def action_path(self, step):
        return step.action.path

    def action_data(self, step):
        return step.action.data

    def action_status_code(self, step):
        return step.action.status_code

    def action_validators(self, step):
        validators = Validator.objects.filter(action=step.action)
        validators = validators.order_by('order', 'id')
        iterable = ((validator.pattern,) for validator in validators)
        return format_html_join(mark_safe('<br><br>'), '&bull; {}', iterable)

    readonly_fields = (
        'action_url',
        'action_method',
        'action_path',
        'action_data',
        'action_status_code',
        'action_validators',
    )

class ScenarioAdminForm(forms.ModelForm):
    class Meta:
        model = Scenario
        fields = []  # Required but ignored.
        widgets = {
            'name': forms.TextInput(attrs={'size': 80}),
        }

class ScenarioAdmin(admin.ModelAdmin):
    fields = (
        'name',
        'priority',
    )
    form = ScenarioAdminForm
    inlines = (
        StepInline,
    )
    list_display = (
        'name',
        'priority',
    )
    save_on_top = True
    search_fields = (
        'name',
    )

admin.site.register(Scenario, ScenarioAdmin)

class StepAdmin(admin.ModelAdmin):
    fields = (
        'scenario',
        'action',
        'order',
    )
    list_display = (
        'id',
        'scenario',
        'action',
    )
    ordering = (
        'scenario__name',
        'order',
        'id',
    )
    save_on_top = True
    search_fields = (
        'scenario__name',
        'action__name',
        'action__path',
    )

admin.site.register(Step, StepAdmin)
