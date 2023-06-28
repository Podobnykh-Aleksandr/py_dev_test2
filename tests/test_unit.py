import unittest
import requests
from parameterized import parameterized
from yandexDisk import YaUploader

# Токен для входа
token = ''
# Заголовки для входа
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'OAuth {token}',
}

host = "https://cloud-api.yandex.net/v1/disk/resources"
params = {"path": 'netology'}

FIXTURE = [
    ('Папка2',),
    ('FolderXo',),
    (4,)
    ]


class TestYaDiskClass(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    @parameterized.expand(FIXTURE)
    def test_create_base_folder(self, folder_name):
        ya = YaUploader(token)
        status = ya.create_folder(folder_name)

        self.assertIn(status, [200, 201], msg='Problem with connecting to yandex disk')

        response = requests.get(host, headers=headers, params=params)
        self.assertEqual(response.status_code, 200, msg='The problem with connecting to Yadisk from test')

        folders_names = []
        for file in response.json()['_embedded']['items']:
            if file['type'] == 'dir':
                folders_names.append(file['name'])
        self.assertIn(str(folder_name), folders_names, msg='the folder is not in YaDisk')
