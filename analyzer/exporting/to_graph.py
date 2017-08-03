import os
from graphviz import Digraph

from analyzer.utils import slugfy


def to_graph(base_fname, sections):
    dot = Digraph(format='pdf', comment=base_fname)
    dot.attr('node', shape='plaintext')

    available_courses = []

    # create nodes
    for section in sections:
        with dot.subgraph(name='cluster_' + slugfy(section['name'])) as sg:
            sg.attr(label=section['name'])
            sg.attr(pencolor='transparent')

            for course in section['courses']:
                if course['codigo'] != '******':
                    available_courses.append(course['codigo'])
                    name = '{codigo} - {nome}'.format(**course)
                    sg.node(course['codigo'], name)

    # create edges
    for section in sections:
        for course in section['courses']:
            if course['codigo'] != '******':
                for requirement in course['requisitos'].split():
                    requirement = requirement.strip()
                    if requirement and requirement in available_courses:
                        dot.edge(requirement, course['codigo'])

    dot.attr(pagedir='LT')
    dot.render(base_fname)
    try:
        os.remove(base_fname)
    except FileNotFoundError:
        pass
