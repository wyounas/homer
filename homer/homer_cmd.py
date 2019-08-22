"""
A command line utility to use Homer. Example usage:

> python homer_cmd.py --help

Above shows help. Following will display stats on the command line:

> python homer_cmd.py --name sdf --author dede --file_path=/correct/path/to/file.txt

"""
import os
import click
from homer.analyzer import Article
from homer.cmdline_printer import ArticlePrinter

@click.command()
@click.option('--name', help='Article name, can be an empty string.')
@click.option('--author', help='Author name, can be an empty string.')
@click.option('--file_path', required=True, type=click.Path(exists=True))
def homer_cmd(name, author, file_path):
    file_path = os.path.abspath(file_path)
    printer = ArticlePrinter(Article(name, author, open(file_path, mode='r', encoding='utf-8').read()))
    printer.print_article_stats()
    printer.print_paragraph_stats()


if __name__ == "__main__":
    homer_cmd()


