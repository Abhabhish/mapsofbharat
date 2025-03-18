const map = L.map('map',{attributionControl:false,zoomControl: false}).setView([22.90,79.07], 5);

tileLayer = L.tileLayer('http://{s}.google.com/vt/lyrs=r&x={x}&y={y}&z={z}', {
    maxZoom: 20,
    subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
})

tileLayer.addTo(map)

zControls = L.control.zoom({position: 'bottomright'})

zControls.addTo(map)




