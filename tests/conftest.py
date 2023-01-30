import pytest
import time
from connpass_client import ConnpassClient, Writer


@pytest.fixture(scope="session")
def event_data():
    cli = ConnpassClient()
    data = cli.get(event_id="266898")
    yield data

    # TODO プリント文だとPytestに取られちゃうので修正
    print("waiting for 5 sec...")
    time.sleep(5)

