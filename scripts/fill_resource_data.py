import json
import subprocess

import psutil

from app.models import (Resource as ResourceModel,
                        ResourceData as ResourceDataModel,
                        ResourceField as ResourceFieldModel,
                        ResourceGraph as ResourceGraphModel,
                        RESOURCE_FIELDS_BY_NAME)


def _get_cpu_data(resource_graph: ResourceGraphModel) -> list:
    return [
        {
            'resource_field': ResourceFieldModel.objects.get(
                id=RESOURCE_FIELDS_BY_NAME['CPU average usage']
            ),
            'resource_graph': resource_graph,
            'resource_value': str(psutil.cpu_percent()),
        },
        {
            'resource_field': ResourceFieldModel.objects.get(
                id=RESOURCE_FIELDS_BY_NAME['CPU average temperature']
            ),
            'resource_graph': resource_graph,
            'resource_value': str(psutil.sensors_temperatures()
                                  .get('cpu_thermal')[0].current),
        },
        {
            'resource_field': ResourceFieldModel.objects.get(
                id=RESOURCE_FIELDS_BY_NAME['per-CPU average usage']
            ),
            'resource_graph': resource_graph,
            'resource_value': str(psutil.cpu_percent(percpu=True)),
        },
    ]


def _get_gpu_data(resource_graph: ResourceGraphModel) -> list:
    # TODO: uncomment when Raspberry Foundtaion releases Raspberry OS 64 bits stable
    """
    return [
        {
            'resource_field': ResourceFieldModel.objects.get(
                id=RESOURCE_FIELDS_BY_NAME['GPU average temperature']
            ),
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

    tmp = [(p.pid, p.info['name'], p.info['memory_info'].rss / 1000000)
           for p in sorted(psutil.process_iter(['name', 'memory_info']),
                           key=lambda p: p.info['memory_info'].rss)
           ][-5:]
    tmp.reverse()

    return [
        {
            'resource_field': ResourceFieldModel.objects.get(
                id=RESOURCE_FIELDS_BY_NAME['RAM average usage']
            ),
            'resource_graph': resource_graph,
            'resource_value': str(mem.percent),
        },
        {
            'resource_field': ResourceFieldModel.objects.get(
                id=RESOURCE_FIELDS_BY_NAME['Top 5 RAM consuming processes']
            ),
            'resource_graph': resource_graph,
            'resource_value': str(tmp),
        },
        {
            'resource_field': ResourceFieldModel.objects.get(
                id=RESOURCE_FIELDS_BY_NAME['SWAP average usage']
            ),
            'resource_graph': resource_graph,
            'resource_value': str(swap.percent),
        },
    ]


def _get_system_data(resource_graph: ResourceGraphModel) -> list:
    cpu_info = json.loads(
        subprocess.run(['lscpu', '--json'], capture_output=True).stdout
    )
    cpu_fields = {'Architecture:', 'CPU(s):', 'Thread(s) per core:',
                  'Core(s) per socket:', 'Vendor ID:', 'Model name:',
                  'CPU max MHz:', 'CPU min MHz:'}

    cpu_info_data = [item for item in cpu_info.get('lscpu')
                     if item.get('field') in cpu_fields]

    return [
        {
            'resource_field': ResourceFieldModel.objects.get(
                id=RESOURCE_FIELDS_BY_NAME['Linux kernel version']
            ),
            'resource_graph': resource_graph,
            'resource_value': str(
                subprocess.run(['uname', '-r'],
                               capture_output=True).stdout.decode('utf-8')
                .replace('\n', '')
            ),
        },
        {
            'resource_field': ResourceFieldModel.objects.get(
                id=RESOURCE_FIELDS_BY_NAME['CPU model']
            ),
            'resource_graph': resource_graph,
            'resource_value': str(cpu_info_data),
        },
        {
            'resource_field': ResourceFieldModel.objects.get(
                id=RESOURCE_FIELDS_BY_NAME['MAC']
            ),
            'resource_graph': resource_graph,
            'resource_value': str(
                subprocess.run(['cat', '/sys/class/net/eth0/address'],
                               capture_output=True).stdout.decode('utf-8')
                .replace('\n', '')
            ),
        },
        {
            'resource_field': ResourceFieldModel.objects.get(
                id=RESOURCE_FIELDS_BY_NAME['Uptime server']
            ),
            'resource_graph': resource_graph,
            'resource_value': str(
                subprocess.run(['uptime', '-s'],
                               capture_output=True).stdout.decode('utf-8')
                .replace('\n', '')
            ),
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
            'resource_field': ResourceFieldModel.objects.get(
                id=RESOURCE_FIELDS_BY_NAME['Hard disk storage: /']
            ),
            'resource_graph': resource_graph,
            'resource_value': str(data),
        },
    ]


def _get_network_data(resource_graph: ResourceGraphModel) -> list:
    ps = subprocess.run(['vnstat', '--oneline'], capture_output=True)
    vnstat_data = ps.stdout.decode('utf-8').split(';')

    private_ip_command = ("ifconfig | "
                          "grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | "
                          "grep -Eo '([0-9]*\.){3}[0-9]*' | "
                          "grep -v '127.0.0.1'")
    ps = subprocess.Popen(private_ip_command, shell=True,
                          stdout=subprocess.PIPE)
    private_ip = ps.stdout.read().decode('utf-8').replace('\\n', '')
    public_ip = (subprocess.run(['curl', 'https://ipinfo.io/ip'],
                                capture_output=True)
                 .stdout.decode('utf-8').replace('\n', ''))

    return [
        {
            'resource_field': ResourceFieldModel.objects.get(
                id=RESOURCE_FIELDS_BY_NAME['Public IP']
            ),
            'resource_graph': resource_graph,
            'resource_value': public_ip,
        },
        {
            'resource_field': ResourceFieldModel.objects.get(
                id=RESOURCE_FIELDS_BY_NAME['Private IP']
            ),
            'resource_graph': resource_graph,
            'resource_value': str(private_ip).replace('\n', ''),
        },
        {
            'resource_field': ResourceFieldModel.objects.get(
                id=RESOURCE_FIELDS_BY_NAME['Download average traffic rate for today']
            ),
            'resource_graph': resource_graph,
            'resource_value': str(vnstat_data[6]),
        },
        {
            'resource_field': ResourceFieldModel.objects.get(
                id=RESOURCE_FIELDS_BY_NAME['Download packages total for day']
            ),
            'resource_graph': resource_graph,
            'resource_value': str(vnstat_data[3]),
        },
        {
            'resource_field': ResourceFieldModel.objects.get(
                id=RESOURCE_FIELDS_BY_NAME['Download packages total for month']
            ),
            'resource_graph': resource_graph,
            'resource_value': str(vnstat_data[8]),
        },
        {
            'resource_field': ResourceFieldModel.objects.get(
                id=RESOURCE_FIELDS_BY_NAME['Upload average traffic rate for today']
            ),
            'resource_graph': resource_graph,
            'resource_value': str(vnstat_data[11]),
        },
        {
            'resource_field': ResourceFieldModel.objects.get(
                id=RESOURCE_FIELDS_BY_NAME['Upload packages total for day']
            ),
            'resource_graph': resource_graph,
            'resource_value': str(vnstat_data[4]),
        },
        {
            'resource_field': ResourceFieldModel.objects.get(
                id=RESOURCE_FIELDS_BY_NAME['Upload packages total for month']
            ),
            'resource_graph': resource_graph,
            'resource_value': str(vnstat_data[9]),
        },
    ]


def fill_resource_data() -> None:
    resource_graph = ResourceGraphModel.objects[:1].first()

    resource_data_list = []
    data = (
        _get_cpu_data(resource_graph) +
        _get_gpu_data(resource_graph) +
        _get_memory_data(resource_graph) +
        _get_system_data(resource_graph) +
        _get_hard_disk_data(resource_graph) +
        _get_network_data(resource_graph)
    )

    for item in data:
        resource_data = ResourceDataModel(**item)
        resource_data_list.append(resource_data)

    resource = ResourceModel()
    resource.data = resource_data_list
    resource.save()
