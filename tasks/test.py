from invoke import task


@task
def pytest(ctx):
    ctx.run('pytest', pty=True)


@task
def flake8(ctx):
    ctx.run('flake8 .', pty=True)


@task(default=True)
def all(ctx):
    pytest(ctx)
    flake8(ctx)
