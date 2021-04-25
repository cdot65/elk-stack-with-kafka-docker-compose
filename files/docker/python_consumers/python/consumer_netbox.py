from kafka import KafkaConsumer
import json
import requests
import re


def kafka_cleanup(each_message):
    device_info = dict()
    device_info['hostname'] = each_message.value['data']['name']
    device_info['rack'] = each_message.value['data']['rack']
    device_info['site'] = each_message.value['data']['site']
    device_info['tenant'] = each_message.value['data']['tenant']
    device_info['device_type'] = each_message.value['data']['device_type']
    device_info['primary_ip'] = each_message.value['data']['primary_ip']
    device_info['serial'] = each_message.value['data']['serial']
    device_info['device_role'] = each_message.value['data']['device_role']
    device_info['event'] = each_message.value['event']

    message_type = f':sparkles: *Netbox Device*: {device_info["event"]}\n'

    hostname = f':white_small_square: *Hostname*: {device_info["hostname"]}\n'
    site = f':white_small_square: *Site*: {device_info["site"]["name"]}\n'
    tenant = f':white_small_square: *Tenant*: {device_info["tenant"]["name"]}\n'
    device_type = f':white_small_square: *Device Type*: {device_info["device_type"]["display_name"]}\n'
    serial = f':white_small_square: *Serial*: {device_info["serial"]}\n'

    message = message_type + hostname + site + tenant + device_type + serial

    return(message)


def send_request(message):
    try:
        response = requests.request(
            "POST", 
            url = "https://hooks.slack.com/services/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",
            headers={"Content-Type": "application/json"},
            json={'text': f'{message}'}
        )

        print('Response HTTP Status Code: {status_code}'.format(
            status_code=response.status_code))
        print('Response HTTP Response Body: {content}'.format(
            content=response.content))
    except requests.exceptions.RequestException:
        print('HTTP Request failed')




consumer = KafkaConsumer('netbox', value_deserializer=lambda m: json.loads(m.decode('utf-8')), bootstrap_servers='192.168.105.80:9092')


for each_message in consumer:
    print(each_message)
    message = kafka_cleanup(each_message)
    send_request(message)
