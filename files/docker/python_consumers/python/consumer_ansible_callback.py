from kafka import KafkaConsumer
from json import loads, dumps
import requests
import re

def kafka_cleanup(each_message):
    host_ip = each_message.value['host']
    host_name = each_message.value['hostname']
    msg = each_message.value['router_message']
    return(host_ip, host_name, msg)


def syslog_cleanup(msg):
    match = re.match(r"^\[(?P<junos_string>.*)]", msg)
    if match:
        junos_string = match.groupdict(['junos_string'])
        for k,v in junos_string.items():
            msg = v.split(" ")
            neighbor = msg[2]
            neighbor = neighbor.split("=")
            neighbor = neighbor[1].replace('"','')
            iface = msg[3]
            iface = iface.split("=")
            iface = iface[1].replace('"','')
        return(neighbor, iface)


def send_request(host_name, neighbor, iface):
    try:
        response = requests.post(
            url="http://10.255.127.47/api/v2/job_templates/12/launch/",
            headers={
                "Authorization": "Basic YXV0b21hdGlvbjpqdW5pcGVyMTIz",
                "Content-Type": "application/json; charset=utf-8",
            },
            data=dumps({
                "extra_vars": {
                    "iface": iface,
                    "host_name": host_name,
                    "neighbor": neighbor
                }
            })
        )
        print('Response HTTP Status Code: {status_code}'.format(
            status_code=response.status_code))
        print('Response HTTP Response Body: {content}'.format(
            content=response.content))
    except requests.exceptions.RequestException:
        print('HTTP Request failed')


consumer = KafkaConsumer(
    'ansible_callback',
    value_deserializer=lambda m: loads(m.decode('utf-8')),
    bootstrap_servers='192.168.105.80:9092'
    )


for each_message in consumer:
    # host_ip, host_name, msg = kafka_cleanup(each_message)
    # neighbor, iface = syslog_cleanup(msg)
    # send_request(host_name, neighbor, iface)
    print(each_message)
