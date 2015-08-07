myService = {
    "name": "myService",
    "image": "backend:latest",
    "command": "java -jar /tmp/backend.jar",
    "environment": {
        "SERVICE_NAME": "myService",
        "SERVICE_TAGS": "myTag",
        "SERVICE_8081_IGNORE": 1,
        "SERVICE_8080_CHECK_CMD": "/tmp/health-check.sh",
        "SERVICE_8080_CHECK_INTERVAL": "15s"
    },
    "ports": ['8080']
}
