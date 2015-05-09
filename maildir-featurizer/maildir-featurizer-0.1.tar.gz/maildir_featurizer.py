import pathlib, argparse, datetime

p = argparse.ArgumentParser(description = 'Get simple email features very quickly.')
p.add_argument('maildir', nargs = '+', help = 'Maildir(s) to look at')

def features(p):
    '''
    :param pathlib.Path p: An email file
    '''
    name = p.name.split(',')[0]
    rawdate, delivery_identifier, rawhostname = name.split('.')
    date = datetime.datetime.fromtimestamp(float(rawdate.replace('_', '.')))
    return {
    #   'name': name,
        'date': date,
        'delivery_identifier': delivery_identifier,
        'hostname': rawhostname,
        'size': p.stat().st_size,
    }

def messages(maildir):
    parent = pathlib.Path(maildir)
    for child in parent.iterdir():
        if child.is_file():
            pass
        elif child.name in {'new', 'cur', 'tmp'}:
            for grandchild in child.iterdir():
                if grandchild.is_file():
                    yield features(grandchild)
        else:
            yield from messages(child)

def cli():
    import sys, csv
    f = ['date', 'delivery_identifier', 'hostname', 'size']
    w = csv.DictWriter(sys.stdout, fieldnames = f)
    w.writeheader()
    for maildir in p.parse_args().maildir:
        for message in messages(maildir):
            w.writerow(message)

if __name__ == '__main__':
    cli()
