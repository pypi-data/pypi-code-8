import reseasdk

def test_help(capsys):
    reseasdk.main(['help'])
    assert capsys.readouterr()[0].startswith('Usage: ')
    reseasdk.main([])
    assert capsys.readouterr()[0].startswith('Usage: ')
