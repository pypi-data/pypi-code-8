from django import forms


class LogicCheck(object):
    """ Checks various conditions between field values and optional fields. """
    def __init__(self, model):
        self.conditional_field_value = None
        self.condition_value = None
        self.optional_field_value = None
        self.optional_field_verbose_name = None
        self.model = model

    def test(self, cleaned_data, conditional_field, condition_value, optional_field,
             logic=None, required_optional_field_value=None):

        """Tests condition and raises a forms validation error on failure.

            Args:
                logic: label to indicate how to handle the field and values
                    * required_if_value (default): if conditional_field == condition_value ? required : not required
                    * not_required_if_value: if conditional_field == condition_value ? not required : required
                    * if_condition_then:
                    * if_condition_then_not:

        """
        logic = logic or 'required_if_value'
        self.optional_field = optional_field
        self.conditional_field_value = cleaned_data.get(conditional_field, None)
        self.conditional_field_value = self.conditional_field_value.lower()
        self.condition_value = self.condition_value.lower()
        self.optional_field_value = self.cleaned_data.get(optional_field, None)
        self.optional_field_value = self.optional_field_value.lower()
        self.required_optional_field_value = required_optional_field_value
        for field in self.model._meta.fields:
            if field.name == self.optional_field:
                self.optional_field_verbose_name = field.verbose_name
                break
        if logic == 'required_if_value':
            self.required_if_value()
        elif logic == 'not_required_if_value':
            self.not_required_if_value()
        elif logic == 'if_condition_then':
            self.if_condition_then()
        elif logic == 'if_condition_then_not':
            self.if_condition_then_not()

    def required_if_value(self):
        # default option
        # if conditional_field == condition_value ? required : not required
        if self.conditional_field_value:
            if self.conditional_field_value == self.condition_value and not self.optional_field_value:
                raise forms.ValidationError(
                    'Please provide an answer for \'{}\'...'.format(self.optional_field_verbose_name,))
            if not self.conditional_field_value == self.condition_value and self.optional_field_value:
                raise forms.ValidationError(
                    '{} is not required if {} is {}. Please correct'.format(
                        self.optional_field, self.conditional_field, self.condition_value,))

    def not_required_if_value(self):
        # if conditional_field == condition_value ? not required : required
        if self.conditional_field_value:
            if self.conditional_field_value == self.condition_value and self.optional_field_value:
                raise forms.ValidationError(
                    '{} is not required if {} is {}. Please correct'.format(
                        self.optional_field, self.conditional_field, self.condition_value,))
            if not self.conditional_field_value == self.condition_value and not self.optional_field_value:
                raise forms.ValidationError(
                    'Please provide an answer for \'{}\'...'.format(self.optional_field_verbose_name,))

    def if_condition_then(self):
        if self.conditional_field_value:
            if (self.conditional_field_value == self.condition_value and
                    not self.optional_field_value == self.required_optional_field_value):
                raise forms.ValidationError(
                    '{} must be {} if {} is {}. Please correct'.format(
                        self.optional_field,
                        self.required_optional_field_value,
                        self.conditional_field,
                        self.condition_value,))
            if (not self.conditional_field_value == self.condition_value and
                    self.optional_field_value == self.required_optional_field_value):
                raise forms.ValidationError(
                    '{} cannot be {} if {} is not \'{}\'. Please correct'.format(
                        self.optional_field, self.optional_field_value, self.conditional_field, self.condition_value,))

    def if_condition_then_not(self):
        if self.conditional_field_value:
            if (self.conditional_field_value == self.condition_value and
                    self.optional_field_value == self.required_optional_field_value):
                raise forms.ValidationError(
                    '{} must not be {} if {} is {}. Please correct'.format(
                        self.optional_field,
                        self.required_optional_field_value,
                        self.conditional_field,
                        self.condition_value,))
            if (self.conditional_field_value != self.condition_value and
                    self.optional_field_value != self.required_optional_field_value):
                raise forms.ValidationError(
                    '{} must be {} if {} is {}. Please correct'.format(
                        self.optional_field, self.optional_field_value, self.conditional_field, self.condition_value,))
