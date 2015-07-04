#
# -*- encoding: utf-8 -*-

"""
sortorder.ja.py
~~~~~~~~~~~~~~~
日本語用の SortOrderBase を定義するモジュール

:copyright: © 2011-2015 鈴見咲君高(Suzumizaki-Kimitaka)
:license: 二項BSD(2-clause BSD)

日本語用の :class:`sortorder.SortOrderBase` 実装です。

Yogosyu(用語集)拡張においては sortorder のほかに yogosyu と
user_ordered_index_patch の両方を :code:`extension` に含める\
必要があります。

:file:`conf.py` で :code:`language = 'ja'` を指定しておけば\
何もしなくても必要な拡張から読み込まれるようになっています。
そうでない場合は ext の拡張リストの中に :code:`sortorder_ja` を
含めることで自動的に SortOrderJa が使われるようになります。

Yogosyu拡張においては :code:`yogosyu` directive で\
読みがなを与えることになります。読みがなと言っても必ずしも\
ひらがな・カタカナでなくても構いません。索引を目で探すことを\
考えて設定してください。例えば、英単語に対してカタカナを\
当てることにはあまり意味がありません。単語の一部が英語に\
なっている場合、ルビとは異なり読み仮名も英語のままにしておく\
ほうが良いように思います。
"""

import sortorder
import string
import sys

ord_hiragana_begins = 0x3041 # Unicodeにおけるひらがなの最初の番号
ord_hiragana_vu = 0x3094 # Unicodeにおける「ゔ」の番号
ord_hiragana_ends = 0x3097 # Unicodeにおけるひらがなの最後の番号
ord_katakana_begins = 0x30a1 # Unicodeにおけるカタカナの最初の番号
ord_katakana_vu = 0x30f4 # Unicodeにおける「ヴ」の番号

diff_katakana_hiragana = ord_katakana_begins - ord_hiragana_begins

if sys.version_info[0] >= 3:
    unichr = lambda i: chr(i)

def hiragana_to_katakana(s):
    """カタカナをひらがなに変換します

    :param str_or_unicode s: 変換したいカタカナ文字列をご指定ください
    :rtype: str(Python 3), unicode(Python 2)
    :return: カタカナ部分をひらがなにした文字列を返します
    
    cp932に含まれていないカタカナも全部変換して返します。
    """
    r = u''
    for c in s:
        if ord_hiragana_begins <= ord(c) <= ord_hiragana_vu:
            r += unichr(ord(c) + diff_katakana_hiragana)
        else:
            r += c
    return r

vowels_for_tyoon = (
    u'アァカヵガタダナハバパマヤャラワヮヷ',
    u'イィキギシジチヂニヒビピミリヰヸ',
    u'ウヴゥクグスズツッヅヌフブプムユュル', 
    u'エェケヶゲセゼテデネヘベペメレヱヹ',
    u'オォコゴソゾトドノホボポモヨョロヲヺ',
    u'ン',
    )

def tyoon_to_vowel(s):
    """長音符号を母音のカタカナに変換します

    :param str_or_unicode s: 変換したい長音を含む文字列の全体
    :rtype: str(Python 3), unicode(Python 2)
    :return: 変換結果を返します

    各長音符号を、それぞれ直前の文字に基づいて母音に変換した結果を返します。
    """
    r = u''
    for c in s:
        if c != u'ー' or not len(r):
            r += c
            continue
        prev = r[-1]
        for l in vowels_for_tyoon:
            if prev in l:
                r += l[0]
                break
        else:
            r += c
    return r    

kana_need_insert_after = {
    u'ウ': u'ヴ',
    u'カ': u'ヵ',
    u'ケ': u'ヶ',
    u'ワ': u'ヷ',
    u'ヰ': u'ヸ',
    u'ヱ': u'ヹ',
    u'ヲ': u'ヺ',
    }
sutegana_katakana_swappable = u'ァィゥェォッャュョヮ'
katakana_swappable_with = u'アイウエオツヤユヨワ'
kana_reorder = u''
for k in range(ord_katakana_begins, ord_katakana_vu):
    kc = unichr(k)
    idx = katakana_swappable_with.find(kc)
    if idx >= 0:
        ks = sutegana_katakana_swappable[idx]
        kana_reorder = kana_reorder[:-1] + kc + kana_reorder[-1]
    else:
        kana_reorder += kc
    if kc in kana_need_insert_after:
        kana_reorder += kana_need_insert_after[kc]        
