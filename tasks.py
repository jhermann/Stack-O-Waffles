from invoke import ctask as task

LABELS = ('Ready', 'In Progress')
PROJECTS = """
    jhermann/rituals
    jhermann/rudiments
    jhermann/gh-commander
    jhermann/thin-man
    Springerle/py-generic-project
    Build-The-Web/bootils
"""
PROJECTS = [i.strip() for i in PROJECTS.splitlines() if i]

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
