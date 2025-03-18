document.addEventListener('DOMContentLoaded', function () {
    const stateSelect = document.getElementById('state-select');
    const districtSelect = document.getElementById('district-select');
    const subDistrictSelect = document.getElementById('sub_district-select');
    const blockSelect = document.getElementById('block-select');
    const pincodeSelect = document.getElementById('pincode-select')
    const gramPanchayatSelect = document.getElementById('gram_panchayat-select')
    const townVillageSelect = document.getElementById('town_village-select')

    const boundarySelect = document.getElementById('boundary-select')

    blockSelect.addEventListener('change', function () {
        const state = stateSelect.value;
        const district = districtSelect.value;
        const subDistrict = subDistrictSelect.value;
        const block = blockSelect.value;

        pincodeSelect.innerHTML = '<option value="">Select Pincode</option>';
        gramPanchayatSelect.innerHTML = '<option value="">Select Gram Panchayat</option>';
        townVillageSelect.innerHTML = '<option value="">Select Town/Village</option>';


        boundarySelect.innerHTML = '<option value="">Select Boundary</option>';

        if (block) {
            fetch(`/get-pincodes/?state=${encodeURIComponent(state)}&district=${encodeURIComponent(district)}&sub_district=${encodeURIComponent(subDistrict)}&block=${encodeURIComponent(block)}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Failed to fetch districts');
                    }
                    return response.json();
                })
                .then(data => {
                    // console.log(data)
                    if (data.pincodes) {
                        data.pincodes.forEach(pincode => {
                            const option = document.createElement('option');
                            option.value = pincode;
                            option.textContent = pincode;
                            pincodeSelect.appendChild(option);
                        })
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

        fetch(`/get-applicable_boundaries/?recently_changed_field=block&status=${encodeURIComponent(status)}`)
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
                    console.error('Error fetching districts:', error);
                    alert('Could not load districts. Please try again.');
                });
    });
});