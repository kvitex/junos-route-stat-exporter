#!/usr/bin/env python3
import xmltodict
import os
from lxml import etree
from jnpr.junos import Device
from dotenv import load_dotenv
from flask import Flask
from flask import request



load_dotenv()
user             = os.environ['DEVICE_USER']
password         = os.environ['DEVICE_PASSWORD']
metrics_name_prefix = os.environ.get('METRICS_NAME_PREFIX', 'junos_route_')

app = Flask(__name__)
@app.route('/metrics', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        hostname = request.form.get('hostname')
    else:
        hostname = request.args.get('hostname')
    if not hostname:
        return('Missing parameter: hostname')
    dev = Device(host=hostname, user=user, password=password, normalize=True)
    dev.open()
    rpc = dev.rpc.get_route_summary_information()
    rpc_xml = etree.tostring(rpc, pretty_print=True, encoding='unicode')
    dev.close()
    route_tables_data = xmltodict.parse(rpc_xml,force_list={'protocols'})['route-summary-information']['route-table']
    metrics = []
    for table in  route_tables_data:
        table_name = table['table-name']
        for pkey in table:
            if pkey.find('count') > -1:
                labels = [
                    ('table', f'"{table_name}"'),
                ]
                metrics.append({
                    'name': pkey.replace('-','_'),
                    'value': table[pkey],
                    'labels': labels
                 })
        protocols = table.get('protocols', [])
        for protocol in protocols:
            protocol_name = protocol['protocol-name']
            labels = [
                ('table', f'"{table_name}"'),
                ('protocol', f'"{protocol_name}"')
            ]
            for pkey in protocol:
                if pkey.find('count') > -1:
                    metrics.append({
                        'name': pkey.replace('-','_'),
                        'value': protocol[pkey],
                        'labels': labels
                     })
    output_list = []
    for metric in metrics:
        metric_name = metric['name']
        metric_value = metric['value']
        labels_string = ','.join(list(map(lambda st: '='.join(st), metric['labels'])))
        output_list.append(f'{metrics_name_prefix}{metric_name} {{{labels_string}}} {metric_value}')
    return '\n'.join(output_list)
