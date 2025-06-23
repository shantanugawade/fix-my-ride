function getNearbyServiceCenters() {
    console.log("Fetching nearby service centers...");

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            let lat = position.coords.latitude;
            let lon = position.coords.longitude;

            fetch('/get_nearby_garages', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ latitude: lat, longitude: lon })
            })
            .then(response => response.json())
            .then(data => {
                console.log("API Response:", data);
                let centerList = document.getElementById("service-centers");
                centerList.innerHTML = "";

                if (!data.service_centers || data.service_centers.length === 0) {
                    centerList.innerHTML = "<p>No nearby service centers found.</p>";
                    return;
                }

                data.service_centers.forEach(center => {
                    let div = document.createElement("div");
                    div.classList.add("center-card");
                    div.innerHTML = `
                        <h3>${center.name}</h3>
                        <p class="location">📍 ${center.address}</p>
                        <a href="https://www.google.com/maps/search/?api=1&query=${center.latitude},${center.longitude}" 
                            target="_blank" class="view-details">View on Map</a>
                    `;
                    centerList.appendChild(div);
                });
            })
            .catch(error => {
                console.error("Error fetching service centers:", error);
                document.getElementById("service-centers").innerHTML = "<p>Failed to load service centers.</p>";
            });

        }, function(error) {
            console.error("Geolocation error:", error);
            document.getElementById("service-centers").innerHTML = "<p>Please allow location access.</p>";
        });
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}

window.onload = getNearbyServiceCenters;
