import psutil

from app.models import Resource as ResourceModel, ResourceData as ResourceDataModel


def _get_cpu_data() -> list:
    top_five_processes = [(p.pid, p.info['name'], sum(p.info['cpu_times'])) for p in
           sorted(psutil.process_iter(['name', 'cpu_times']), key=lambda p: sum(p.info['cpu_times'][:2]))][-5:]
    top_five_processes.reverse()

    return [
        {
            'resource_name': 'CPU average usage',
            'resource_type': 'float',
            'resource_graph': {'type': 'pie', 'color': '#000099'},
            'resource_value': str(psutil.cpu_percent()),
        },
        {
            'resource_name': 'CPU average temperature',
            'resource_type': 'string',
            'resource_graph': {'type': 'pie', 'color': '#000099'},
            'resource_value': psutil.sensors_temperatures().get('cpu-thermal')[0].current,
        },
        {
            'resource_name': 'per-CPU average usage',
            'resource_type': 'list',
            'resource_graph': {'type': 'pie', 'color': '#000099'},
            'resource_value': str(psutil.cpu_percent(percpu=True)),
        },
        {
            'resource_name': 'Top 5 CPU consuming processes',
            'resource_type': 'tuple',
            'resource_graph': {'type': 'pie', 'color': '#000099'},
            'resource_value': str(top_five_processes),
        }
    ]


def _get_gpu_data() -> None:
    pass


def _get_memory_data() -> None:
    # RAM and SWAP
    pass


def _get_system_data() -> None:
    pass


def _get_hard_disk_data() -> None:
    pass


def _get_network_data() -> None:
    pass


def init_collection_data() -> None:
    resource_data_list = []
    data = (_get_cpu_data() + _get_gpu_data() + _get_memory_data() +
            _get_system_data() + _get_hard_disk_data() + _get_network_data())

    for item in data:
        resource_data = ResourceDataModel(**item)
        resource_data_list.append(resource_data)

    resource = ResourceModel()
    resource.data = resource_data_list
    resource.save()
