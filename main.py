import os
from datetime import datetime
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from prometheus_client import start_http_server, Summary
from prometheus_client import Gauge

# Set env variables
argocd_api_endpoint = os.environ["ARGOCD_API_ENDPOINT"]
argocd_api_token = os.environ["ARGOCD_API_TOKEN"]

# Set prometheus variables
argocd_app_image_tag = Gauge('argocd_app_image_tag', 'image_tag', ['tag', 'app_name'])

headers = {"Authorization": "Bearer %s" %argocd_api_token}

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
apps_json = requests.get(url=argocd_api_endpoint+"/api/v1/applications"  , headers=headers, verify=False).json()

if __name__ == '__main__':
    start_http_server(8000)
    while True:
        for app in apps_json['items']:
            app_name = app['metadata']['name']
            app_url = argocd_api_endpoint+"/api/v1/applications/%s" % app_name
            images_json = requests.get(url=app_url , headers=headers, verify=False).json()
            app_images = images_json['status']['summary']['images'][0]
            app_deployed_at = images_json['status']['history']
            sorted_response = sorted(app_deployed_at, key=lambda x: x['id'], reverse=True)
            highest_deployedAt = sorted_response[0]['deployedAt']
            app_images_tag = app_images.split(':')
            dt = datetime.strptime(highest_deployedAt, "%Y-%m-%dT%H:%M:%SZ")
            current_time = datetime.now().timestamp()
            deployed_time = dt.timestamp()
            drift_time = int(current_time) - deployed_time
            argocd_app_image_tag.labels(tag=app_images_tag[1],app_name=app_name).set(drift_time)
    time.sleep(30)