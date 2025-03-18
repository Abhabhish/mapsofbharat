document.addEventListener('DOMContentLoaded', function () {
    const townVillageSelect = document.getElementById('town_village-select')

    const boundarySelect = document.getElementById('boundary-select')

    townVillageSelect.addEventListener('change', function () {
        const townVillage = townVillageSelect.value;
        
        boundarySelect.innerHTML = '<option value="">Select Boundary</option>';

        if (townVillage) {
            var status = 'nonempty'
        } else{
            var status = 'empty'
        }

        fetch(`/get-applicable_boundaries/?recently_changed_field=town_village&status=${encodeURIComponent(status)}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Failed to fetch districts');
                    };
                    return response.json();
                })
                .then(data => {
                    if (data.applicable_boundaries) {
                        data.applicable_boundaries.forEach(boundary => {
                            console.log(boundary)
                            const option = document.createElement('option');
                            option.value = boundary;
                            option.textContent = boundary;
                            boundarySelect.appendChild(option);
                        });
                    } else if (data.error) {
                        alert(data.error);
                    }
                })
                .catch(error => {
                    console.error('Error fetching districts:', error);
                    alert('Could not load districts. Please try again.');
                });
    });
});