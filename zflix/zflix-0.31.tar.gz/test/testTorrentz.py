import sys

def test_search(torrentz, link, keyword):
    """
    Check if a torrentz search output a link according to the keywords.
    """
    res = {}
    torrentz.search_torrent("TPB AFK", res)
    for result in res[torrentz]:
        if result['link'] == link:
            return True

    return False


if __name__ == "__main__":
    sys.path.insert(0, '..')
    from src.trackers.torrentz import torrentz
    test = torrentz()
    ok = test_search(test,
                "https://torrentz.eu/7c337ab52faa3b68e67f9aa4fd0b5c703c63797f",
                "TPB AFK")
    print(ok)
