from io import BytesIO

import requests
from lxml.html import parse as parse_html


BASE_URL = 'https://siga.ufrj.br/sira/repositorio-curriculo/distribuicoes/{}.html'


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


def get_sections(curriculum_code):
    r = requests.get(BASE_URL.format(curriculum_code))
    r.raise_for_status()
    tree = parse_html(BytesIO(r.content))
    return list(map(build_section,
                    tree.xpath(TABLES_XPATH)[RELEVANT_SECTIONS]))

