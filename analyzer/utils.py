import unicodedata


def slugfy(s):
    return (unicodedata.normalize('NFKD', s)
            .encode('ascii', 'ignore')
            .decode('ascii')
            .replace(' ', '_')
            .lower())
