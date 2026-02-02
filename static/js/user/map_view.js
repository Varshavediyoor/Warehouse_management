document.addEventListener("DOMContentLoaded", function () {

    const map = L.map('deliveryMap', {
        zoomControl: false
    }).setView([12.9716, 77.5946], 11); // Bangalore example

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap'
    }).addTo(map);

    L.control.zoom({ position: 'bottomright' }).addTo(map);

    /* STATUS COLORS */
    const statusColors = {
        ontime: '#22c55e',
        risk: '#facc15',
        delayed: '#ef4444'
    };

    /* DELIVERY STAFF DATA (Sample – Replace with Live API) */
    const deliveries = [
        {
            name: "Ravi Kumar",
            status: "ontime",
            location: [12.9758, 77.6050],
            route: [
                [12.9716, 77.5946],
                [12.9758, 77.6050]
            ]
        },
        {
            name: "Amit Singh",
            status: "risk",
            location: [12.9352, 77.6245],
            route: [
                [12.9611, 77.6387],
                [12.9352, 77.6245]
            ]
        },
        {
            name: "Salman Ali",
            status: "delayed",
            location: [13.0050, 77.5700],
            route: [
                [12.9910, 77.5520],
                [13.0050, 77.5700]
            ]
        }
    ];

    deliveries.forEach(delivery => {

        /* MARKER */
        const marker = L.circleMarker(delivery.location, {
            radius: 8,
            color: statusColors[delivery.status],
            fillColor: statusColors[delivery.status],
            fillOpacity: 0.9
        }).addTo(map);

        marker.bindPopup(`
            <strong>${delivery.name}</strong><br>
            Status: <span style="color:${statusColors[delivery.status]}">
                ${delivery.status.toUpperCase()}
            </span>
        `);

        /* ROUTE LINE */
        L.polyline(delivery.route, {
            color: statusColors[delivery.status],
            weight: 4,
            opacity: 0.8,
            dashArray: delivery.status === 'delayed' ? '8 6' : null
        }).addTo(map);
    });
});
