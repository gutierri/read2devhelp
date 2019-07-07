#!/usr/bin/env python3

import argparse
import os
import re
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from xml.dom import minidom


DEVHELP_DIR = os.environ.get('README2DEVHELP_DIR')
if not DEVHELP_DIR:
    DEVHELP_DIR = Path().home() / '.local/share/devhelp/books'


def build_bundle(name):
    book_path = DEVHELP_DIR.joinpath(name)
    os.makedirs(book_path, exist_ok=True)
    print('Book folder -> {}'.format(book_path))

    index_path = book_path.joinpath('index.html')
    if not index_path.exists():
        print('Create file index.html -> {}'.format(index_path))
        open(index_path, 'a').close()

    devhelp2_path = book_path.joinpath('{}.devhelp2'.format(name))
    if not devhelp2_path.exists():
        print('Create file devhelp2 -> {}'.format(devhelp2_path))
        open(devhelp2_path, 'a').close()

    return (book_path, index_path, devhelp2_path)


def pull_readme(repository_url):
    resp = urllib.request.urlopen(repository_url).read()
    search_readme = re.search(r'id="readme"', resp.decode('utf-8'))
    data, valid = resp.decode('utf-8'), search_readme.group()
    return data, valid


def extract_readme(raw_body):
    body = re.search(r'<article.+<\/article>', raw_body.replace('\n', ''),
                     re.MULTILINE)
    valid_readme = re.search(r'<h1.+<\/h1>', body.group())
    return valid_readme, body.group()


def generate_index(raw_body, url_repository):
    headings = re.findall(r'<(h[1-2])>(.+?)</\1>', raw_body)
    index = {'subs': []}
    for (tag, content) in headings:
        content_clened = re.sub(r'<[^>]+>', '', content)
        if tag == 'h1':
            index['chapter'] = content_clened
        else:
            anchor_subchapter = re.search(r'<a id=".+?"', content).group()
            anchor_subchapter = re.search(r'"(.+)"',
                                          anchor_subchapter).groups()[0]
            link = 'index.html#{anchor}'.format(anchor=anchor_subchapter)
            index['subs'].append({'name': content_clened, 'link': link})
    else:
        if 'chapter' not in index:
            index['chapter'] = url_repository.split('/')[-1]

    return index


def generate_xml(index, url_repository):
    title = index['chapter']
    subs = index['subs']
    online = url_repository
    name = url_repository.split('/')[-1]

    attrs = {'xmlns': 'http://www.devhelp.net/book',
             'title': title,
             'link': 'index.html',
             'author': 'Unknown',
             'name': name,
             'version': 'Unknown',
             'language': 'Unknown',
             'online': online}
    root = ET.Element('book', attrib=attrs)
    chapters = ET.SubElement(root, 'chapters')

    for sub_attrs in subs:
        ET.SubElement(chapters, 'sub', sub_attrs)

    body_xml = ET.tostring(root).decode('utf-8')

    pretty_xml = minidom.parseString(body_xml)
    return pretty_xml.toprettyxml(indent="  ")


def builder(repo):
    get_readme, _ = pull_readme(repo)
    is_valid, raw_data = extract_readme(get_readme)
    (path_dir, path_index, path_devhelp2) = build_bundle(repo.split('/')[-1])
    chapters = generate_index(raw_data, repo)
    xml_generated = generate_xml(chapters, repo)

    with path_index.open('w') as readme_index_html:
        html_body = '''
        <!doctype html>
        <html lang="en">
        <head>
        <meta charset="utf-8">
        <meta name="viewport"
              content="width=device-width,
              initial-scale=1, shrink-to-fit=no">
        </head>
        <body>{}</body>
        </html>
        '''
        readme_index_html.write(html_body.format(raw_data))

    with path_devhelp2.open('w') as devhelp_xml:
        pretty_xml = minidom.parseString(xml_generated)
        devhelp_xml.write(pretty_xml.toprettyxml(indent="  "))


def command_line_parse():
    parser = argparse.ArgumentParser(
            description='Download and Convert README for DevHelp')
    parser.add_argument('repository_url', help='Repository home URL',
                        type=str)
    return parser


def main():
    command_args = command_line_parse().parse_args()
    builder(command_args.repository_url)


if __name__ == '__main__':
    main()
