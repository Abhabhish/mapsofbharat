function getCSRFToken() {
    const csrfToken = document.cookie.split(';').find(cookie => cookie.trim().startsWith('csrftoken='));
    return csrfToken ? csrfToken.split('=')[1] : null;
}


fetch(geojsonUrl)
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(geojsonData => {
        filteredGeojson = {
            ...geojsonData,
            features: geojsonData.features.filter(feature => {
                return Object.entries(boundaryFilteringFields).every(([key, value]) =>
                    String(feature.properties[key]).toLowerCase() === String(value).toLowerCase()
                );
            })
        };

        const stateBounds = L.geoJSON(filteredGeojson).getBounds();
        map.fitBounds(stateBounds);

        return fetch("/api/population/", {
            method: "POST",
            headers: { 
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken()
            },
            body: JSON.stringify({dataFilteringFields,extraFields, family_id: colorRangeFamily })
        });
    })

    .then(response => response.json())
    .then(rawData => {
        colorRanges = rawData['color_ranges']
        filteredData = rawData['filtered_data']
        responseData = {}

        for (let entry of filteredData) {            
            let key = Object.entries(extraFields).map(([key, property]) => entry[key] || "").join("|");
            let _sum = entry.population_sum;
            let color = "gray";
            let value_range = "range not exists";
            for (let range of colorRanges) {
                if (_sum >= range.start && _sum <= range.end) {
                    color = range.color;
                    value_range = `${range.start} - ${range.end}`;
                    break;
                }
            }
            responseData[key] = {
                ...entry,
                color: color,
                value_range: value_range
            };
        }



        L.geoJSON(filteredGeojson, {
            onEachFeature: (feature, layer) => {
                // Generate a consistent key using only relevant fields
                let featureKey = Object.entries(extraFields)
                    .map(([key, property]) => feature.properties[property] || "")
                    .join("|");

                // Get corresponding data from API response
                const data = responseData[featureKey] || { population: "N/A", color: "gray" };

                let popupContent = Object.entries(data)
                    .map(([key, value]) => `<b>${key}:</b> ${value}<br>`)
                    .join("");

                layer.bindPopup(popupContent);
                layer.setStyle({
                    fillColor: data.color,
                    fillOpacity: 0.4,
                    color: "black",
                    weight: 1
                });
            }
        }).addTo(map);
        addAllDataToRightPanel(responseData);
        
    })
    .catch(error => console.error("Error loading GeoJSON:", error));



function addAllDataToRightPanel(responseData) {
    const rightPanel = document.getElementById('right-panel');
    rightPanel.innerHTML = ""; // Clear the panel before adding new data

    if (Object.keys(responseData).length === 0) return;

    // Create a table
    const table = document.createElement('table');
    table.style.borderCollapse = 'collapse';
    table.style.width = '100%';

    // Add table header using the first object from responseData
    const headerRow = document.createElement('tr');
    const firstKey = Object.keys(responseData)[0];
    for (const key of Object.keys(responseData[firstKey])) {
        const headerCell = document.createElement('th');
        headerCell.textContent = key;
        headerCell.style.border = '1px solid black';
        headerCell.style.padding = '8px';
        headerCell.style.backgroundColor = 'grey';
        headerRow.appendChild(headerCell);
    }
    table.appendChild(headerRow);

    // Add all rows from responseData
    Object.values(responseData).forEach(data => {
        const dataRow = document.createElement('tr');
        Object.values(data).forEach(value => {
            const dataCell = document.createElement('td');
            dataCell.textContent = value;
            dataCell.style.border = '1px solid black';
            dataCell.style.padding = '8px';
            dataCell.style.textAlign = 'center';
            dataRow.appendChild(dataCell);
        });
        table.appendChild(dataRow);
    });

    // Append the table to the right panel
    rightPanel.appendChild(table);
}


