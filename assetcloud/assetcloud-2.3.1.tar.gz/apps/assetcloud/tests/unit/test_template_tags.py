# coding=utf-8
# (c) 2011 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com
from django.core.urlresolvers import reverse
from taggit.utils import parse_tags
from assetcloud.forms import SearchForm
from assetcloud.templatetags.css_utils import file_icon_class
from assetcloud.templatetags.tag_url import remove_tag_from_url
from assetcloud.templatetags import resize
from django import forms
from .utils import UnitTestCase
from django.template import Template, Context


class ResizeTests(UnitTestCase):
    class MockAssetImageInfo(object):
        def __init__(self, width, height):
            self.width = width
            self.height = height

    class MockAsset(object):
        def __init__(self, width, height):
            self.id = 1001
            self.image_info = ResizeTests.MockAssetImageInfo(width, height)

    def setUp(self):
        self.mock = self.get_mock_asset(100, 200)
        self.width = 10
        self.height = 20

    def get_mock_asset(self, width, height):
        return ResizeTests.MockAsset(width, height)

    def test_aspect_width_preserves_aspect_ratio(self):
        width = resize.aspect_width(self.mock, self.height)
        self.assertEqual(self.mock.image_info.height / self.mock.image_info.width,
                         self.height / width)

    def test_aspect_height_preserves_aspect_ratio(self):
        height = resize.aspect_height(self.mock, self.width)
        self.assertEqual(self.mock.image_info.height / self.mock.image_info.width,
                         height / self.width)

    def test_resize_bounds_within_works_for_landscape(self):
        mock = ResizeTests.MockAsset(100, 50)
        expected_width, expected_height = 24, 12
        aspect_width, aspect_height = resize.get_resize_bounds_within(mock, 24)
        self.assertEqual(aspect_width, expected_width)
        self.assertEqual(aspect_height, expected_height)

    def test_resize_bounds_within_works_for_square(self):
        mock = ResizeTests.MockAsset(100, 100)
        expected_width, expected_height = 24, 24
        aspect_width, aspect_height = resize.get_resize_bounds_within(mock, 24)
        self.assertEqual(aspect_width, expected_width)
        self.assertEqual(aspect_height, expected_height)

    def test_resize_bounds_within_works_for_portrait(self):
        mock = ResizeTests.MockAsset(50, 100)
        expected_width, expected_height = 42, 85
        aspect_width, aspect_height = resize.get_resize_bounds_within(mock, 85)
        self.assertEqual(aspect_width, expected_width)
        self.assertEqual(aspect_height, expected_height)

    def test_resize_bounds_within_works_for_landscape_to_portrait_bounds(self):
        mock = ResizeTests.MockAsset(100, 50)
        expected_width, expected_height = 24, 12
        aspect_width, aspect_height = resize.get_resize_bounds_within(
            mock, 1000, 12)
        self.assertEqual(aspect_width, expected_width)
        self.assertEqual(aspect_height, expected_height)

    def test_resize_bounds_within_works_for_portrait_to_landscape_bounds(self):
        mock = ResizeTests.MockAsset(50, 100)
        expected_width, expected_height = 45, 90
        aspect_width, aspect_height = resize.get_resize_bounds_within(
            mock, 45, 1000)
        self.assertEqual(aspect_width, expected_width)
        self.assertEqual(aspect_height, expected_height)

    def test_resize_bounds_within_works_for_large_dimensions(self):
        mock = ResizeTests.MockAsset(11664, 11663)
        expected_width, expected_height = 1024, 1024
        aspect_width, aspect_height = resize.get_resize_bounds_within(mock, 1024, 2000)
        self.assertEqual(aspect_width, expected_width)
        self.assertEqual(aspect_height, expected_height)

    def test_resize_url_with_width(self):
        url = resize.resize_url(self.mock, self.width)
        self.assertEqual(url, reverse(
                'asset-resize-download-width-action',
                args=[self.mock.id, self.width]))

    def test_resize_url(self):
        url = resize.resize_url(self.mock, self.mock.image_info.width, self.mock.image_info.height)
        self.assertEqual(url, reverse(
                'asset-resize-download-action',
                args=[self.mock.id, self.mock.image_info.width, self.mock.image_info.height]))

    def tearDown(self):
        pass


