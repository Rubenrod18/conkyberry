import subprocess

import psutil

from app.models import Resource as ResourceModel, ResourceData as ResourceDataModel


def _get_cpu_data() -> list:
    top_five_processes = [(p.pid, p.info['name'], sum(p.info['cpu_times'])) for p in
                          sorted(psutil.process_iter(['name', 'cpu_times']),
                                 key=lambda p: sum(p.info['cpu_times'][:2]))][-5:]
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
            'resource_value': str(psutil.sensors_temperatures().get('cpu-thermal')[0].current),
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


def _get_gpu_data() -> list:
    """
    return [
        {
            'resource_name': 'GPU average temperature',
            'resource_type': 'float',
            'resource_graph': {'type': 'pie', 'color': '#000099'},
            'resource_value': str(subprocess.run(['/opt/vc/bin/vcgencmd', 'measure_temp'])),
        },
    ]
    """
    return []


def _get_memory_data() -> list:
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
            'resource_name': 'RAM average usage',
            'resource_type': 'float',
            'resource_graph': {'type': 'pie', 'color': '#000099'},
            'resource_value': str(mem.percent),
        },
        {
            'resource_name': 'Top 5 RAM consuming processes',
            'resource_type': 'float',
            'resource_graph': {'type': 'pie', 'color': '#000099'},
            'resource_value': str(tmp),
        },
        {
            'resource_name': 'SWAP average usage',
            'resource_type': 'float',
            'resource_graph': {'type': 'pie', 'color': '#000099'},
            'resource_value': str(swap.percent),
        },
    ]


def _get_system_data() -> list:
    # uname -r
    # lscpu
    # cat /sys/class/net/eth0/address
    # uptime -s
    # uptime -p
    # TODO: Weather API
    return [
        {
            'resource_name': 'Linux kernel version',
            'resource_type': 'str',
            'resource_graph': {'type': 'pie', 'color': '#000099'},
            'resource_value': str(subprocess.run(['uname', '-r'])),
        },
        {
            'resource_name': 'CPU model',
            'resource_type': 'str',
            'resource_graph': {'type': 'pie', 'color': '#000099'},
            'resource_value': str(subprocess.run(['lscpu'])),
        },
        {
            'resource_name': 'MAC',
            'resource_type': 'str',
            'resource_graph': {'type': 'pie', 'color': '#000099'},
            'resource_value': str(subprocess.run(['cat', '/sys/class/net/eth0/address'])),
        },
        {
            'resource_name': 'Uptime server',
            'resource_type': 'str',
            'resource_graph': {'type': 'pie', 'color': '#000099'},
            'resource_value': str(subprocess.run(['uptime', '-s'])),
        },
    ]


def _get_hard_disk_data() -> list:
    return [
        {
            'resource_name': 'Hard disk storage: /',
            'resource_type': 'str',
            'resource_graph': {'type': 'pie', 'color': '#000099'},
            'resource_value': str(psutil.disk_usage('/')),
        },
    ]


def _get_network_data() -> list:
    data = subprocess.run(['vnstat --oneline'])
    data = data.split(';')

    private_ip_command = "ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'"
    ps = subprocess.Popen(private_ip_command, shell=True, stdout=subprocess.PIPE)
    private_ip = ps.read().decode('utf-8').replace('\\n','')

    return [
        {
            'resource_name': 'Public IP',
            'resource_type': 'str',
            'resource_graph': {'type': 'pie', 'color': '#000099'},
            'resource_value': subprocess.run(['curl', 'https://ipinfo.io/ip']).stdout.decode('utf-8'),
        },
        {
            'resource_name': 'Private IP',
            'resource_type': 'str',
            'resource_graph': {'type': 'pie', 'color': '#000099'},
            'resource_value': str(private_ip),
        },
        {
            'resource_name': 'Upload Kb/s',
            'resource_type': 'str',
            'resource_graph': {'type': 'pie', 'color': '#000099'},
            'resource_value': str(data[6]),
        },
        {
            'resource_name': 'Upload Kb/s at day',
            'resource_type': 'str',
            'resource_graph': {'type': 'pie', 'color': '#000099'},
            'resource_value': str(data[3]),
        },
        {
            'resource_name': 'Upload Kb/s at month',
            'resource_type': 'str',
            'resource_graph': {'type': 'pie', 'color': '#000099'},
            'resource_value': str(data[8]),
        },
        {
            'resource_name': 'Download Kb/s',
            'resource_type': 'str',
            'resource_graph': {'type': 'pie', 'color': '#000099'},
            'resource_value': str(data[11]),
        },
        {
            'resource_name': 'Download Kb/s at day',
            'resource_type': 'str',
            'resource_graph': {'type': 'pie', 'color': '#000099'},
            'resource_value': str(data[4]),
        },
        {
            'resource_name': 'Download Kb/s at month',
            'resource_type': 'str',
            'resource_graph': {'type': 'pie', 'color': '#000099'},
            'resource_value': str(data[9]),
        },
    ]


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
