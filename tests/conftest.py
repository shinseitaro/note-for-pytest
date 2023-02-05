import os
import pathlib
import time

import pytest
from connpass_client import ConnpassClient, Writer, io


# セッションごとに必ず５秒スリープ
@pytest.fixture(autouse=True, scope="session")
def sleep():
    print("auto sleep: waiting for 5 sec...\n")
    time.sleep(5)
    

@pytest.fixture(scope="session")
def an_event_data():
    # 上記でSleepしてるので不要
    # print("waiting for 5 sec...\n")
    # time.sleep(5)
    cli = ConnpassClient()
    data = cli.get(event_id="266898")
    yield data


@pytest.fixture(scope="session")
def some_events_data():
    cli = ConnpassClient()

    data = cli.get(event_id="273501,272790,271250,270289,269404,266898,264872",  order=2 )
    # io.Writer(data).to_csv("./some_events_data.csv")

    yield data
    # print("Deleting file... \n")
    # time.sleep(5)
    # os.remove("./some_events_data.csv")

@pytest.fixture()
def custom_event_data():

    def _custom_event_data(**params):
        cli = ConnpassClient()
        return cli.get(**params)

    return _custom_event_data

