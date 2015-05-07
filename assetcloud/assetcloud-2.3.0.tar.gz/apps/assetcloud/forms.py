# (c) 2011 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com
from datetime import timedelta
import logging

from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets
from taggit.models import Tag
import haystack.forms

from assetcloud.asset_metadata_util import get_metadata_model_and_form_classes, get_asset_metadata_for_metadata_model
from assetcloud.widgets import PreviewImageWidget, TagSearchWidget
from assetcloud.fields import ClientsideTagField, SpacesAllowedTagField
from assetcloud.models import Asset, Account, DEFAULT_COLOURS
from assetcloud.upload_history import filter_assets_by_last_upload
from assetcloud import app_settings


logger = logging.getLogger(__name__)


class AssetForm(forms.ModelForm):
    """
    Form for editing assets.
    """

    def __init__(self, *args, **kwargs):
        super(AssetForm, self).__init__(*args, **kwargs)
        self.initialise_metadata_forms(*args, **kwargs)

    def initialise_metadata_forms(self, *args, **kwargs):
        self.metadata_forms = []

        for asset_metadata_model in app_settings.ASSET_METADATA_MODELS:

            metadata_model, metadata_form = get_metadata_model_and_form_classes(asset_metadata_model)

            if "instance" in kwargs:
                del kwargs["instance"]

            if self.instance:
                metadata_instance = get_asset_metadata_for_metadata_model(self.instance, metadata_model)

                kwargs["instance"] = metadata_instance

            self.metadata_forms.append(metadata_form(*args, **kwargs))

    def is_valid(self):
        form_valid = super(AssetForm, self).is_valid()

        for form in self.metadata_forms:
            form_valid &= form.is_valid()

        return form_valid

    def has_metadata_errors(self):
        for metadata_form in self.metadata_forms:
            if metadata_form.errors:
                return True
        return False

    def save(self, commit=True):
        super(AssetForm, self).save(commit)

        for form in self.metadata_forms:
            form.save(commit)

    class Meta:
        model = Asset
        fields = ('title', 'description', 'thumbnail')
        widgets = {
            "thumbnail": PreviewImageWidget
        }


class InvalidAssetIdsError(RuntimeError):
    pass


def parse_asset_ids(asset_ids):
    """
    Parse a comma-separated asset ID string into a list
    """
    if not asset_ids:
        return []
    try:
        return [int(s) for s in asset_ids.split(',')]
    except ValueError:
        raise InvalidAssetIdsError()


class AssetIdsField(forms.CharField):
    widget = widgets.HiddenInput

    def to_python(self, value):
        try:
            return parse_asset_ids(value)
        except InvalidAssetIdsError:
            raise ValidationError("Couldn't parse %s into asset IDs" % value)


class ShareAssetsForm(forms.Form):
    asset_ids = AssetIdsField()
    recipient = forms.EmailField(required=True, label="Email to", widget=forms.TextInput(attrs={'placeholder': 'Recipients email'}))
    message = forms.CharField(required=False, widget=forms.Textarea(), label="Include a personal message (optional)")


class CustomiseForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = (
            'welcome_text',
            'logo',
            'header_background',
            'header_links',
            'header_links_active',
            'subdomain',
            )
        widgets = {
            'logo': PreviewImageWidget(img_class='custom-logo'),
            }

    homepage_tags_json = ClientsideTagField()

    def __init__(self, *args, **kwargs):
        super(CustomiseForm, self).__init__(*args, **kwargs)

        # For use in customise.html
        self.colour_fields = [self[field_name]
                              for field_name in Account.COLOUR_FIELD_NAMES]

        self._change_blank_colours_to_default()

    def _change_blank_colours_to_default(self):
        for field in self.colour_fields:
            if not self.initial[field.name]:
                self.initial[field.name] = DEFAULT_COLOURS[field.name]

    def save(self, commit=True):
        result = super(CustomiseForm, self).save(commit)
        if commit:
            self.instance.homepage_tags.set(*self.cleaned_data['homepage_tags_json'])
        return result


class TagSetForm(forms.Form):
    """
    Takes a comma or space separated text string, and returns a list of tags.

    For details on behaviour, see:
        http://django-taggit.readthedocs.org/en/latest/forms.html
    """
    tags = SpacesAllowedTagField()


