import yaml


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


def make_publisher():
    publisher = {
        'publisher': {
            'build': './publisher',
            'container_name': 'mqtt_publisher',
            'environment': {
                'MQTT_BROKER_HOST': '172.28.0.2',
                'MQTT_BROKER_PORT': '1883',
                'MQTT_TOPIC': '172.28.2.1'
            },
            'depends_on': [
                'broker'
            ],
            'volumes': [
                './publisher/output/tcp_dump:/app/output/tcp_dump'
            ],
            'networks': {
                'mqtt_net': {
                    'ipv4_address': '172.28.1.1'
                }
            },
            'cap_add': [
                'NET_ADMIN',
                'NET_RAW'
            ]
        }
    }
    return publisher


def make_subscriber():
    subscriber = {
        'subscriber': {
            'build': './subscriber',
            'container_name': 'mqtt_subscriber',
            'environment': {
                'MQTT_BROKER_HOST': '172.28.0.2',
                'MQTT_BROKER_PORT': '1883',
                'MQTT_TOPIC': '172.28.2.1'
            },
            'depends_on': [
                'broker'
            ],
            'volumes': [
                './subscriber/output/latency_log:/app/output/latency_log',
                './subscriber/output/tcp_dump:/app/output/tcp_dump',
                './subscriber/output/debug:/app/output/debug'
            ],
            'networks': {
                'mqtt_net': {
                    'ipv4_address': '172.28.2.1'
                }
            },
            'cap_add': [
                'NET_ADMIN',
                'NET_RAW'
            ]
        }
    }
    return subscriber


def make_services():
    services = {}
    services.update(make_broker())
    services.update(make_publisher())
    services.update(make_subscriber())
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


def make_compose():
    compose = {
        'services': make_services(),
        'networks': make_network()
    }
    return compose


if __name__ == "__main__":
    compose_dict = make_compose()
    filename = 'docker-compose.with_cloud.yml'
    with open(filename, 'w') as f:
        yaml.dump(compose_dict, f, sort_keys=False)
    print(f"{filename} has been created.")
