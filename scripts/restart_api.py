from datetime import datetime

from kubernetes import client, config


def main():
    config.load_incluster_config()
    
    apps_api = client.AppsV1Api()
    apps_api.patch_namespaced_deployment("bertopic-api", "abb", body={
        "spec": {
            "template": {
                "metadata": {
                    "annotations": {
                        "kubectl.kubernetes.io/restartedAt": datetime.now().isoformat()
                    }
                }
            }
        }
    })


if __name__ == '__main__':
    main()