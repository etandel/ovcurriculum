import sys
import unicodedata
from csv import DictWriter
from io import BytesIO
from itertools import chain
from pprint import pprint

import requests
from lxml.html import parse as parse_html
from clint.textui import progress


BASE_URL = 'https://siga.ufrj.br/sira/repositorio-curriculo/distribuicoes/{}.html'


CURRICULA = [
    ('Astrofísica', '7613365E-92A4-F79F-6268-CA7155B029B5'),
    ('Astronomia Computacional', '761658BA-92A4-F79F-6268-CA716A32D813'),
    ('Astronomia Instrumental', '7AC10A59-92A4-F79B-1E8E-D192798C6B4B'),
    ('Astronomia Matemática', '7A99D464-92A4-F79C-4BFC-2F8C1F81AE86'),
    ('Difusão Astronômica', '7AA1894A-92A4-F79C-4BFC-2F8C433EF3D5'),
]


FIELDS = ['codigo', 'nome', 'creditos', 'carga_horaria_teorica',
          'carga_horaria_pratica', 'carga_horaria_extensao', 'requisitos']


RELEVANT_SECTIONS = slice(1, 9)
TABLES_XPATH = '//table[@class="lineBorder"]'
SECTION_NAME_XPATH = './/tr[@class="tableTitle"]//center//b/text()'


def _remove_empty(xs):
    return list(filter(None, xs))


def _normalize_reqs(raw_reqs):
    return raw_reqs.replace('(P)', '').replace(',', '&').strip()


def build_courses(table):
    fields = ['codigo', 'nome', 'creditos', 'carga_horaria_teorica',
              'carga_horaria_pratica', 'carga_horaria_extensao', 'requisitos']

    courses = []
    rows = table.xpath('.//tr')[1:-1]
    for row in rows:
        raw_course = row.xpath('(.//td/a|.//td)/text()')

        # filter empty lines
        if raw_course:
            # general suggestions
            if len(raw_course[0]) > 10:
                raw_course = ['******'] + raw_course

            course = dict(zip(fields, raw_course))
            course['requisitos'] = _normalize_reqs(course['requisitos'])
            courses.append(course)

    return courses


def build_section(table):
    return {
        'name': table.xpath(SECTION_NAME_XPATH)[0],
        'courses': build_courses(table),
    }


def _get_tree(area_code):
    r = requests.get(BASE_URL.format(area_code))
    r.raise_for_status()
    return parse_html(BytesIO(r.content))


def _slugfy(s):
    return (unicodedata.normalize('NFKD', s)
            .encode('ascii', 'ignore')
            .decode('ascii')
            .replace(' ', '_')
            .lower())


def export_curriculum(exports, name, code):
    tree = _get_tree(code)
    sections = list(map(build_section,
                        tree.xpath(TABLES_XPATH)[RELEVANT_SECTIONS]))

    for export in exports:
        export(_slugfy(name), sections)


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


def to_graph(base_fname, sections):
    export_sections_to_graph(base_fname + '.png', sections)


def main():
    exports = []

    if '--csv' in sys.argv:
        exports.append(to_csv)

    if '--graph' in sys.argv:
        exports.append(to_graph)

    if exports:
        for name, code in progress.bar(CURRICULA):
            export_curriculum(exports, name, code)


if __name__ == '__main__':
    main()
