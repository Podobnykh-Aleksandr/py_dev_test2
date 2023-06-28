import requests


class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}',
        }

    def create_folder(self, folder_name):
        host = "https://cloud-api.yandex.net/v1/disk/resources"
        params = {"path": 'netology/' + str(folder_name)}
        headers = self.get_headers()
        response = requests.get(host, headers=headers, params=params)
        if response.status_code == 404:
            response = requests.put(host, headers=headers, params=params)
        return response.status_code

    def upload(self, folder_name, photo):
        current_files_names = []
        host = "https://cloud-api.yandex.net/v1/disk/resources"
        params = {"path": 'netology/' + folder_name}
        headers = self.get_headers()
        response = requests.get(host, headers=headers, params=params)
        if response.status_code == 404:
            requests.put(host, headers=headers, params=params)
        else:
            for file in response.json()['_embedded']['items']:
                current_files_names.append(file['name'])
        if str(photo['likes']) + '.jpg' in current_files_names:
            params['path'] += "/" + str(photo['likes']) + photo['date'] + '.jpg'
        else:
            params['path'] += "/" + str(photo['likes']) + '.jpg'
        response = requests.post(host + '/upload', headers=headers, params={**params, 'url': photo['url']})
        return response.status_code
