import requests
import arguing
import datalang
import os

configuration = datalang.loadFile('.gc')
credentials = configuration['credentials']

# Error
if len(arguing.argv) == 1:
    exit('Error: No arguments.')

elif arguing.check('upload') and not os.path.exists(arguing.get('upload')):
    exit(f'Error: The file "{arguing.get("upload")}" does not exists.')

# Main
def request(method, url, action, json=None):
    if method in ['get', 'delete']:
        response = requests.request(
            method=method,
            url=url,
            auth=(credentials['username'], credentials['token'])
        )

    elif method in ['post', 'patch']:
        response = requests.request(
            method=method,
            url=url,
            json=json,
            auth=(credentials['username'], credentials['token'])
        )

    if response.status_code >= 400:
        exit(f'Failed to {action}')

    return response

if arguing.check('login'):
    configuration['credentials']['username'] = arguing.get('--username')
    configuration['credentials']['token'] = arguing.get('--token')

    datalang.dumpFile('.gc', configuration)

elif arguing.check('list'):
    if arguing.get('list') == None:
        action = 'list current user Gists.'
        url = 'https://api.github.com/gists'

    else:
        action = 'list {arguing.get("list")} Gists.\n'
        url = f'https://api.github.com/users/{arguing.get("list")}/gists'

    response = request('get', url, action)

    for gist in response.json():
        if len(gist['files']) > 0:
            gistTitle = list(gist['files'].keys())[0]

            print(f'[+] Title: {gistTitle} ({gist["id"]}).')

            for file in gist['files']:
                print(f'- {file} ({gist["files"][file]["language"]}).')

        print()

elif arguing.check('download'):
    response = request(
        'get',
        'https://api.github.com/gists/' + arguing.get('download'),
        f'download Gist "{arguing.get("download")}".'
    )

    if len(response.json()['files']) > 0:
        for file in response.json()['files']:
            get = requests.get(response.json()['files'][file]['raw_url']).text

            with open(file, 'a') as fileObject:
                fileObject.write(get)

            print(f'"{file}" has been downloaded.')

    else:
        print('No files.')

elif arguing.check('upload'):
    fileName = arguing.get('upload')
    description = f'{arguing.get("--description")} (gistCat 1.0.1)'

    if arguing.check('--private'):
        public = False

    else:
        public = True

    with open(fileName) as fileContent:
        fileContent = fileContent.read()

    response = request(
        'post',
        'https://api.github.com/gists',
        'upload Gist.',
        json={
            'description': description,
            'public': public,
            'files': {
                fileName: {
                    'content': fileContent
                }
            }
        },
    )

    print(f'File "{arguing.get("upload")}" has been uploaded with the ID {response.json()["id"]}.')

elif arguing.check('delete'):
    response = request(
        method='delete',
        url='https://api.github.com/gists/' + arguing.get('delete'),
        action=f'delete Gist {arguing.get("delete")}.'
    )

    print(f'Gist "{arguing.get("delete")}" has been deleted.')

elif arguing.check('update'):
    if not os.path.exists(arguing.get("--file")):
        exit('Cannot find the file "{arguing.get("--file")}".')

    else:
        with open(arguing.get('--file')) as fileContent:
            fileContent = fileContent.read()

        description = f'{arguing.get("--description")} (gistCat 0.0.1)'
        response = request(
            method='patch',
            url='https://api.github.com/gists/' + arguing.get('update'),
            action='update Gist.',
            json={
                'description': description,
                'files': {
                    arguing.get('--file'): {
                        'content': fileContent
                    }
                }
            },
        )

    print(f'Succesfuly updated Gist ({arguing.get("update")}).')

elif arguing.get('commits'):
    response = request(
        method='get',
        url=f'https://api.github.com/gists/{arguing.get("commits")}/commits',
        action='get commits from' + arguing.get('commits')
    ).json()

    for commit in response:
        print(f'From {commit["user"]["login"]} ({commit["version"]}).')
        print('- Commited at: ' + str(commit['committed_at']))
        print('- Added      : ' + str(commit['change_status']['additions']))
        print(f'- Deletions  : {commit["change_status"]["deletions"]}\n')