class TagUrlTests(UnitTestCase):
    def test_remove_tag_from_url_removes_tag(self):
        context = self.setup_context(tags="qwerty, asdf", more_tags="sdsd")
        tag = "asdf"

        url = remove_tag_from_url(context, tag)

        self.assertEqual("tags=qwerty", url)

    def test_remove_tag_from_url_removes_tag_non_ascii(self):
        context = self.setup_context(tags=u"qwerty, £££", more_tags="sdsd")
        tag = u"£££"

        url = remove_tag_from_url(context, tag)

        self.assertEqual("tags=qwerty", url)

    def test_remove_tag_from_url_where_tag_is_not_in_tags(self):
        """
        The url should remain unchanged and no error should be thrown.
        """
        context = self.setup_context(tags="qwerty, asdf", more_tags="sdsd")
        tag = "ppp"

        url = remove_tag_from_url(context, tag)

        self.assertEqual("more_tags=sdsd&tags=qwerty%2C+asdf", url)

    def setup_context(self, tags=None, more_tags=None):
        """
        Sets up a stub context object containing tag data that is in the
        expected format (i.e parsed by Taggit).
        """
        form = SearchForm(user="testuser")
        form.data = dict(tags=tags, more_tags=more_tags)

        tags_list = parse_tags(tags)
        more_tags_list = parse_tags(more_tags)
        form.cleaned_data = dict(tags=tags_list, more_tags=more_tags_list)

        return dict(form=form)


