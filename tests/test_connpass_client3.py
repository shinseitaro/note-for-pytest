import csv
from pprint import pprint

import pytest
from connpass_client import ConnpassClient, io

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

