"""
A command line utility to use Homer. Example usage:

> python homer_cmd.py --help

Above shows help. Following will display stats on the command line:

> python homer_cmd.py --name sdf --author dede --file_path=/correct/path/to/file.txt

"""
import os
import click
import docx2txt
from homer.analyzer import Article
from homer.cmdline_printer import ArticlePrinter
from homer.constants import DOCX_EXTENSION, TXT_EXTENSION

def create_txt_from_docx(file_path):
    filename, file_extension = os.path.splitext(file_path)
    if file_extension == DOCX_EXTENSION:
        text = docx2txt.process(file_path)
        with open(filename + TXT_EXTENSION, "w") as text_file:
            print(text, file=text_file)
        return os.path.abspath(filename + TXT_EXTENSION)
    else:
        return os.path.abspath(file_path)

@click.command()
@click.option('--name', help='Article name, can be an empty string.')
@click.option('--author', help='Author name, can be an empty string.')
@click.option('--file_path', required=True, type=click.Path(exists=True))
def homer_cmd(name, author, file_path):
    new_path = create_txt_from_docx(file_path)
    printer = ArticlePrinter(Article(name, author, open(new_path, mode='r', encoding='utf-8').read()))
    printer.print_article_stats()
    printer.print_paragraph_stats()


if __name__ == "__main__":
    homer_cmd()