class SearchForm(haystack.forms.SearchForm):
    """
    Asset Cloud's tweaked version of Haystack's search form.
    Filters search results by account.
    """
    from_date = forms.DateField(
        label="between:",
        required=False,
        widget=widgets.DateInput(attrs={'class': 'date-field'})
    )
    until_date = forms.DateField(
        label="and:",
        required=False,
        widget=widgets.DateInput(attrs={'class': 'date-field'})
    )

    tags = SpacesAllowedTagField(
        required=False,
        widget=widgets.HiddenInput(attrs={'id': 'tags'})
    )

    more_tags = SpacesAllowedTagField(
        required=False,
        label='',
        widget=TagSearchWidget(attrs={'class': 'add_more_tags', 'placeholder': 'Start typing...'})
    )

    last_upload = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')

        # Let assetcloud.views.SearchView.build_form() override data arg (see
        # comment in that method to find out why).
        if 'data_override' in kwargs:
            data_override = kwargs.pop('data_override')
            # Data can be passed as a positional argument or a keyword argument.
            # If it has been passed as a positional argument and we add it as
            # a keyword argument then we get a
            # TypeError: __init__() got multiple values for keyword argument
            # 'data'
            # so we make sure to override the positional arg and not the kw arg
            # if it has already been passed as a positional arg
            if len(args) >= 1:
                args = (data_override,) + args[1:]
            else:
                kwargs['data'] = data_override

        super(SearchForm, self).__init__(*args, **kwargs)

    def clean(self):
        """
        Django calls clean() to validate form data prior to processing:
        self.cleaned_data = validated form data that is ready to processed
        self.data = (raw) form data (that can be displayed on the page)
        """
        super(SearchForm, self).clean()

        if self.cleaned_data.get('from_date') and \
                self.cleaned_data.get('until_date') and \
                self.cleaned_data.get('from_date') > \
                self.cleaned_data.get('until_date'):
            self.swap_cleaned_dates()
            self.swap_raw_dates()

        if self.cleaned_data.get('more_tags'):
            self.merge_cleaned_tags()
            self.merge_raw_tags()

        # When a last upload filter is in effect and the user adds a date
        # range filter we want to remove the last upload filter, because date
        # range and last upload filters are mutually exclusive. We remove the
        # last upload filter here instead of changing the parameters that the
        # front end sends through because having the front end remove the
        # last upload parameter would be more complex.
        if self.have_date_range_filter() and self.have_last_upload_filter():
            del self.cleaned_data['last_upload']

        return self.cleaned_data

    def swap_cleaned_dates(self):
        later_date = self.cleaned_data['from_date']
        earlier_date = self.cleaned_data['until_date']
        self.cleaned_data['from_date'] = earlier_date
        self.cleaned_data['until_date'] = later_date

    def swap_raw_dates(self):
        # Copy self.data so that we can modify it without getting a "This
        # QueryDict instance is immutable" error }:->
        self.data = self.data.copy()

        later_date = self.data['from_date']
        earlier_date = self.data['until_date']
        self.data['from_date'] = earlier_date
        self.data['until_date'] = later_date

    def merge_cleaned_tags(self):
        tags = self.cleaned_data['tags']
        more_tags = self.cleaned_data['more_tags']
        tags.extend(more_tags)

        self.cleaned_data['tags'] = tags
        self.cleaned_data['more_tags'] = None

    def merge_raw_tags(self):
        """
        We are using the cleaned tags as they have been parsed by Taggit
        (see LowerCasingTagField) into a neat set of tags.
        """
        self.data = self.data.copy()

        tags = self.cleaned_data['tags']
        self.data['tags'] = ", ".join(tags)
        self.data['more_tags'] = ''

    def search(self):
        if not self.is_valid():
            return self.no_query_found()

        sqs = self.searchqueryset.all()

        sqs = self.apply_query_string_filters(sqs)

        sqs = self.apply_date_filters(sqs)

        sqs = self.apply_tag_filters(sqs)

        sqs = self.apply_last_upload_filter(sqs)

        sqs = self.apply_access_control_filters(sqs)

        sqs = sqs.order_by('-added')

        if self.load_all:
            sqs = sqs.load_all()

        return sqs

    def have_date_filter(self):
        """
        Is a date filter in effect?

        Note that 'last upload' is considered a date filter.
        """
        return self.have_date_range_filter() or \
               self.have_last_upload_filter()

    def have_date_range_filter(self):
        return self.is_valid() and \
               (self.cleaned_data.get('from_date') or
                self.cleaned_data.get('until_date'))

    def have_last_upload_filter(self):
        return self.is_valid() and \
               bool(self.cleaned_data.get('last_upload'))

    def have_tag_filter(self):
        return self.is_valid() and \
               (self.cleaned_data.get('tags') or
                self.cleaned_data.get('more_tags'))

    def apply_query_string_filters(self, sqs):
        q = self.cleaned_data['q']
        if q:
            sqs = sqs.auto_query(q)
        return sqs

    def apply_date_filters(self, sqs):
        added_gte = self.cleaned_data.get('from_date')
        added_lte = self.cleaned_data.get('until_date')

        if added_gte:
            sqs = sqs.filter(added__gte=added_gte)
        if added_lte:
            added_lt = added_lte + timedelta(days=1)
            sqs = sqs.filter(added__lt=added_lt)

        return sqs

    def apply_tag_filters(self, sqs):
        tags = self.cleaned_data.get('tags')
        if tags:
            for tag_name in tags:
                try:
                    tag = Asset.tags.get(name__exact=tag_name)
                except Tag.DoesNotExist:
                    # If the tag does not exist then there can't possibly be
                    # any results for it, so return no results
                    return sqs.none()
                tag_id = tag.id
                sqs = sqs.filter(tags=tag_id)
        return sqs

    def apply_last_upload_filter(self, sqs):
        if self.have_last_upload_filter():
            sqs = filter_assets_by_last_upload(sqs, self.user)
        return sqs

    def apply_access_control_filters(self, sqs):
        return self.user.get_profile().filter_search(sqs)

    def _remove_date_filter(self, d):
        d = d.copy()
        d.pop('from_date', None)
        d.pop('until_date', None)
        d.pop('last_upload', None)
        return d

    def query_string_without_date_filter(self):
        query_dict = self._remove_date_filter(self.data.copy())
        return query_dict.urlencode()

    def query_string_with_last_upload(self):
        # Sometimes self.data is just a plain dict when this method is called
        # when there are no query params (the other methods aren't called if
        # there are no query params).
        if not self.data:
            return 'last_upload=True'

        query_dict = self._remove_date_filter(self.data.copy())
        query_dict['last_upload'] = 'True'

        return query_dict.urlencode()

    def query_string_without_tag_filter(self):
        query_dict = self.data.copy()
        query_dict.pop('tags', None)
        query_dict.pop('more_tags', None)
        return query_dict.urlencode()

    def tag_list(self):
        return self.cleaned_data['tags']
