## Device API

- `GET /device`

    Return a JSON list of devices.

      curl localhost:2112/device

- `PUT /device`

    Reads a JSON dictionary from the request and creates a new device.

      curl localhost:2112/device -XPUT \
        -H 'content-type: application/json' \
        -d '{"id": "testing", "ota_mode": false}'

- `GET /device/<id>`

    Return a JSON dictionary with information about the given sensor.

      curl localhost:2112/device/testing


- `DELETE /device/<id>`

    Delete a device.

      curl localhost:2112/device/testing -XDELETE

- `POST /device/<id>/ota`

    Update the value of `ota_mode` using the value of the `ota_mode`
    form parameter.  E.g.,

        curl http://localhost:2112/device/12345678/ota -d ota_mode=true
