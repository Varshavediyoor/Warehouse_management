document.addEventListener("DOMContentLoaded", function () {

    const map = L.map('miniRouteMap').setView([12.9716, 77.5946], 12);
  
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
  
    const route = [
      [12.9716, 77.5946],
      [12.9755, 77.6020],
      [12.9820, 77.6100]
    ];
  
    // Optimized route line
    L.polyline(route, {
      color: '#3b82f6',
      weight: 4
    }).addTo(map);
  
    // Current location
    L.circleMarker(route[0], {
      radius: 7,
      color: '#22c55e',
      fillOpacity: 1
    }).addTo(map).bindPopup("You");
  
    // Next delivery highlight
    L.circleMarker(route[1], {
      radius: 9,
      color: '#facc15',
      fillOpacity: 1
    }).addTo(map).bindPopup("Next Delivery");
  
  });