import csv
from pprint import pprint

import pytest
from connpass_client import ConnpassClient, io

# 複数のイベントリクエストに対するテスト
# some_events_data フィクスチャを使って以下のテストを書いてみましょう。

# some_events_data のレスポンスフィールドは、['results_start', 'results_returned', 'results_available', 'events'] である
def test_no3_1(some_events_data):
    res = set(some_events_data.keys())
    assert res == set(
        [
            "results_start",
            "results_returned",
            "results_available",
            "events",
        ]
    )

# events の配列データは7つである
def test_no3_2(some_events_data):
    events = some_events_data["events"]
    assert len(events) == 7

# events の配列データで返ってくるそれぞれの辞書データのキーは ['event_id', 'title', 'catch', 'description', 'event_url', 'started_at', 'ended_at', 'limit', 'hash_tag', 'event_type', 'accepted', 'waiting', 'updated_at', 'owner_id', 'owner_nickname', 'owner_display_name', 'place', 'address', 'lat', 'lon', 'series'] と一致する

def test_no3_3(some_events_data):
    for data in some_events_data["events"]:
        assert set(data.keys()) == set(['event_id', 'title', 'catch', 'description', 'event_url', 'started_at', 'ended_at', 'limit', 'hash_tag', 'event_type', 'accepted', 'waiting', 'updated_at', 'owner_id', 'owner_nickname', 'owner_display_name', 'place', 'address', 'lat', 'lon', 'series'])
    

# イベントIDがリクエストした時のID７つと一致すること
def test_no3_4(some_events_data):
    ids = set([d["event_id"] for d in some_events_data["events"]]) 
    assert ids == set([273501, 272790, 271250, 270289, 269404, 266898, 264872])

# results_returnedと events の配列データ数は一致する
def test_no3_5(some_events_data):
    assert some_events_data["results_returned"] == len(some_events_data["events"])

# owner_id は全て 36417 である
def test_no3_6(some_events_data):
    ids = set([d["owner_id"] for d in some_events_data["events"]]) 
    assert ids == set([36417])

# events の配列データは、開催日時順が降順(新着順)である
def test_no3_7(some_events_data):
    from datetime import datetime

    # これ chatgpt に書いてもらった
    def _is_descending_order(dates_list):
      return all(dates_list[i] >= dates_list[i+1] for i in range(len(dates_list) - 1))

    dts = [datetime.fromisoformat(d["started_at"]) for d in some_events_data["events"]]
    assert _is_descending_order(dts)
