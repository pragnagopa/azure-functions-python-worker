import pathlib
import subprocess
import sys

from azure.functions_worker import protos
from azure.functions_worker import testutils


class TestLoader(testutils.WebHostTestCase):

    @classmethod
    def get_script_dir(cls):
        return 'load_functions'

    def test_loader_simple(self):
        r = self.webhost.request('GET', 'simple')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.text, '__app__.simple.main')

    def test_loader_custom_entrypoint(self):
        r = self.webhost.request('GET', 'entrypoint')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.text, '__app__.entrypoint.main')

    def test_loader_subdir(self):
        r = self.webhost.request('GET', 'subdir')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.text, '__app__.subdir.sub.main')

    def test_loader_relimport(self):
        r = self.webhost.request('GET', 'relimport')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.text, '__app__.relimport.relative')


class TestPluginLoader(testutils.AsyncTestCase):

    async def test_entry_point_plugin(self):
        test_binding = pathlib.Path(__file__).parent / 'test-binding'
        subprocess.run([
            sys.executable, '-m', 'pip',
            '--disable-pip-version-check',
            'install', '--quiet',
            '-e', test_binding
        ], check=True)

        try:

            async with testutils.start_mockhost(
                    script_root='test-binding/functions') as host:
                func_id, r = await host.load_function('foo')

            self.assertEqual(r.response.function_id, func_id)
            self.assertEqual(r.response.result.status,
                             protos.StatusResult.Success)
        finally:
            subprocess.run([
                sys.executable, '-m', 'pip',
                '--disable-pip-version-check',
                'uninstall', '-y', '--quiet', 'foo-binding'
            ], check=True)
