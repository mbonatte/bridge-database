var map = L.map('map').setView([48.3740124, 12.8769753], 4);  // Sets initial map view to center around the general area of the bridges

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap'
}).addTo(map);

// Function to fetch initial bridge data
function fetchBridgeNames() {
    fetch('/bridges/names')
    .then(response => response.json())
    .then(data => {
        addMarkersToMap(data);
    })
    .catch(error => console.error('Error fetching bridge names:', error));
}

// Function to add markers to the map
function addMarkersToMap(bridges) {
    bridges.forEach(function(bridge) {
        var marker = L.marker([bridge.latitude, bridge.longitude]).addTo(map);
        marker.bindPopup(`<b>${bridge.name}</b><br>
                          <button onclick="fetchBridgeDetails('${bridge.id}')" class="detail-btn">View Details</button>
                          <button onclick="window.open('/bridge/${bridge.id}', '_blank')" class="full-btn">Full Description</button>`);
    });
}

// Function to fetch detailed information of a bridge
function fetchBridgeDetails(bridgeId) {
    fetch(`/bridges/details?id=${encodeURIComponent(bridgeId)}`)
    .then(response => response.json())
    .then(data => {
        displayBridgeDetails(data);
    })
    .catch(error => console.error('Error fetching bridge details:', error));
}

// Function to display bridge details
function displayBridgeDetails(bridge) {
    var popupContent = `<b>${bridge.general_info.bridge_name}</b><br/>
                        Located in: ${bridge.general_info.city}, ${bridge.general_info.country}<br/>
                        Year of construction: ${bridge.general_info.year_of_construction}<br/>
                        Length: ${bridge.geometrical.total_length_m} meters<br/>
                        Max Span: ${bridge.geometrical.max_span_m} meters`;
    L.popup()
        .setLatLng([bridge.general_info.latitude, bridge.general_info.longitude])
        .setContent(popupContent)
        .openOn(map);
}

// Initial fetch for bridge names
fetchBridgeNames();