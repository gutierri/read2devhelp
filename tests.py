import io
import os
import pathlib
import shutil
import tempfile
import unittest
import xml.etree.ElementTree as ET
from unittest.mock import patch

import read2devhelp as read2dev


class MockRequest:
    def __init__(self, *args, **kwargs):
        pass

    def read(self):
        with io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     'mock/mock.html')) as mock_readme:
            body = mock_readme.read()
        return body.encode('utf-8')


class TestReadme2Devhelp(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = read2dev.DEVHELP_DIR = pathlib.Path(tempfile.mkdtemp())
        self.github_repos = 'https://github.com/axios/axios'
        self.mock_readme = MockRequest().read().decode('utf-8')
        self.index_expected = {'chapter': 'Axios',
                               'subs': [
                                   {'name': 'foo', 'link': 'index.html'},
                                   {'name': 'foobar', 'link': 'index.html'}
                               ]}

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)

    @patch('read2devhelp.urllib.request.urlopen', MockRequest)
    def test_repos_exists_readme(self):
        _, has_readme = read2dev.pull_readme(self.github_repos)
        self.assertTrue(has_readme)

    def test_readme_has_valid(self):
        has_valid_readme, _ = read2dev.extract_readme(self.mock_readme)

        self.assertTrue(has_valid_readme)

    def test_generate_index(self):
        index = read2dev.generate_index(self.mock_readme, self.github_repos)

        self.assertEqual('axios', index['chapter'])
        self.assertIn({'name': 'Features',
                       'link': 'index.html#user-content-features'},
                      index['subs'])
        self.assertIn({'name': 'Browser Support',
                       'link': 'index.html#user-content-browser-support'},
                      index['subs'])
        self.assertIs(3, len(index['subs']))

    def test_generate_xml(self):
        build_xml = read2dev.generate_xml(self.index_expected,
                                          self.github_repos)

        xml_generated = build_xml
        self.assertIn('<book', xml_generated)
        self.assertIn('<chapters', xml_generated)
        self.assertIn('<sub', xml_generated)

        xml_parsed = ET.fromstring(xml_generated)
        root = xml_parsed

        self.assertIn(('title', 'Axios'), root.attrib.items())
        self.assertIn(('link', 'index.html'), root.attrib.items())
        self.assertIn(('author', 'Unknown'), root.attrib.items())
        self.assertIn(('name', 'axios'), root.attrib.items())
        self.assertIn(('version', 'Unknown'), root.attrib.items())
        self.assertIn(('language', 'Unknown'), root.attrib.items())
        self.assertIn(('online', 'https://github.com/axios/axios'),
                      root.attrib.items())

    def test_index_xml(self):
        index = read2dev.generate_index(self.mock_readme, self.github_repos)
        build_xml = read2dev.generate_xml(index, self.github_repos)

        xml_generated = build_xml
        root = ET.fromstring(xml_generated)

        self.assertIn('chapters', root[0].tag)
        self.assertIs(len(root[0]), 3)
        self.assertCountEqual(['Features',
                               'index.html#user-content-features'],
                              root[0][0].attrib.values())
        self.assertCountEqual(['Browser Support',
                               'index.html#user-content-browser-support'],
                              root[0][1].attrib.values())
        self.assertCountEqual(['Chapter003',
                               'index.html#user-content-chapter003'],
                              root[0][2].attrib.values())

    @patch('read2devhelp.urllib.request.urlopen', MockRequest)
    def test_save_bundle_files_generate(self):
        read2dev.builder(self.github_repos)

        self.assertTrue(self.tmp_dir.joinpath('axios/').exists())
        self.assertTrue(self.tmp_dir.joinpath('axios/index.html').exists())
        self.assertTrue(self.tmp_dir.joinpath('axios/axios.devhelp2').exists())

        self.assertTrue(self.tmp_dir.joinpath('axios/index.html').stat()
                                    .st_size)
        self.assertTrue(self.tmp_dir.joinpath('axios/axios.devhelp2').stat()
                                    .st_size)


class TestCommandLine(unittest.TestCase):
    def setUp(self):
        self.command_line = read2dev.command_line_parse()

    def test_args_empty(self):
        with self.assertRaises(SystemExit):
            self.command_line.parse_args([])

    def test_args_repository_url(self):
        args = self.command_line.parse_args(['https://github.com/axios/axios'])
        self.assertEqual('https://github.com/axios/axios',
                         args.repository_url)
