"""Update pyproject.toml version based on package.json version."""
import json
import time

import toml

from config import Config


def _get_files_data() -> dict:
    with open(f'{ROOT_DIRECTORY}/package.json') as fd:
        json_data = json.load(fd)

    with open(f'{ROOT_DIRECTORY}/pyproject.toml') as fd:
        toml_data = toml.load(fd)

    return {'json_data': json_data, 'toml_data': toml_data}


def _update_pyproject_file(json_data: dict, toml_data: dict) -> None:
    toml_data['tool']['poetry']['version'] = json_data['version']
    new_toml_data = toml.dumps(toml_data)

    with open(f'{ROOT_DIRECTORY}/pyproject.toml', 'w') as fd:
        fd.write(new_toml_data)


print('Updating pyproyect.toml version...')
start = time.time()

ROOT_DIRECTORY = Config.ROOT_DIRECTORY
_update_pyproject_file(**_get_files_data())

exec_time = round((time.time() - start), 2)
print(f'Updated pyproyect.toml version  ( {exec_time} seconds)')
