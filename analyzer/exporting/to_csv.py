from itertools import chain
from csv import DictWriter

from analyzer.scraping import FIELDS


def _section2rows(section):
    return [{'section': section['name'], **course}
            for course in section['courses']]


def export_sections_to_csv(filename_or_object, sections):
    if isinstance(filename_or_object, str):
        f = open(filename_or_object, 'w', newline='')
        opened = True
    else:
        f = filename_or_object
        opened = False

    try:
        writer = DictWriter(f, ['section'] + FIELDS)
        writer.writeheader()
        writer.writerows(chain.from_iterable(map(_section2rows, sections)))
    except Exception:
        raise
    finally:
        if opened:
            f.close()


def to_csv(base_fname, sections):
    export_sections_to_csv(base_fname + '.csv', sections)
