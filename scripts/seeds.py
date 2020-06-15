import time

from app.models import ResourceGraph as ResourceGraphModel


def seed_resource_graph() -> None:
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
