import subprocess

import psutil

from app.models import Resource as ResourceModel, ResourceData as ResourceDataModel, \
    ResourceGraph as ResourceGraphModel, RESOURCE_FIELDS_BY_NAME


def _get_cpu_data(resource_graph: ResourceGraphModel) -> list:
    top_five_processes = [(p.pid, p.info['name'], sum(p.info['cpu_times'])) for p in
                          sorted(psutil.process_iter(['name', 'cpu_times']),
                                 key=lambda p: sum(p.info['cpu_times'][:2]))][-5:]
    top_five_processes.reverse()

    return [
        {
            'resource_name': RESOURCE_FIELDS_BY_NAME['CPU average usage'],
            'resource_type': 'float',
            'resource_graph': resource_graph,
            'resource_value': str(psutil.cpu_percent()),
        },
        {
            'resource_name': RESOURCE_FIELDS_BY_NAME['CPU average temperature'],
            'resource_type': 'float',
            'resource_graph': resource_graph,
            'resource_value': str(psutil.sensors_temperatures().get('cpu-thermal')[0].current),
        },
        {
            'resource_name': RESOURCE_FIELDS_BY_NAME['per-CPU average usage'],
            'resource_type': 'list',
            'resource_graph': resource_graph,
            'resource_value': str(psutil.cpu_percent(percpu=True)),
        },
        {
            'resource_name': RESOURCE_FIELDS_BY_NAME['Top 5 CPU consuming processes'],
            'resource_type': 'list',
            'resource_graph': resource_graph,
            'resource_value': str(top_five_processes),
        }
    ]


def _get_gpu_data(resource_graph: ResourceGraphModel) -> list:
    # TODO: uncomment when Raspberry Foundtaion releases Raspberry OS 64 bits stable
    """
    return [
        {
            'resource_name': RESOURCE_FIELDS_BY_NAME['GPU average temperature'],
            'resource_type': 'float',
            'resource_graph': resource_graph,
            'resource_value': str(subprocess.run(['/opt/vc/bin/vcgencmd', 'measure_temp'])),
        },
    ]
    """
    return []


def _get_memory_data(resource_graph: ResourceGraphModel) -> list:
    # RAM and SWAP
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()

    tmp = [
              (p.pid, p.info['name'], p.info['memory_info'].rss / 1000000)
              for p in sorted(
            psutil.process_iter(
                ['name', 'memory_info', 'cpu_times']
            ),
            key=lambda p: p.info['memory_info'].rss
        )
          ][-5:]
    tmp.reverse()

    return [
        {
            'resource_name': RESOURCE_FIELDS_BY_NAME['RAM average usage'],
            'resource_type': 'float',
            'resource_graph': resource_graph,
            'resource_value': str(mem.percent),
        },
        {
            'resource_name': RESOURCE_FIELDS_BY_NAME['Top 5 RAM consuming processes'],
            'resource_type': 'list',
            'resource_graph': resource_graph,
            'resource_value': str(tmp),
        },
        {
            'resource_name': RESOURCE_FIELDS_BY_NAME['SWAP average usage'],
            'resource_type': 'float',
            'resource_graph': resource_graph,
            'resource_value': str(swap.percent),
        },
    ]


def _get_system_data(resource_graph: ResourceGraphModel) -> list:
    # uname -r
    # lscpu
    # cat /sys/class/net/eth0/address
    # uptime -s
    # uptime -p
    # TODO: Weather API
    return [
        {
            'resource_name': RESOURCE_FIELDS_BY_NAME['Linux kernel version'],
            'resource_type': 'str',
            'resource_graph': resource_graph,
            'resource_value': str(subprocess.run(['uname', '-r'], capture_output=True).stdout.decode('utf-8')),
        },
        {
            'resource_name': RESOURCE_FIELDS_BY_NAME['CPU model'],
            'resource_type': 'str',
            'resource_graph': resource_graph,
            'resource_value': str(subprocess.run(['lscpu'], capture_output=True).stdout.decode('utf-8')),
        },
        {
            'resource_name': RESOURCE_FIELDS_BY_NAME['MAC'],
            'resource_type': 'str',
            'resource_graph': resource_graph,
            'resource_value': str(subprocess.run(['cat', '/sys/class/net/eth0/address'],
                                                 capture_output=True).stdout.decode('utf-8')),
        },
        {
            'resource_name': RESOURCE_FIELDS_BY_NAME['Uptime server'],
            'resource_type': 'str',
            'resource_graph': resource_graph,
            'resource_value': str(subprocess.run(['uptime', '-s'], capture_output=True).stdout.decode('utf-8')),
        },
    ]


