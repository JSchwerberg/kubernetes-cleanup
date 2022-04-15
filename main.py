from datetime import datetime, timedelta
from kubernetes import config, client
import os
import pytz

def main():
    threshold = os.getenv("THRESHOLD", "120")
    threshold_time = datetime.utcnow().replace(tzinfo=pytz.utc) - timedelta(minutes = int(threshold))

    config.load_config()
    api_instance = client.CoreV1Api()

    label_selector = os.getenv("LABEL_SELECTOR", "environment_type=cicd")
    namespaces = api_instance.list_namespace(label_selector = label_selector).to_dict()

    for namespace in namespaces["items"]:
        if namespace["metadata"]["creation_timestamp"] < threshold_time:
            print(f'''{namespace["metadata"]["name"]} is older than threshold. Deleting.
                  ({namespace["metadata"]["creation_timestamp"]})''')
            api_instance.delete_namespace(namespace["metadata"]["name"])
        else:
            print(f'{namespace["metadata"]["name"]} is still new!')

if __name__ == '__main__':
    main()
