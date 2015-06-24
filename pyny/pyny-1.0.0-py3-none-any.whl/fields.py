# -*- coding: utf-8 -*-

#
# Copyright 2015 Jun-ya HASEBA
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from abc import ABCMeta, abstractmethod
import datetime
import decimal


class BaseField(metaclass=ABCMeta):
    """
    すべてのフィールドクラスのスーパークラス。
    新しいフィールドクラスを実装する場合は当クラスを継承すること。
    """

    def __init__(self, name=None):
        """
        BaseFieldを構築する。

        :param name: 当フィールドが参照する値のキー
        :type name: str
        """
        # プロパティを設定する
        self.name = name

    @abstractmethod
    def convert(self, target):
        """
        指定された値をそのフィールドクラスに適した型に変換する。
        サブクラスでそれぞれのクラスに応じた値を返すようオーバーライドすること。

        :param target: 変換対象
        :type target: object
        :return: 変換後の値
        :rtype: object
        """
        raise NotImplementedError()


class StringField(BaseField):
    """
    文字列を表現するフィールドクラス。
    """

    def __init__(self, name=None):
        """
        StringFieldを構築する。

        :param name: 当フィールドが参照する値のキー
        :type name: str
        """
        # プロパティを設定する
        super().__init__(name)

    def convert(self, target):
        """
        指定された値を文字列に変換する。

        :param target: 変換対象
        :type target: object
        :return: 変換後の値
        :rtype: str
        """
        # 対象が文字列の場合は変換せずに返却する
        if isinstance(target, str):
            return target

        # 対象を文字列に変換する
        return str(target)


class IntegerField(BaseField):
    """
    整数を表現するフィールドクラス。
    """

    def __init__(self, name=None):
        """
        IntegerFieldを構築する。

        :param name: 当フィールドが参照する値のキー
        :type name: str
        """
        # プロパティを設定する
        super().__init__(name)

    def convert(self, target):
        """
        指定された値を整数に変換する。

        :param target: 変換対象
        :type target: object
        :return: 変換後の値
        :rtype: int
        """
        # 対象が整数の場合は変換せずに返却する
        if isinstance(target, int):
            return target

        # 対象を整数に変換する
        return int(target)


class DecimalField(BaseField):
    """
    固定小数点数を表現するフィールドクラス。
    """

    def __init__(self, name=None):
        """
        DecimalFieldを構築する。

        :param name: 当フィールドが参照する値のキー
        :type name: str
        """
        # プロパティを設定する
        super().__init__(name)

    def convert(self, target):
        """
        指定された値を固定小数点数に変換する。

        :param target: 変換対象
        :type target: object
        :return: 変換後の値
        :rtype: decimal.Decimal
        """
        # 対象が固定小数点数の場合は変換せずに返却する
        if isinstance(target, decimal.Decimal):
            return target

        # 対象を固定小数点数に変換する
        return decimal.Decimal(str(target))


class FloatField(BaseField):
    """
    浮動小数点数を表現するフィールドクラス。
    """

    def __init__(self, name=None):
        """
        FloatFieldを構築する。

        :param name: 当フィールドが参照する値のキー
        :type name: str
        """
        # プロパティを設定する
        super().__init__(name)

    def convert(self, target):
        """
        指定された値を浮動小数点数に変換する。

        :param target: 変換対象
        :type target: object
        :return: 変換後の値
        :rtype: float
        """
        # 対象が浮動小数点数の場合は変換せずに返却する
        if isinstance(target, float):
            return target

        # 対象を浮動小数点数に変換する
        return float(target)


class DateField(BaseField):
    """
    日付を表現するフィールドクラス。
    """

    def __init__(self, name=None, fmt='%Y/%m/%d'):
        """
        DateFieldを構築する。

        :param name: 当フィールドが参照する値のキー
        :type name: str
        :param fmt: 日付のフォーマット
        :type fmt: str
        """
        # プロパティを設定する
        super().__init__(name)
        self._fmt = fmt

    def convert(self, target):
        """
        指定された値を日付に変換する。

        :param target: 変換対象
        :type target: object
        :return: 変換後の値
        :rtype: datetime.date
        """
        # 対象が日付の場合は変換せずに返却する
        if isinstance(target, datetime.date):
            return target

        # 対象を日付に変換する
        return datetime.datetime.strptime(str(target), self._fmt).date()


class DateTimeField(BaseField):
    """
    日時を表現するフィールドクラス。
    """

    def __init__(self, name=None, fmt='%Y/%m/%d %H:%M:%S'):
        """
        DateTimeFieldを構築する。

        :param name: 当フィールドが参照する値のキー
        :type name: str
        :param fmt: 日時のフォーマット
        :type fmt: str
        """
        # プロパティを設定する
        super().__init__(name)
        self._fmt = fmt

    def convert(self, target):
        """
        指定された値を日時に変換する。

        :param target: 変換対象
        :type target: object
        :return: 変換後の値
        :rtype: datetime.datetime
        """
        # 対象が日時の場合は変換せずに返却する
        if isinstance(target, datetime.datetime):
            return target

        # 対象を日時に変換する
        return datetime.datetime.strptime(str(target), self._fmt)
