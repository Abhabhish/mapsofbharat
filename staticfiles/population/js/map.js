const map = L.map('map',{attributionControl:false,zoomControl: false}).setView([22.90,79.07], 5);

tileLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png')

tileLayer.addTo(map)

zControls = L.control.zoom({position: 'bottomright'})

zControls.addTo(map)