class CssUtilsTests(UnitTestCase):
    def test_file_icon_class_for_unknown_type(self):
        icon = file_icon_class("file.xyz")

        self.assertEquals("unknown", icon)

    def test_file_icon_class_for_pdf_file(self):
        icon = file_icon_class("file.pdf")

        self.assertEquals("pdf", icon)

    def test_file_icon_class_for_pdf_file_uppercase(self):
        icon = file_icon_class("file.PDF")

        self.assertEquals("pdf", icon)

    def test_file_icon_class_for_doc_file(self):
        icon = file_icon_class("file.doc")

        self.assertEquals("doc", icon)

    def test_file_icon_class_for_xls_file(self):
        icon = file_icon_class("file.xls")

        self.assertEquals("xls", icon)

    def test_file_icon_class_for_xlsx_file(self):
        icon = file_icon_class("file.xlsx")

        self.assertEquals("xlsx", icon)

    def test_file_icon_class_for_ppt_file(self):
        icon = file_icon_class("file.ppt")

        self.assertEquals("ppt", icon)

    def test_file_icon_class_for_wav_file(self):
        icon = file_icon_class("file.wav")

        self.assertEquals("wav", icon)

    def test_file_icon_class_for_mp3_file(self):
        icon = file_icon_class("file.mp3")

        self.assertEquals("mp3", icon)

    def test_file_icon_class_for_mov_file(self):
        icon = file_icon_class("file.mov")

        self.assertEquals("mov", icon)

    def test_file_icon_class_for_mpg_file(self):
        icon = file_icon_class("file.mpg")

        self.assertEquals("mpg", icon)

    def test_file_icon_class_for_mp4_file(self):
        icon = file_icon_class("file.mp4")

        self.assertEquals("mp4", icon)

    def test_file_icon_class_for_aac_file(self):
        icon = file_icon_class("file.aac")

        self.assertEquals("aac", icon)

    def test_file_icon_class_for_ai_file(self):
        icon = file_icon_class("file.ai")

        self.assertEquals("ai", icon)

    def test_file_icon_class_for_aiff_file(self):
        icon = file_icon_class("file.aiff")

        self.assertEquals("aiff", icon)

    def test_file_icon_class_for_avi_file(self):
        icon = file_icon_class("file.avi")

        self.assertEquals("avi", icon)

    def test_file_icon_class_for_c_file(self):
        icon = file_icon_class("file.c")

        self.assertEquals("c", icon)

    def test_file_icon_class_for_css_file(self):
        icon = file_icon_class("file.css")

        self.assertEquals("css", icon)

    def test_file_icon_class_for_dat_file(self):
        icon = file_icon_class("file.dat")

        self.assertEquals("dat", icon)

    def test_file_icon_class_for_eps_file(self):
        icon = file_icon_class("file.eps")

        self.assertEquals("eps", icon)

    def test_file_icon_class_for_exe_file(self):
        icon = file_icon_class("file.exe")

        self.assertEquals("exe", icon)

    def test_file_icon_class_for_flv_file(self):
        icon = file_icon_class("file.flv")

        self.assertEquals("flv", icon)

    def test_file_icon_class_for_html_file(self):
        icon = file_icon_class("file.html")

        self.assertEquals("html", icon)

    def test_file_icon_class_for_htm_file(self):
        icon = file_icon_class("file.htm")

        self.assertEquals("htm", icon)

    def test_file_icon_class_for_odf_file(self):
        icon = file_icon_class("file.odf")

        self.assertEquals("odf", icon)

    def test_file_icon_class_for_ods_file(self):
        icon = file_icon_class("file.ods")

        self.assertEquals("ods", icon)

    def test_file_icon_class_for_odt_file(self):
        icon = file_icon_class("file.odt")

        self.assertEquals("odt", icon)

    def test_file_icon_class_for_otp_file(self):
        icon = file_icon_class("file.otp")

        self.assertEquals("otp", icon)

    def test_file_icon_class_for_ots_file(self):
        icon = file_icon_class("file.ots")

        self.assertEquals("ots", icon)

    def test_file_icon_class_for_ott_file(self):
        icon = file_icon_class("file.ott")

        self.assertEquals("ott", icon)

    def test_file_icon_class_for_psd_file(self):
        icon = file_icon_class("file.psd")

        self.assertEquals("psd", icon)

    def test_file_icon_class_for_py_file(self):
        icon = file_icon_class("file.py")

        self.assertEquals("py", icon)

    def test_file_icon_class_for_qt_file(self):
        icon = file_icon_class("file.qt")

        self.assertEquals("qt", icon)

    def test_file_icon_class_for_rar_file(self):
        icon = file_icon_class("file.rar")

        self.assertEquals("rar", icon)

    def test_file_icon_class_for_rtf_file(self):
        icon = file_icon_class("file.rtf")

        self.assertEquals("rtf", icon)

    def test_file_icon_class_for_sql_file(self):
        icon = file_icon_class("file.sql")

        self.assertEquals("sql", icon)

    def test_file_icon_class_for_tgz_file(self):
        icon = file_icon_class("file.tgz")

        self.assertEquals("tgz", icon)

    def test_file_icon_class_for_txt_file(self):
        icon = file_icon_class("file.txt")

        self.assertEquals("txt", icon)

    def test_file_icon_class_for_xml_file(self):
        icon = file_icon_class("file.xml")

        self.assertEquals("xml", icon)

    def test_file_icon_class_for_zip_file(self):
        icon = file_icon_class("file.zip")

        self.assertEquals("zip", icon)

    def test_file_icon_class_for_tiff_file(self):
        icon = file_icon_class("file.tiff")

        self.assertEquals("tiff", icon)

    def test_file_icon_class_for_TIIF_file(self):
        icon = file_icon_class("file.TIFF")

        self.assertEquals("tiff", icon)

    def test_file_icon_class_for_tif_file(self):
        icon = file_icon_class("file.tif")

        self.assertEquals("tif", icon)

    def test_file_icon_class_for_TIF_file(self):
        icon = file_icon_class("file.TIF")

        self.assertEquals("tif", icon)


class RenderformTests(UnitTestCase):
    def test_renderform_renders_helptext(self):
        class HelptextForm(forms.Form):
            help_field = forms.CharField(help_text='sample help text')
        form = HelptextForm()
        template = Template("{% load renderform %}{% render_form form %}")
        context = Context({'form': form})
        self.assertIn('sample help text', template.render(context))
