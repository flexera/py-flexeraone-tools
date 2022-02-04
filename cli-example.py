#cli.py
import click
from .bar import make_bar

@click.group()
def foo():
    pass

make_bar(foo)
foo()


#bar.py
from .baz import make_baz

def make_bar(foo):
    @foo.group()
    def bar():
        pass

    make_baz(bar)

#baz.py

def make_baz(bar):
    @bar.command()
    def baz():
        print('baz')
