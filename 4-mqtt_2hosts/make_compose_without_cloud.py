import yaml


def ip_suffix(ip: str) -> int:
    """IPアドレスの最後のオクテットを取得

    Args:
        ip (str): IPアドレス（例: '172.28.1.1'）

    Returns:
        int: 最後のオクテット
    """
    assert ip.count('.') == 3, "Invalid IP address format."
    return int(ip.split('.')[-1])


def make_broker():
    broker = {
        'broker': {
            'image': 'eclipse-mosquitto:2',
            'container_name': 'mqtt_broker',
            'ports': [
                "1883:1883"
            ],
            'volumes': [
                "./broker/mosquitto.conf:/mosquitto/config/mosquitto.conf",
                "./broker/data:/mosquitto/data",
                "./broker/log:/mosquitto/log"
            ],
            'networks': {
                'mqtt_net': {
                    'ipv4_address': '172.28.0.2'
                }
            }
        }
    }
    return broker


def make_publisher(own_ip: str, target_ip: str):
    """publisherのサービス定義

    Args:
        own_ip (str): publisherのIPアドレス（ex. 172.28.1.1）
        target_ip (str): subscriberのIPアドレス（ex. 172.28.2.1）

    Returns:
        dict: publisherのサービス定義
    """
    assert own_ip != target_ip, "own_ip and target_ip must be different."
    assert ip_suffix(own_ip) == ip_suffix(
        target_ip), "The last octet of own_ip and target_ip must be the same."
    n = ip_suffix(own_ip)
    broker_ip = target_ip
    publisher = {
        f'publisher_{n}': {
            'build': './publisher',
            'container_name': f'mqtt_publisher_{n}',
            'environment': {
                'MQTT_BROKER_HOST': broker_ip,
                'MQTT_BROKER_PORT': '1883',
                'MQTT_TOPIC': target_ip
            },
            'volumes': [
                './publisher/output/tcp_dump:/app/output/tcp_dump'
            ],
            'networks': {
                'mqtt_net': {
                    'ipv4_address': own_ip
                }
            },
            'cap_add': [
                'NET_ADMIN',
                'NET_RAW'
            ]
        }
    }
    return publisher


def make_subscriber(own_ip: str):
    """subscriberのサービス定義
    Args:
        own_ip (str): subscriberのIPアドレス（ex. 172.28.2.1）
    Returns:
        dict: subscriberのサービス定義
    """
    n = ip_suffix(own_ip)
    broker_ip = own_ip
    subscriber = {
        f'subscriber_{n}': {
            'build': './subscriber',
            'container_name': f'mqtt_subscriber_{n}',
            'environment': {
                'MQTT_BROKER_HOST': broker_ip,
                'MQTT_BROKER_PORT': '1883',
                'MQTT_TOPIC': own_ip,
                'VIA_CLOUD': False
            },
            'volumes': [
                './subscriber/output/latency_log:/app/output/latency_log',
                './subscriber/output/tcp_dump:/app/output/tcp_dump',
                './subscriber/output/debug:/app/output/debug'
            ],
            'networks': {
                'mqtt_net': {
                    'ipv4_address': own_ip
                }
            },
            'cap_add': [
                'NET_ADMIN',
                'NET_RAW'
            ]
        }
    }
    return subscriber


def make_services(num_container: int = 1):
    services = {}
    # services.update(make_broker())
    for i in range(num_container):
        _from = f'172.28.1.{i + 1}'
        _to = f'172.28.2.{i + 1}'
        services.update(make_publisher(
            _from, _to))
        services.update(make_subscriber(_to))
    return services


def make_network():
    network = {
        'mqtt_net': {
            'driver': 'bridge',
            'ipam': {
                'config': [
                    {
                        'subnet': '172.28.0.0/16',
                    }
                ]
            }
        }
    }
    return network


def make_compose(num_container: int = 1):
    compose = {
        'services': make_services(num_container),
        'networks': make_network()
    }
    return compose


if __name__ == "__main__":
    num_container = 50
    compose_dict = make_compose(num_container)
    filename = 'docker-compose.without_cloud.yml'
    with open(filename, 'w') as f:
        yaml.dump(compose_dict, f, sort_keys=False)
    print(f"{filename} has been created.")
