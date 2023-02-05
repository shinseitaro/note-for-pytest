import pytest
import time
from connpass_client import ConnpassClient, Writer, io
import os
import pathlib


@pytest.fixture(scope="session")
def an_event_data():
    print("waiting for 5 sec...\n")
    time.sleep(5)

    cli = ConnpassClient()
    data = cli.get(event_id="266898")
    yield data


@pytest.fixture(scope="session")
def some_events_data():
    print("waiting for 5 sec...\n")
    time.sleep(5)
    cli = ConnpassClient()

    data = cli.get(event_id="273501,272790,271250,270289,269404,266898,264872")
    Writer(data).to_csv("./some_events_data.csv")

    yield data
    # print("Deleting file... \n")
    # time.sleep(5)
    # os.remove("./some_events_data.csv")


@pytest.fixture()
def custom_event_data():

    def _custom_event_data(**params):
        print("waiting for 5 sec... \n")
        time.sleep(5)

        cli = ConnpassClient()
        return cli.get(**params)

    return _custom_event_data

