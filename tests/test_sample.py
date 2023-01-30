from connpass_client import ConnpassClient
from pprint import pprint


def test_results():
    cli = ConnpassClient()
    event_id = "266898"
    data = cli.get(event_id=event_id)

    assert data["results_returned"] == 1


cli = ConnpassClient()
series_id = "5944"
data = cli.get(series_id=series_id)

# pprint(data.keys())
