from connpass_client import ConnpassClient, io
from pprint import pprint
import csv 

import pytest 

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

# 4. テストの目的からフィクスチャを書く
# 以下のテストは、フィクスチャを新規に作る必要が有ります。テストにあわせてフィクスチャを作り、テストを作成してください

# event_id="266898" を３回リクエストし、常に同じレスポンスであることを確認する
def test_no4_1(custom_event_data):
    from itertools import combinations

    data1 = custom_event_data(event_id = "266898")
    data2 = custom_event_data(event_id = "266898")
    data3 = custom_event_data(event_id = "266898")

    comb = combinations([data1, data2, data3], 2)


    assert all([x == y for [x, y] in comb])

# event_id="266898" のレスポンスをいったん CSV に書き出し、一行目が以下の一致すること。
# "event_id,title,catch,description,event_url,started_at,ended_at,limit,hash_tag,event_type,accepted,waiting,updated_at,owner_id,owner_nickname,owner_display_name,place,address,lat,lon,series"
def test_no4_2(an_event_data, tmp_path):
    fpath = tmp_path / "mycsv.csv"
    io.Writer(an_event_data).to_csv(fpath)

    with open(fpath, 'r') as file:
        first_line = file.readline().strip()
        assert first_line == "event_id,title,catch,description,event_url,started_at,ended_at,limit,hash_tag,event_type,accepted,waiting,updated_at,owner_id,owner_nickname,owner_display_name,place,address,lat,lon,series"

# 任意の event_id でリクエストして、常に同じレスポンスが返ってくること
# コンパスはユーザーがデータを入力するサービスなので、意図しない入力が機能を壊す恐れもあるかもしれない
# そこで任意のイベントIDは現時点で最も直近で入力されたイベントとして扱うことにしてみた。

def test_no4_3(custom_event_data):
    from itertools import combinations

    latest = custom_event_data(order=3)
    event_id = latest["events"][0]["event_id"]
    print("latest event id: ", event_id)

    data1 = custom_event_data(event_id = event_id)
    data2 = custom_event_data(event_id = event_id)

    assert data1 == data2


