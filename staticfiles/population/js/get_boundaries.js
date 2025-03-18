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

        // Add filtered districts to map
        L.geoJSON(filteredGeojson,
             {
            onEachFeature: handleFeature
        }
    ).addTo(map);
    })
    .catch(error => console.error("Error loading GeoJSON:", error));



function handleFeature(feature, layer) {
    const queryParams = Object.entries(dataFilteringFields)
        .map(([key, property]) => `${key}=${encodeURIComponent(feature.properties[property])}`)
        .join('&');
    const url = `/api/population/?${queryParams}&family_id=${colorRangeFamily}`;


    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                layer.bindPopup(`<b>Error:</b> ${data.error}`).openPopup();
            } else {
                let popupContent = '';
                for (const [key, value] of Object.entries(data)) {
                    popupContent += `<b>${key}:</b> ${value}<br>`;
                }
                layer.bindPopup(popupContent);
                layer.setStyle({
                    fillColor: data.color,
                    fillOpacity: 0.5,
                    color: 'black',
                    weight: 1,
                });

                // Dynamically create and add the table to the right panel
                addTableToRightPanel(data);
                addColorTableToRightPanel(data);
            }
        })
        .catch(error => {
            // console.error("Error fetching population data:", error);
            console.log(url)
            layer.bindPopup(`<b>Error:</b> Unable to fetch population data.`).openPopup();
        });
}


function addTableToRightPanel(data) {
    const rightPanel = document.getElementById('right-panel');
    
    // Check if a table already exists
    let table = rightPanel.querySelector('boundary-table');
    
    if (!table) {
        // If no table exists, create a new one
        table = document.createElement('boundary-table');

        // Add table header
        const headerRow = document.createElement('tr');
        for (const key of Object.keys(data)) {
            const headerCell = document.createElement('th');
            headerCell.textContent = key;
            headerCell.style.border = '1px solid black';
            headerCell.style.padding = '8px';
            headerCell.style.backgroundColor = 'grey';
            headerRow.appendChild(headerCell);
        }
        table.appendChild(headerRow);

        // Append the table to the right panel
        rightPanel.appendChild(table);
    }

    // Add a new row for the current feature
    const dataRow = document.createElement('tr');
    for (const value of Object.values(data)) {
        const dataCell = document.createElement('td');
        dataCell.textContent = value;
        dataCell.style.border = '1px solid black';
        dataCell.style.padding = '8px';
        dataCell.style.textAlign = 'center';
        dataRow.appendChild(dataCell);
    }
    table.appendChild(dataRow);
}





function addColorTableToRightPanel(colorData) {
    const rightPanel = document.getElementById('right-panel');
    
    // Check if a color table already exists
    let colorTable = rightPanel.querySelector('color-table');
    
    if (!colorTable) {
        // If no color table exists, create a new one
        colorTable = document.createElement('color-table');
        colorTable.style.marginTop = '16px'; // Add some spacing between tables

        // Add table header
        const headerRow = document.createElement('tr');
        
        const colorHeader = document.createElement('th');
        colorHeader.textContent = 'Color';
        colorHeader.style.border = '1px solid black';
        colorHeader.style.padding = '8px';
        colorHeader.style.backgroundColor = 'grey';
        colorHeader.style.color = 'white'; // Make text readable
        headerRow.appendChild(colorHeader);
        
        const valueRangeHeader = document.createElement('th');
        valueRangeHeader.textContent = 'Value Range';
        valueRangeHeader.style.border = '1px solid black';
        valueRangeHeader.style.padding = '8px';
        valueRangeHeader.style.backgroundColor = 'grey';
        valueRangeHeader.style.color = 'white';
        headerRow.appendChild(valueRangeHeader);
        
        colorTable.appendChild(headerRow);

        // Append the color table to the right panel
        rightPanel.appendChild(colorTable);
    }

    // Check for duplicate row based on color and value_range
    const existingRows = colorTable.querySelectorAll('tr');
    let isDuplicate = false;

    for (let i = 1; i < existingRows.length; i++) { // Skip header row
        const cells = existingRows[i].querySelectorAll('td');
        if (
            cells[0].textContent === colorData.color && 
            cells[1].textContent === colorData.value_range
        ) {
            isDuplicate = true;
            break;
        }
    }

    if (!isDuplicate) {
        // Add a new row for the current color data
        const dataRow = document.createElement('tr');
        
        const colorCell = document.createElement('td');
        colorCell.textContent = colorData.color;
        colorCell.style.border = '1px solid black';
        colorCell.style.padding = '8px';
        colorCell.style.textAlign = 'center';
        colorCell.style.backgroundColor = colorData.color; // Set the background color
        colorCell.style.color = 'white'; // Ensure text is visible
        dataRow.appendChild(colorCell);
        
        const valueRangeCell = document.createElement('td');
        valueRangeCell.textContent = colorData.value_range; // Set the value range correctly
        valueRangeCell.style.border = '1px solid black';
        valueRangeCell.style.padding = '8px';
        valueRangeCell.style.textAlign = 'center';
        dataRow.appendChild(valueRangeCell);
        
        colorTable.appendChild(dataRow);
    }
}






