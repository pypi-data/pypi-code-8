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

from pyny import api
from pyny.fields import BaseField


class Model:
    """
    JSONをマッピングするモデルのスーパークラス。
    モデルクラスを定義する場合は当クラスを継承すること。
    """

    def __init__(self, data):
        """
        Modelを構築する。

        :param data: マッピング対象のJSON
        :type data: dict
        """
        # JSONをモデルにマッピングする
        for k, v in self.__class__.__dict__.items():
            # フィールドクラス以外は無視する
            if not isinstance(v, BaseField):
                continue

            # プロパティに値を設定する
            field_name = v.name or k
            value = self._get_value(data, field_name)
            setattr(self, k, v.convert(value) if value is not None else None)

    @classmethod
    def get_data(cls, layer_id, feature_id):
        """
        指定されたレイヤID、項目IDにマッチするデータを取得する。

        :param layer_id: レイヤID
        :type layer_id: str
        :param feature_id: 項目ID
        :type feature_id: int
        :return: マッチするデータが存在する場合はそのデータ、存在しない場合はNone
        :rtype: Model
        """
        # 条件に合致するデータを取得する
        data = api.get_data(layer_id, feature_id)
        if data:
            return cls(data)
        else:
            return None

    @classmethod
    def get_all_data(cls, layer_id):
        """
        指定されたレイヤIDにマッチするすべてのデータを取得する。

        :param layer_id: レイヤID
        :type layer_id: str
        :return: マッピングされたモデルのリスト
        :rtype: list
        """
        # 当該レイヤIDの全データを取得する
        return [cls(data) for data in api.get_all_data(layer_id)]

    def _get_value(self, data, key):
        """
        辞書の中から指定されたキーに対応する値を取得する。
        キーにドットが含まれる場合はドットをキーの区切り文字として再帰的に辞書を探索する。

        :param data: 探索対象の辞書
        :type data: dict
        :param key: キー
        :type key: str
        :return: 辞書から取得した値
        :rtype: object
        """
        # 辞書を再帰的に探索する
        if '.' in key:
            new_keys = key.split('.', 1)
            new_data = data.get(new_keys[0])
            return self._get_value(new_data, new_keys[1]) if new_data else None
        else:
            return data.get(key)
