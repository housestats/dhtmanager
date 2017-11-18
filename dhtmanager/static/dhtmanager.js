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

        devid = data[i].id

        // mark devices seen as we find them.
        if (! devices[devid]) {
            devices[devid] = {seen: true}
        } else {
            devices[devid].seen = true;
        }

        row = devtable.querySelector('#device_' + devid);
        if (!row) {
            devices[devid] = {seen: true};
            row = document.createElement('tr')
            row.setAttribute('id', 'device_' + devid);
            for (attr in data[i]) {
                cell = document.createElement('td');
                row.appendChild(cell);
            }
            devtable.appendChild(row);
        }

        row.cells[0].innerHTML = data[i].id
        row.cells[1].innerHTML = data[i].address
        row.cells[2].innerHTML = data[i].last_seen_interval.toFixed(0)
        row.cells[3].innerHTML = data[i].ota_mode
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

var handle_table_click = function(e) {
    if (e.srcElement.className == 'toggleota') {
        devid = e.srcElement.parentNode.id.slice(7);
        atomic.ajax({url: '/device/' + devid + '/ota/toggle'})
            .success(function (data, xhr) {
                flash(e.srcElement.parentNode, 2);
            });
    }
}

if (devtable) {
    document.addEventListener('click', handle_table_click);
    var update_interval = setInterval(get_device_status, 1000);
}
