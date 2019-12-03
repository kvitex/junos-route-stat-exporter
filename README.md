# junos-routestat-exporter
Prometheus exporter for route tables statistics from JunOS devices.
Netconf ssh service on standart port(830) must be enabled on target device.

### Runnig exporter as a Flask application:

```
export FLASK_APP=junos-route-stat-exporter.py
export DEVICE_USER=username
export DEVICE_PASSWORD=password
/usr/bin/env python3 -m flask run --host=0.0.0.0 --port=8080
```

Usename and password should be defined in environment variables or in .env file:

### Running exporter in docker:
```
docker run -d -e DEVICE_USER=username -e DEVICE_PASSWORD=password\
  -p 8080:8080 --name junos-route-stat-exporter junos-route-stat-exporter
```

or

```
docker run --env-file .env -p 8080:8080 --name junos-route-stat-exporter junos-route-stat-exporter
```


