import re
import time

from django import forms
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.shortcuts import redirect
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe

from replay.models import Action, Validator, Scenario

class ActionAdminForm(forms.ModelForm):
    class Meta:
        model = Action
        fields = []  # Required but ignored.
        widgets = {
            'name': forms.TextInput(attrs={'size': 50}),
            'path': forms.TextInput(attrs={'size': 50}),
            'data': forms.Textarea(attrs={'rows': 4, 'cols': 80}),
            'files': forms.Textarea(attrs={'rows': 2, 'cols': 80}),
            'content': forms.Textarea(attrs={'rows': 8, 'cols': 80}),
        }

class ValidatorInline(admin.StackedInline):
    model = Validator
    extra = 8
    ordering = (
        'order',
        'id',
    )
    fields = (
        'order',
        'pattern',
    )

class ActionAdmin(admin.ModelAdmin):
    def create_scenario(self, request, queryset):
        scenario = Scenario(name='Scenario %s' % time.ctime())
        scenario.save()
        for action in queryset:
            action.scenario = scenario
            action.save()
        return redirect('admin:replay_scenario_change', scenario.id)

    create_scenario.short_description = 'Create scenario from actions'

    def create_validators(self, request, queryset):
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

    def get_queryset(self, request):
        queryset = super(ActionAdmin, self).get_queryset(request)
        queryset = queryset.annotate(count_validators=Count('validators__id'))
        return queryset

    def scenario_link(self, action):
        scenario = action.scenario
        url = reverse('admin:replay_scenario_change', args=(scenario.id,))
        return mark_safe('<a href="%s">%s</a>' % (url, scenario))

    scenario_link.short_description = 'Scenario Link'
    scenario_link.allow_tags = True

    def validators_count(self, instance):
        return instance.count_validators

    validators_count.admin_order_field = 'count_validators'
    validators_count.short_description = 'Validators'

    actions = (
        'create_scenario',
        'create_validators',
    )
    fields = (
        ('scenario', 'scenario_link', 'order'),
        'name',
        ('method', 'path'),
        'data',
        'files',
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
        'scenario',
        'order',
        'method',
        'path',
        'status_code',
        'validators_count',
    )
    ordering = (
        '-scenario',
        'order',
        'id',
    )
    readonly_fields = (
        'scenario_link',
    )
    save_on_top = True
    search_fields = (
        'name',
        'method',
        'path',
        'status_code',
    )

admin.site.register(Action, ActionAdmin)

class ValidatorAdmin(admin.ModelAdmin):
    def action_link(self, validator):
        action = validator.action
        url = reverse('admin:replay_action_change', args=(action.id,))
        return mark_safe('<a href="%s">%s</a>' % (url, action))

    fields = (
        'action',
        'action_link',
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
        '-action',
        'order',
        'id',
    )
    readonly_fields = (
        'action_link',
    )
    save_on_top = True
    search_fields = (
        'action__name',
        'action__path',
        'pattern',
    )

admin.site.register(Validator, ValidatorAdmin)

class ActionInline(admin.StackedInline):
    def action_link(self, action):
        url = reverse('admin:replay_action_change', args=(action.id,))
        return mark_safe('<a href="%s">%s</a>' % (url, action))

    def validators(self, action):
        validators = Validator.objects.filter(action=action)
        validators = validators.order_by('order', 'id')
        iterable = ((validator.pattern,) for validator in validators)
        return format_html_join(mark_safe('<br><br>'), '&bull; {}', iterable)

    model = Action
    extra = 8
    ordering = (
        'order',
        'id',
    )
    fields = (
        'action_link',
        'order',
        'name',
        ('method', 'path'),
        'data',
        'files',
        'status_code',
        'content',
        'validators',
    )
    form = ActionAdminForm
    readonly_fields = (
        'action_link',
        'validators',
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
        ActionInline,
    )
    list_display = (
        'id',
        'name',
        'priority',
    )
    ordering = (
        '-id',
    )
    save_on_top = True
    search_fields = (
        'name',
    )

admin.site.register(Scenario, ScenarioAdmin)
