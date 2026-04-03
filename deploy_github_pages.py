import os
import base64
import json
import requests

TOKEN = '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'
owner = 'afkzhass'
repo = 'educational-platform'

headers = {
    'Authorization': f'token {TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

# 1. Проверить репозиторий
resp = requests.get(f'https://api.github.com/repos/{owner}/{repo}', headers=headers)
if resp.status_code == 404:
    print('Репозиторий не найден. Создайте его вручную на GitHub.')
    raise SystemExit(1)
elif resp.status_code == 200:
    print('Репозиторий найден, обновляем файлы.')
else:
    print('Ошибка при проверке репозитория:', resp.status_code, resp.text)
    raise SystemExit(1)

# 2. Получить blobs
files = {
    'index.html': open('index.html', 'rb').read(),
    'styles/main.css': open('styles/main.css', 'rb').read(),
    'scripts/app.js': open('scripts/app.js', 'rb').read()
}

blobs = {}
for path, data in files.items():
    payload = {'content': base64.b64encode(data).decode('ascii'), 'encoding': 'base64'}
    r = requests.post(f'https://api.github.com/repos/{owner}/{repo}/git/blobs', headers=headers, json=payload)
    r.raise_for_status()
    blobs[path] = r.json()['sha']
    print('Blob created:', path)

# 3. Создать дерево
tree_items = []
for path, sha in blobs.items():
    tree_items.append({'path': path, 'mode': '100644', 'type': 'blob', 'sha': sha})

r = requests.post(f'https://api.github.com/repos/{owner}/{repo}/git/trees', headers=headers, json={'tree': tree_items})
r.raise_for_status()
tree_sha = r.json()['sha']
print('Tree created', tree_sha)

# 4. Создать коммит
commit_message = 'Initial commit via script'
commit_data = {'message': commit_message, 'tree': tree_sha}
# пробуем получить текущую ссылку main
rref = requests.get(f'https://api.github.com/repos/{owner}/{repo}/git/ref/heads/main', headers=headers)
if rref.status_code == 200:
    # Есть ветка. возьмём sha и создадим commit с parent
    parent_sha = rref.json()['object']['sha']
    commit_data['parents'] = [parent_sha]

r = requests.post(f'https://api.github.com/repos/{owner}/{repo}/git/commits', headers=headers, json=commit_data)
r.raise_for_status()
commit_sha = r.json()['sha']
print('Commit created', commit_sha)

if rref.status_code == 404:
    # создаём refs
    r = requests.post(f'https://api.github.com/repos/{owner}/{repo}/git/refs', headers=headers, json={'ref':'refs/heads/main','sha':commit_sha})
    r.raise_for_status()
    print('Branch main создан')
else:
    r = requests.patch(f'https://api.github.com/repos/{owner}/{repo}/git/refs/heads/main', headers=headers, json={'sha': commit_sha})
    r.raise_for_status()
    print('Branch main обновлён')

# 5. Настроить GitHub Pages
r = requests.post(f'https://api.github.com/repos/{owner}/{repo}/pages', headers=headers, json={'source': {'branch': 'main', 'path': '/'}})
if r.status_code in (201, 202):
    print('GitHub Pages включен')
elif r.status_code == 422:
    print('Pages уже включён или история не готова (это нормально).')
else:
    print('Ошибка Pages:', r.status_code, r.text)

url = f'https://{owner}.github.io/{repo}/'
print('Готово! Сайт должен стать доступен по URL (как только Pages развернётся):', url)
print('Проверка статуса: https://api.github.com/repos/{owner}/{repo}/pages')
