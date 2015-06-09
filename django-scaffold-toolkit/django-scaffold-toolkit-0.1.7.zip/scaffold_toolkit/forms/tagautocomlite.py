# coding=utf-8
from django import forms
from django.conf import settings
from django.shortcuts import resolve_url
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
import os


class TagAutocompleteInput(forms.TextInput):
    def _media(self):
        from django.utils import translation

        lang = translation.get_language().replace('_', '-')
        if lang == 'zh-hans':
            lang = 'zh-CN'
        lang_js = '%slibrary/select2-3.5.2/select2_locale_%s' % (settings.STATIC_URL, lang) if os.path.exists(
            '%slibrary/select2-3.5.2/select2_locale_%s' % (settings.STATIC_ROOT, lang)) else ''
        js = ['%sjavascript/library/select2-3.5.2/select2.js' % settings.STATIC_URL]
        if lang_js:
            js.append(lang_js)

        return forms.Media(css={'all': ['%sjavascript/library/select2-3.5.2/select2.css' % settings.STATIC_URL,
                                        '%sjavascript/library/select2-3.5.2/select2-bootstrap.css' % settings.STATIC_URL]},
                           js=js)

    media = property(_media)

    def render(self, name, value, attrs=None):
        js = u"""<script>
    require(['select2','select2_cn'],function(){{
    $("#{id_for_label}").select2({{
    placeholder: '科目拼音或名称',
        tags:true,
        multiple: true,
         tokenSeparators: [",", " ",";"],
        ajax: {{
            url: "{url}",
            dataType: 'json',
            data: function (term) {{
                return{{term: term}}
            }},
            results: function (data) {{
                return {{results: data}};
            }}
        }},
        createSearchChoice: function(term, data) {{
            if ($(data).filter(function() {{
              return this.text.localeCompare(term) === 0;
            }}).length === 0) {{
              return {{
                id: term,
                text: term
              }};
            }}
        }},
        initSelection: function (element, callback) {{
            var data = [];
            $(element.val().split(",")).each(function (index,name) {{
                data.push({{id: this, text: name}});
            }});
            callback(data);
        }},
        minimumInputLength: 1,
        triggerChange: true
    }})
    }})
    </script>
    """
        js = js.format(id_for_label=force_text(self.id_for_label('id_%s' % name)),
                       url=force_text(resolve_url('tag_suggestion')))

        code = "%s %s" % (super(TagAutocompleteInput, self).render(name, value, attrs), js)
        return mark_safe(code)