headings = {
    kana_reorder[:11]: u"あ",
    kana_reorder[11:23]: u"か",
    kana_reorder[23:33]: u"さ",
    kana_reorder[33:44]: u"た",
    kana_reorder[44:49]: u"な",
    kana_reorder[49:64]: u"は",
    kana_reorder[64:69]: u"ま",
    kana_reorder[69:75]: u"や",
    kana_reorder[75:80]: u"ら",
    kana_reorder[80:90]: u"わ",
    }
assert len(kana_reorder) == 90
assert kana_reorder[75:80] == u'ラリルレロ'


class SortOrderJa(sortorder.SortOrderBase):
    """Japanese specific SortOrder implementation

    日本語用の :class:`sortorder.SortOrderBase` 実装です。
    
    並べ替えは次の順序になります:

    #. 小書きの文字は通常文字の直後
    #. 濁音は対応する清音の直後
    #. 半濁音は対応する濁音の直後
    #. ASCII内の英字はかなの後ろ
    #. 大文字小文字・ひらがなカタカナは区別しない
    #. 一方が他方を包含する場合は短い方が先
    #. genindexの索引においてはかな→英字→その他の順
    #. 長音は適切であれば「あいうえおん」のどれかに置換

    :file:`conf.py` 用にいろいろ定義して細かく制御もできそうですが、
    それは今後の課題、あるいは皆さんでご自由に。
    """

    def get_string_to_sort(self, entry_name):
        """入力に対する整序用文字列を返します

        :param str_or_unicode entry_name: 元の文字列かその読みがなを与えてください
        :rtype: str(Python 3), unicode(Python 2)
        :return: 整序用の文字列を返します

        :class:`sortorder.SortOrderBase` の実装関数です。
        
        定義のとおり、読みがな自体を返すわけではないことにご注意ください。
        """
        s = self.get_ja_canonical_yomi(entry_name)
        r = u''
        for c in s:
            idx = kana_reorder.find(c)
            if idx >= 0:
                r += unichr(ord_hiragana_begins + idx)
            else:
                r += c
        if r[0] in string.ascii_letters:
            return u'\ufffd' + r.lower()
        return r.lower()

    def get_group_name(self, entry_name):
        """与えられた項目名に対するグループ名を返します

        :param str_or_unicode entry_name: グループ名が欲しい文字列かその読み文字列
        :rtype: str(Python 3), unicode(Python 2)
        :return: 与えられた文字列に対するグループ名を返します
        
        :class:`sortorder.SortOrderBase` の実装関数です。

        英字は文字通り英字のみでまとめてグループ化します。\
        各自の実装ではこのあたりに工夫の余地があるでしょう。
        """
        s = self.get_ja_canonical_yomi(entry_name)
        if s[0] in string.ascii_letters:
            return u'英字'
        for k,v in headings.items():
            if s[0] in k:
                return v
        return u"その他"

    def get_ja_canonical_yomi(self, entry_name):
        """与えられた名前の読みを返します
        
        :param str_or_unicode entry_name: 読みがなが欲しい文字列をご指定ください
        :rtype: str(Python 3), unicode(Python 2)
        :return: 与えられた文字列に対する索引用の読みがなを返します

        このクラス専用の内部関数です。
        読みを得た上でひらがなをカタカナにし、\
        長音を母音化した文字列を返します。
        """
        n = hiragana_to_katakana(entry_name)
        n = tyoon_to_vowel(n)
        return n


def get_default_sort_order(cfg):
    """このmoduleで定義したsortorder.SortOrderBaseクラスの実体を返します

    :param sphinx.config.Config cfg: Sphinxの設定、ただし現時点で参照されていません
    :rtype: SortOrderJa
    :return: class:`SortOrderJa` の実体を返します

    :file:`sortorder.__init__.py` の同名methodから呼び出されます。
    """
    return SortOrderJa()

def setup(app):
    """Sphinxから呼び出される初期化関数です
    
    :param sphinx.application.Sphinx app: 環境や設定を含むオブジェクト
    :rtype: None
    :return: None
    """
    sortorder.setup(app)
    app.add_config_value('sort_order', SortOrderJa(), 'env')
