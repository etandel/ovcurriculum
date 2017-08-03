import os
import sys
import unicodedata

from clint.textui import progress

from analyzer.exporting import to_csv
from analyzer.scraping import get_sections


OUTPUT_DIR = 'output'


CURRICULA = [
    ('Astrofísica', '7613365E-92A4-F79F-6268-CA7155B029B5'),
    ('Astronomia Computacional', '761658BA-92A4-F79F-6268-CA716A32D813'),
    ('Astronomia Instrumental', '7AC10A59-92A4-F79B-1E8E-D192798C6B4B'),
    ('Astronomia Matemática', '7A99D464-92A4-F79C-4BFC-2F8C1F81AE86'),
    ('Difusão Astronômica', '7AA1894A-92A4-F79C-4BFC-2F8C433EF3D5'),
]


def _slugfy(s):
    return (unicodedata.normalize('NFKD', s)
            .encode('ascii', 'ignore')
            .decode('ascii')
            .replace(' ', '_')
            .lower())


def export_curriculum(exports, name, code):
    sections = get_sections(code)

    base_name = os.path.join(OUTPUT_DIR, _slugfy(name))
    for export in exports:
        export(base_name, sections)


def to_graph(base_fname, sections):
    export_sections_to_graph(base_fname + '.png', sections)


def main():
    exports = []

    if '--csv' in sys.argv:
        exports.append(to_csv)

    if '--graph' in sys.argv:
        exports.append(to_graph)

    if exports:
        try:
            os.mkdir(OUTPUT_DIR)
        except FileExistsError:
            pass

        for name, code in progress.bar(CURRICULA):
            export_curriculum(exports, name, code)


if __name__ == '__main__':
    main()
