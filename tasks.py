import os
import tempfile

import requests
from invoke import ctask as task

LABELS = ('Ready', 'In Progress')
PROJECTS = """
    jhermann/rituals
    jhermann/rudiments
    jhermann/gh-commander
    jhermann/thin-man
    jhermann/jmx4py
    jhermann/kunstkopf
    Springerle/py-generic-project
    Build-The-Web/bootils
"""
PROJECTS = [i.strip() for i in PROJECTS.splitlines() if i]
LABEL_MASTER_URL = 'https://raw.githubusercontent.com/jhermann/gh-commander/master/examples/labels.yaml'


@task
def markup(ctx):
    """Create status markup."""
    lines = [
        "Project | Status",
        "----: | :----",
    ]
    for project in PROJECTS:
        line = (
            "[{project}](https://github.com/{project}) |"
            " [![GitHub Issues](https://img.shields.io/github/issues/{project}.svg)](https://github.com/{project}/issues)"
            ).format(project=project)
        for label in LABELS:
            line += (
                " [![{name}](https://badge.waffle.io/{project}.png?label={label}&title={title})]"
                "(https://waffle.io/jhermann/stack-o-waffles)"
                ).format(
                    project=project,
                    name=label,
                    label=label.lower().replace(' ', '+'),
                    title=label.replace(' ', '+'),
                )
        lines.append(line)
    print('\n'.join(lines))


@task(name='sync-labels')
def sync_labels(ctx):
    """Sync labels into managed projects."""
    labels_yaml = requests.get(LABEL_MASTER_URL).text
    with tempfile.NamedTemporaryFile(suffix='.yaml', prefix='gh-label-sync-', delete=False) as handle:
        handle.write(labels_yaml)

    try:
        ctx.run('gh label import {} from {}'.format(' '.join(PROJECTS), handle.name))
    finally:
        os.remove(handle.name)
