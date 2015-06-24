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

import json
from urllib.request import urlopen


# 流山市オープンデータWeb APIのURL
WEB_API_URL = 'http://nagareyama.ecom-plat.jp/map/api/feature/8?layers=%s&pagenum=%d'


class WebApiError(Exception):
    """
    Web APIへのリクエストが正常に完了しなかったことを示す例外。
    """


def get_data(layer_id, feature_id):
    """
    指定されたレイヤID、項目IDにマッチするデータを取得する。

    :param layer_id: レイヤID
    :type layer_id: str
    :param feature_id: 項目ID
    :type feature_id: int
    :return: マッチするデータが存在する場合はそのデータ、存在しない場合はNone
    :rtype: dict
    """
    # すべてのデータを取得する
    all_data = get_all_data(layer_id)

    # 項目IDが一致するデータを探索する
    for data in all_data:
        if data['feature_id'] == feature_id:
            return data
    else:
        return None


def get_all_data(layer_id):
    """
    指定されたレイヤIDにマッチするすべてのデータを取得する。

    :param layer_id: レイヤID
    :type layer_id: str
    :return: 辞書にまとめられたデータのリスト
    :rtype: list
    """
    # データの件数を取得する
    data_count = get_data_count(layer_id)

    # 当該レイヤIDの全データを取得する
    data = _get_json(WEB_API_URL % (layer_id, data_count))
    return data['results']


def get_data_count(layer_id):
    """
    指定されたレイヤIDにマッチするデータの件数を取得する。

    :param layer_id: レイヤID
    :type layer_id: str
    :return: データの件数
    :rtype: int
    """
    # データの件数を取得する
    data = _get_json(WEB_API_URL % (layer_id, 1))
    return int(data['num'])


def _get_json(url):
    """
    指定されたURLにGETでアクセスし、結果のJSONをPythonオブジェクトとして取得する。

    :param url: URL
    :type url: str
    :return: Pythonオブジェクトに変換したJSONの内容
    :rtype: dict
    :raises WebApiError: Web APIへのリクエストが正常に完了しなかった
    """
    # JSONを取得してPythonオブジェクトに変換する
    try:
        with urlopen(url) as response:
            encoding = response.headers.get_content_charset() or 'utf-8'
            return json.loads(response.read().decode(encoding, 'ignore'))
    except Exception as e:
        raise WebApiError(e)
