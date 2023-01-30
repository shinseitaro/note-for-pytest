from connpass_client import ConnpassClient
from pprint import pprint


def test_results(event_data):
    # cli = ConnpassClient()
    # event_id = "266898"
    # data = cli.get(event_id=event_id)

    assert event_data["results_returned"] == 1