def _get_hard_disk_data(resource_graph: ResourceGraphModel) -> list:
    hd_data = psutil.disk_usage('/')
    data = {
        'total': hd_data.total,
        'used': hd_data.used,
        'free': hd_data.free,
        'percent': hd_data.percent,
    }

    return [
        {
            'resource_name': RESOURCE_FIELDS_BY_NAME['Hard disk storage: /'],
            'resource_type': 'dict',
            'resource_graph': resource_graph,
            'resource_value': str(data),
        },
    ]


def _get_network_data(resource_graph: ResourceGraphModel) -> list:
    ps = subprocess.run(['vnstat', '--oneline'], capture_output=True)
    vnstat_data = ps.stdout.decode('utf-8').split(';')

    private_ip_command = "ifconfig | " \
                         "grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | " \
                         "grep -Eo '([0-9]*\.){3}[0-9]*' | " \
                         "grep -v '127.0.0.1'"
    ps = subprocess.Popen(private_ip_command, shell=True, stdout=subprocess.PIPE)
    private_ip = ps.stdout.read().decode('utf-8').replace('\\n', '')

    return [
        {
            'resource_name': RESOURCE_FIELDS_BY_NAME['Public IP'],
            'resource_type': 'str',
            'resource_graph': resource_graph,
            'resource_value': subprocess.run(['curl', 'https://ipinfo.io/ip'], capture_output=True).stdout.decode(
                'utf-8'),
        },
        {
            'resource_name': RESOURCE_FIELDS_BY_NAME['Private IP'],
            'resource_type': 'str',
            'resource_graph': resource_graph,
            'resource_value': str(private_ip),
        },
        {
            'resource_name': RESOURCE_FIELDS_BY_NAME['Download average traffic rate for today'],
            'resource_type': 'str',
            'resource_graph': resource_graph,
            'resource_value': str(vnstat_data[6]),
        },
        {
            'resource_name': RESOURCE_FIELDS_BY_NAME['Download packages total for day'],
            'resource_type': 'str',
            'resource_graph': resource_graph,
            'resource_value': str(vnstat_data[3]),
        },
        {
            'resource_name': RESOURCE_FIELDS_BY_NAME['Download packages total for month'],
            'resource_type': 'str',
            'resource_graph': resource_graph,
            'resource_value': str(vnstat_data[8]),
        },
        {
            'resource_name': RESOURCE_FIELDS_BY_NAME['Upload average traffic rate for today'],
            'resource_type': 'str',
            'resource_graph': resource_graph,
            'resource_value': str(vnstat_data[11]),
        },
        {
            'resource_name': RESOURCE_FIELDS_BY_NAME['Upload packages total for day'],
            'resource_type': 'str',
            'resource_graph': resource_graph,
            'resource_value': str(vnstat_data[4]),
        },
        {
            'resource_name': RESOURCE_FIELDS_BY_NAME['Upload packages total for month'],
            'resource_type': 'str',
            'resource_graph': resource_graph,
            'resource_value': str(vnstat_data[9]),
        },
    ]


def init_collection_data() -> None:
    resource_graph = ResourceGraphModel.objects[:1].first()

    resource_data_list = []
    data = (_get_cpu_data(resource_graph) + _get_gpu_data(resource_graph) + _get_memory_data(resource_graph) +
            _get_system_data(resource_graph) + _get_hard_disk_data(resource_graph) + _get_network_data(resource_graph))

    for item in data:
        resource_data = ResourceDataModel(**item)
        resource_data_list.append(resource_data)

    resource = ResourceModel()
    resource.data = resource_data_list
    resource.save()
