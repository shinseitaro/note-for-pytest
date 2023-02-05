import csv
from pprint import pprint

import pytest
from connpass_client import ConnpassClient, io

# 練習課題
# 一つのイベントリクエストに対するテスト
# an_event_data フィクスチャを使って以下のテストを書いてみましょ

# an_event_data で得ることができる辞書のキーは、['results_start', 'results_returned', 'results_available', 'events'] である
def test_no2_1(an_event_data):
    res = set(an_event_data.keys())

    assert res == set(
        [
            "results_start",
            "results_returned",
            "results_available",
            "events",
        ]
    )


# events の配列データは１つである
def test_no2_2(an_event_data):
    assert len(an_event_data["events"]) == 1


# events キーに紐づく配列に格納された一つの辞書データのキーは ['event_id', 'title', 'catch', 'description', 'event_url', 'started_at', 'ended_at', 'limit', 'hash_tag', 'event_type', 'accepted', 'waiting', 'updated_at', 'owner_id', 'owner_nickname', 'owner_display_name', 'place', 'address', 'lat', 'lon', 'series'] と一致する
def test_no2_3(an_event_data):
    assert set(an_event_data["events"][0]) == set(
        [
            "event_id",
            "title",
            "catch",
            "description",
            "event_url",
            "started_at",
            "ended_at",
            "limit",
            "hash_tag",
            "event_type",
            "accepted",
            "waiting",
            "updated_at",
            "owner_id",
            "owner_nickname",
            "owner_display_name",
            "place",
            "address",
            "lat",
            "lon",
            "series",
        ]
    )


# results_returnedと events の配列データ数は一致する
def test_no2_4(an_event_data):
    assert an_event_data["results_returned"] == len(an_event_data["events"])


