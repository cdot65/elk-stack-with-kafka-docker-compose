from kafka import KafkaConsumer
import json
import requests
import re

def kafka_cleanup(each_message):
    host_ip = each_message.value['host']
    host_name = each_message.value['hostname']
    msg = each_message.value['router_message']
    return(host_ip, host_name, msg)


def send_request(host_ip, host_name, msg):
    try:
        url = 'https://dev85945.service-now.com/api/now/table/incident'
        headers = {"Content-Type":"application/json","Authorization":"Basic YWRtaW46YlpiWmZFQW45YjVQ","Accept":"application/json"}

        body = {
            "category": "network",
            "assigned_to": "0d9dcf322fcf1010ee4eea5ef699b6ba",
            "caller_id": "0d9dcf322fcf1010ee4eea5ef699b6ba",
            "comments": "BGP Down event was captured by ELK via SYSLOG",
            "work_notes": "SYSLOG MESSAGE:\n{}".format(msg),
            "urgency": 1,
            "description": "BGP neighborship has been lost on device {}".format(host_name),
            "incident_state": 1,
            "short_description": "BGP Down Event on device {}".format(host_name)
        }

        body = json.dumps(body)

        response = requests.post(url, headers=headers ,data=body)

        if response.status_code != 201: 
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
            exit()

        data = response.json()


    except requests.exceptions.RequestException:
        print('HTTP Request failed')


consumer = KafkaConsumer(
    'bgp_down',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    bootstrap_servers='192.168.105.80:9092'
    )


for each_message in consumer:
    host_ip, host_name, msg = kafka_cleanup(each_message)
    send_request(host_ip, host_name, msg)
