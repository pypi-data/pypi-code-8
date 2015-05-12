# -*- coding: utf-8 -*-

from django import forms


class BaseKnob(forms.widgets.NumberInput):
    #
    # Creates a widget out of jQuery-Knob:
    # https://github.com/aterrien/jQuery-Knob/
    #
    class Media:
        js = (
            'js/pinogy_common/jquery.knob.js',
            'js/pinogy_common/knob.js',
        )

    def render(self, name, value, attrs=None):
        attrs = {
            "class": "knob",
            "data-fgColor": "#029eee",
            "data-displayPrevious": "true",
        }
        return super(BaseKnob, self).render(name, value, attrs)


class PercentageKnob(BaseKnob):
    def _format_value(self, value):
        """
        Overrides the super method to avoid localization (JS will barf!).
        """
        if value is None or value is "":
            return ""
        return str(value)

    def render(self, name, value, attrs=None):
        attrs = {
            "data-min": "0",
            "data-max": "100",
        }
        return super(PercentageKnob, self).render(name, value, attrs)
