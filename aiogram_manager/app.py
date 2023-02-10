import click


@click.group()
def cli():
    pass


@cli.command()
def startapp():
    print("startapp")


@cli.command()
def startproject():
    print("startproject")
