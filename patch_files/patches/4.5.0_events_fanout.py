#!/opt/manager/env/bin/python

import os
import subprocess
import argparse

from cloudify import amqp_client
from manager_rest.amqp_manager import RabbitMQClient


def log(msg):
    print msg


def delete_exchange(host, user, password, vhost, cert_path):
    client = amqp_client.get_client(amqp_host=host,
                                    amqp_user=user,
                                    amqp_port=5671,
                                    amqp_pass=password,
                                    amqp_vhost=vhost,
                                    ssl_enabled=True,
                                    ssl_cert_path=cert_path)
    client.connect()
    with client.channel() as channel:
        channel.exchange_delete('cloudify-events')


def get_vhost_list(host, user, password, cert_path):
    rabbitmq_client = RabbitMQClient(host, user, password,
                                     verify=cert_path)
    vhosts_list = rabbitmq_client.get_vhost_names()
    return vhosts_list


def delete_all_exchanges(host, user, password, cert_path):
    for vhost in get_vhost_list(host, user, password, cert_path):
        log('Deleting exchange from vhost {0}'.format(vhost))
        delete_exchange(host, user, password, vhost, cert_path)
        log('Exchange from vhost {0} deleted'.format(vhost))


def replace_str_in_file(filepath, str1, str2):
    log('Replacing stuff in file {0}'.format(filepath))
    if not os.path.isfile(filepath):
        log('File {0} was not found'.format(filepath))
        return

    previous_chmod = subprocess.check_output(
        ['sudo', 'stat', '--printf=%a', filepath])
    subprocess.call(['sudo', 'chmod', '666', filepath])
    with open(filepath, 'r') as f:
        s = f.read()
    with open(filepath, 'w') as f:
        s = s.replace(str1, str2)
        f.write(s)
    subprocess.call(['sudo', 'chmod', previous_chmod, filepath])
    log('File {0} updated'.format(filepath))


def restart_service(service_name):
    log('Restarting service {0}'.format(service_name))
    subprocess.call(['sudo', 'systemctl', 'restart', service_name])


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description=(
        '4.5.0 make events queue as fanout type'))

    parser.add_argument('-u', '--username',
                        required=False,
                        default='cloudify',
                        help='rabbitmq username')

    parser.add_argument('-p', '--password',
                        required=False,
                        default='c10udify',
                        help='rabbitmq password')

    parser.add_argument('-i', '--ip',
                        required=False,
                        default='localhost',
                        help='rabbitmq host ip')

    parser.add_argument('-c', '--cert_path',
                        required=False,
                        default='/etc/cloudify/ssl/cloudify_internal_ca_cert.pem',
                        help='path to rabbitmq cert')

    args = parser.parse_args()

    delete_all_exchanges(args.ip, args.username, args.password, args.cert_path)

    replace_str_in_file('/etc/cloudify/rabbitmq/definitions.json', 'cloudify-events', 'cloudify-events-topic')

    replace_str_in_file('/etc/riemann/conf.d/manager.config', 'cloudify-events', 'cloudify-events-topic')

    replace_str_in_file('/opt/cfy/embedded/lib/python2.7/site-packages/cloudify/constants.py', 'cloudify-events', 'cloudify-events-topic')
    replace_str_in_file('/opt/mgmtworker/env/lib/python2.7/site-packages/cloudify/constants.py', 'cloudify-events', 'cloudify-events-topic')
    replace_str_in_file('/opt/manager/env/lib/python2.7/site-packages/cloudify/constants.py', 'cloudify-events', 'cloudify-events-topic')

    restart_service('cloudify-restservice')
    restart_service('cloudify-mgmtworker')
    restart_service('cloudify-amqp-postgres')
