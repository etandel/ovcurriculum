import os
from graphviz import Digraph


def to_graph(base_fname, sections):
    dot = Digraph(format='pdf')

    # create nodes
    for section in sections:
        for course in section['courses']:
            if course['codigo'] != '******':
                name = '{codigo} - {nome}'.format(**course)
                dot.node(course['codigo'], name)

    # create edges
    for section in sections:
        for course in section['courses']:
            if course['codigo'] != '******':
                for requirement in course['requisitos'].split('&'):
                    requirement = requirement.strip()
                    if requirement:
                        dot.edge(requirement, course['codigo'])

    dot.render(base_fname)
    try:
        os.remove(base_fname)
    except FileNotFoundError:
        pass
