import requests
import base64
import os

TOKEN = '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'
owner = 'afkzhass'
repo = 'educational-platform'

headers = {
    'Authorization': f'token {TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

files_to_upload = [
    ('index.html', 'index.html'),
    ('styles/main.css', 'styles/main.css'),
    ('scripts/app.js', 'scripts/app.js'),
]

print('Загружаем файлы в репо...')
for file_path, path_in_repo in files_to_upload:
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
        
        encoded = base64.b64encode(content).decode('utf-8')
        
        url = f'https://api.github.com/repos/{owner}/{repo}/contents/{path_in_repo}'
        
        # Проверяем, есть ли уже такой файл
        get_resp = requests.get(url, headers=headers)
        if get_resp.status_code == 200:
            sha = get_resp.json()['sha']
            message = f'Update {path_in_repo}'
        else:
            sha = None
            message = f'Add {path_in_repo}'
        
        # Загружаем файл
        payload = {
            'message': message,
            'content': encoded,
        }
        if sha:
            payload['sha'] = sha
        
        r = requests.put(url, headers=headers, json=payload)
        if r.status_code in (201, 200):
            print(f'✓ {path_in_repo} загружен')
        else:
            print(f'✗ {path_in_repo} ошибка {r.status_code}: {r.text}')
    except Exception as e:
        print(f'✗ {file_path} ошибка: {e}')

# Включаем Pages
print('\nЭнабл Pages...')
r = requests.post(f'https://api.github.com/repos/{owner}/{repo}/pages', 
                   headers=headers, 
                   json={'source': {'branch': 'main', 'path': '/'}})
if r.status_code in (201, 202):
    print('✓ GitHub Pages включён')
elif r.status_code == 422:
    print('✓ Pages уже включён')
else:
    print(f'Pages статус: {r.status_code}')

url_final = f'https://{owner}.github.io/{repo}/'
print(f'\n✅ Готово! Сайт: {url_final}')
print('⏳ Pages может развернуться за 1-2 минуты.')
