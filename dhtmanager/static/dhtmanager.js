var devtable = document.querySelector('#devices');
var devices = {};

var update_table = function(data, xhr) {
    // mark all devices as unseen
    for (var devid in devices) {
        devices[devid].seen = false;
    }

    // update existing rows or add new rows
    for (i=0; i < data.length; i++) {
        var row;

        device = data[i]
        devid = device.id

        // mark devices seen as we find them.
        if (! devices[devid]) {
            devices[devid] = {}
        }
        devices[devid].seen = true;

        // add devices that aren't already in the table.
        row = devtable.querySelector('#device_' + devid);
        if (!row) {
            row = document.createElement('tr')
            row.id = 'device_' + devid;
            for (attr in data[i]) {
                cell = document.createElement('td');
                row.appendChild(cell);
            }
            devtable.appendChild(row);
        }

        row.cells[0].innerHTML = device.id
        row.cells[1].innerHTML = device.address
        row.cells[2].innerHTML = device.last_seen_interval.toFixed(0)
        row.cells[3].innerHTML = device.ota_mode
        row.cells[3].setAttribute('class', 'toggleota');
    }

    // look for deleted devices
    for (var devid in devices) {
        if (! devices[devid].seen) {
            delete devices[devid];
            row = devtable.querySelector('#device_' + devid);
            row.parentNode.removeChild(row);
        }
    }
};

// called 1/sec in get information about devices from the
// database.
var get_device_status = function() {
    atomic.ajax({url: '/device'})
        .success(update_table);
};

var flash = function(e, times) {
    var colors = ['#ffffff', '#ffff00'];
    color = colors[times % colors.length];
    e.style['background-color'] = color;
    if (times === 0) return;
    setTimeout(function () {flash(e, times - 1);}, 500);
}

// when someone clicks on the ota mode field, send a request to toggle
// the value in the database and and flash the row in order to provide
// feedback.
var handle_table_click = function(e) {
    if (e.srcElement.className == 'toggleota') {
        devid = e.srcElement.parentNode.id.slice(7);
        atomic.ajax({url: '/device/' + devid + '/ota_mode/toggle'})
            .success(function (data, xhr) {
                flash(e.srcElement.parentNode, 2);
            });
    }
}

if (devtable) {
    document.addEventListener('click', handle_table_click);
    var update_interval = setInterval(get_device_status, 1000);
}
