document.addEventListener('DOMContentLoaded', function () {
    const stateSelect = document.getElementById('state-select');
    const districtSelect = document.getElementById('district-select');
    const subDistrictSelect = document.getElementById('sub_district-select');
    const blockSelect = document.getElementById('block-select');
    const pincodeSelect = document.getElementById('pincode-select')
    const gramPanchayatSelect = document.getElementById('gram_panchayat-select')
    const townVillageSelect = document.getElementById('town_village-select')

    const boundarySelect = document.getElementById('boundary-select')

    districtSelect.addEventListener('change', function () {
        const state = stateSelect.value;
        const district = districtSelect.value;

        // Clear existing district options
        subDistrictSelect.innerHTML = '<option value="">Select Sub-District</option>';
        blockSelect.innerHTML = '<option value="">Select Block</option>';
        pincodeSelect.innerHTML = '<option value="">Select Pincode</option>';
        gramPanchayatSelect.innerHTML = '<option value="">Select Gram Panchayat</option>';
        townVillageSelect.innerHTML = '<option value="">Select Town/Village</option>';


        boundarySelect.innerHTML = '<option value="">Select Boundary</option>';

        if (district) {
            fetch(`/get-subdistricts/?state=${encodeURIComponent(state)}&district=${encodeURIComponent(district)}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Failed to fetch districts');
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.sub_districts) {
                        data.sub_districts.forEach(sub_district => {
                            const option = document.createElement('option');
                            option.value = sub_district;
                            option.textContent = sub_district;
                            subDistrictSelect.appendChild(option);
                        });
                    } else if (data.error) {
                        alert(data.error);
                    }
                })
                .catch(error => {
                    console.error('Error fetching districts:', error);
                    alert('Could not load districts. Please try again.');
                });
            var status = 'nonempty'
        } else{
            var status = 'empty'
        }


        fetch(`/get-applicable_boundaries/?recently_changed_field=district&status=${encodeURIComponent(status)}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Failed to fetch districts');
                    };
                    return response.json();
                })
                .then(data => {
                    if (data.applicable_boundaries) {
                        data.applicable_boundaries.forEach(boundary => {
                            // console.log(boundary)
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
                    console.error('Error fetching sub - districts:', error);
                    alert('Could not load sub - districts. Please try again.');
                });
    });
});