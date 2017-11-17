import datetime
import flask
import os

from pony import orm

from dhtmanager import model


class defaults:
    DB_HOST = 'localhost'
    DB_NAME = 'devices'


def create_app():
    app = flask.Flask(__name__)
    app.config.from_object(defaults)
    if 'DHTMANAGER_SETTINGS' in os.environ:
        app.config.from_envvar('DHTMANAGER_SETTINGS')

    model.bind(host=app.config['DB_HOST'],
               user=app.config['DB_USER'],
               password=app.config['DB_PASS'],
               database=app.config['DB_NAME'])

    return app

app = create_app()


@app.route('/ota/<id>')
@model.db_session
def get_ota_status(id):
    try:
        device = model.Device[id]
        device.last_seen = datetime.datetime.utcnow()
    except orm.ObjectNotFound:
        device = model.Device(
            id=id,
            ota_mode=False)

    device.address = flask.request.remote_addr

    return flask.jsonify(device.to_dict())


@app.route('/ota/<id>', methods=['POST'])
@model.db_session
def set_ota_status(id):
    try:
        device = model.Device[id]
    except orm.ObjectNotFound:
        device = model.Device(
            id=id,
            ota_mode=False)

    ota_mode = (flask.request.form.get('ota_mode', 'false').lower()
                in ['true', '1', 'yes'])
    device.ota_mode = ota_mode

    return flask.jsonify(device.to_dict())


@app.route('/ota/<id>/toggle')
@model.db_session
def toggle_ota_status(id):
    try:
        device = model.Device[id]
    except orm.ObjectNotFound:
        flask.abort(404)

    device.ota_mode = not device.ota_mode

    return flask.jsonify(device.to_dict())


@app.route('/')
@model.db_session
def index():
    devices = orm.select(d for d in model.Device)
    return flask.render_template('devices.html',
                                 devices=sorted(devices, key=lambda d: d.id))


@app.route('/device')
@model.db_session
def list_devices():
    devices = orm.select(d for d in model.Device)
    return flask.jsonify([device.to_dict() for device in devices])


@app.route('/device/<id>')
@model.db_session
def get_device_info(id):
    try:
        device = model.Device[id]
    except orm.ObjectNotFound:
        flask.abort(404)

    return flask.jsonify(device.to_dict())
