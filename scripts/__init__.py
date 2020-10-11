import time

from bson import ObjectId

from app.models import (RESOURCE_FIELDS, ResourceField as ResourceFieldModel,
                        ResourceGraph as ResourceGraphModel)


def _init_resource_fields() -> None:
    print('Seeding ResourceFields...')
    start = time.time()

    for resource in RESOURCE_FIELDS:
        resource_id, resource_name, resource_type = resource

        if not ResourceFieldModel.objects(name=resource_name):
            resource_field = ResourceFieldModel()
            resource_field.id = ObjectId(resource_id)
            resource_field.name = resource_name
            resource_field.type = resource_type
            resource_field.save()

    exec_time = round((time.time() - start), 2)
    print('Seeded ResourceFields ( %s seconds)' % exec_time)


def _init_resource_graphs() -> None:
    print('Seeding ResourceGraph...')
    start = time.time()

    if not ResourceGraphModel.objects(name='pie'):
        data = {
            'name': 'pie',
            'graph': {'color': '#000099'}
        }
        resource_graph = ResourceGraphModel(**data)
        resource_graph.save()

    exec_time = round((time.time() - start), 2)
    print('Seeded ResourceGraph ( %s seconds)' % exec_time)


def init_db() -> None:
    _init_resource_fields()
    _init_resource_graphs()
