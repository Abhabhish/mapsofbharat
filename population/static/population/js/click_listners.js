// left hamburger click listner

let activeFamilyId;
document.querySelector('.left-hamburger').addEventListener('click', function() {
    var leftPanel = document.getElementById('left-panel');
    var colorPanel = document.getElementById('color-panel');
    var addColorFamilyForm = document.getElementById('add-color-family-form');
    if (leftPanel.style.display === 'none') {
        leftPanel.style.display = 'flex';
        colorPanel.style.display = 'none'
        addColorFamilyForm.style.display = 'none'
    } else {
        leftPanel.style.display = 'none';
    }
});

// right hamburger click listner
document.querySelector('.right-hamburger').addEventListener('click', function() {
    var rightPanel = document.getElementById('right-panel');
    var colorPanel = document.getElementById('color-panel');
    var addColorFamilyForm = document.getElementById('add-color-family-form');
    if (rightPanel.style.display === 'none') {
        rightPanel.style.display = 'flex';
        colorPanel.style.display = 'none'
        addColorFamilyForm.style.display = 'none'
    } else {
        rightPanel.style.display = 'none';
    }
});

// color palette click listner
document.querySelector('.color-palette').addEventListener('click', function() {
    var colorPanel = document.getElementById('color-panel');
    var leftPanel = document.getElementById('left-panel');
    var rightPanel = document.getElementById('right-panel');
    var addColorFamilyForm = document.getElementById('add-color-family-form');
    var addColorRangeForm = document.getElementById('add-color-range-form')
    var colorRangeTable = document.getElementById('color-range-table')
    if (colorPanel.style.display === 'none') {
        colorPanel.style.display = 'flex';
        leftPanel.style.display='none'
        rightPanel.style.display='none'
        addColorFamilyForm.style.display='none'
        addColorRangeForm.style.display='none'
        colorRangeTable.style.display = 'none'

    
        fetch("/get_color_families/")
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const colorFamilies = data.color_families;
                const tableBody = document.querySelector("#color-family-table-body");
                tableBody.innerHTML = "";
                colorFamilies.forEach(colorFamily => {
                    const newRow = `
                        <tr>
                            <td>${colorFamily.family_name}</td>
                            <td>
                                <button type="button" class="btn btn-primary" get-color-ranges-url="/get_color_ranges/${colorFamily.id}/" id="edit-family-${colorFamily.id}" onclick="editFamily(${ colorFamily.id })">
                                    <i class="fas fa-edit"></i>
                                </button>
                                <button type="button" class="btn btn-danger" delete-family-url="/delete-family/${colorFamily.id}/" id="delete-family-${colorFamily.id}" onclick="deleteFamily(${ colorFamily.id })">
                                    <i class="fas fa-trash"></i>
                                </button>
                            </td>
                        </tr>
                    `;
                    tableBody.insertAdjacentHTML("beforeend", newRow);
                });
            } else {
                alert("Failed to load color families");
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("An error occurred. Please try again.");
        });


    } else {
        colorPanel.style.display = 'none';
    }
});


// Add New Color Family button listner
document.getElementById('button-add-new-color-family').addEventListener('click', function() {
    var addColorFamilyForm = document.getElementById('add-color-family-form');
    var colorPanel = document.getElementById('color-panel')
    addColorFamilyForm.style.display = 'flex';
    colorPanel.style.display='none'
});

document.getElementById('button-add-new-color-range').addEventListener('click', function() {
    var addColorRangeForm = document.getElementById('add-color-range-form')
    var colorRangeTable = document.getElementById('color-range-table')
    addColorRangeForm.style.display = 'flex';
    colorRangeTable.style.display='none'
});


function getCSRFToken() {
    const csrfToken = document.cookie.split(';').find(cookie => cookie.trim().startsWith('csrftoken='));
    return csrfToken ? csrfToken.split('=')[1] : null;
}


document.getElementById('submit-color-family-button').addEventListener('click', function (e) {
    e.preventDefault();
    const addColorFamilyURL = document.getElementById('color-family-form').getAttribute('data-add-url');
    // Get the forms
    var colorRangeTable = document.getElementById('color-range-table');
    var addColorFamilyForm = document.getElementById('add-color-family-form');

    // Serialize form data
    var formData = new FormData(document.getElementById('color-family-form'));
    const csrfToken = getCSRFToken();

    // Send POST request to save data to the model
    fetch(addColorFamilyURL, {
        method: "POST",
        headers: {
            "X-CSRFToken": csrfToken // Include CSRF token
        },
        body: formData
    })
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response was not OK");
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                const newFamily = data.new_family;
                activeFamilyId = newFamily.family_id

                // Update the dropdown with the new family
                const dropdown = document.getElementById("family_name-select");
                const newOption = document.createElement("option");
                newOption.value = newFamily.family_name;
                newOption.textContent = newFamily.family_name;
                dropdown.appendChild(newOption);

                // Hide the color family form and show the color range form
                colorRangeTable.style.display = 'flex';
                addColorFamilyForm.style.display = 'none';

                const colorTableBody = document.querySelector("#color-range-table-body"); // Fixed selector
                colorTableBody.innerHTML = "";

                // Clear the form fields
                document.getElementById('color-family-form').reset();

                alert("Color family added successfully!");
            } else {
                alert("Failed to add color family. Please check the input data.");
                console.error(data.errors);
            }
        })
        .catch(error => {
            console.error("An error occurred:", error);
            alert("Failed to add color family. Please try again.");
        });
});


function deleteFamily(familyId) {
    const deleteButton = document.getElementById(`delete-family-${familyId}`);
    const deleteFamilyUrl = deleteButton.getAttribute('delete-family-url');

    if (confirm("Are you sure you want to delete this item?")) {
        fetch(deleteFamilyUrl)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Remove the row from the table
                const row = deleteButton.closest("tr"); // Get the parent row of the button
                row.remove();
                
                // Remove the family from the dropdown choices
                const familySelect = document.getElementById('family_name-select');
                const optionToRemove = Array.from(familySelect.options).find(option => option.value == familyId);
                if (optionToRemove) {
                    familySelect.removeChild(optionToRemove);
                }

                alert("Family deleted successfully!");
            } else {
                alert("Failed to delete family. Please try again.");
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("An error occurred. Please try again.");
        });
    }
}


function deleteRange(colorId) {
    const deleteButton = document.getElementById(`delete-range-${colorId}`);
    const deleteRangeUrl = deleteButton.getAttribute('delete-range-url');

    if (confirm("Are you sure you want to delete this item?")) {
        fetch(deleteRangeUrl)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Remove the row from the table
                const row = deleteButton.closest("tr"); // Get the parent row of the button
                row.remove();

                alert("Color deleted successfully!");
            } else {
                alert("Failed to delete Color. Please try again.");
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("An error occurred. Please try again.");
        });
    }
}


function editFamily(familyId) {
    activeFamilyId = familyId
    const editFamilyButton = document.getElementById(`edit-family-${familyId}`);
    const getColorRangesUrl = editFamilyButton.getAttribute('get-color-ranges-url');

    var colorRangeTable = document.getElementById('color-range-table');
    var colorPanel = document.getElementById('color-panel')

    fetch(getColorRangesUrl)
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const colorRanges = data.color_ranges;
                // Update the table with the new family
                const tableBody = document.querySelector("#color-range-table-body"); // Fixed selector
                tableBody.innerHTML = "";
                colorRanges.forEach(colorRange => {
                    const newRow = `
                        <tr>
                            <td>${colorRange.start}</td>
                            <td>${colorRange.end}</td>
                            <td style="background-color: ${colorRange.color}; color: #ffffff; text-align: center;">
                                ${colorRange.color}
                            </td>
                            <td>
                                <button type="button" class="btn btn-danger" delete-range-url="/delete-range/${colorRange.id}/" id="delete-range-${colorRange.id}" onclick="deleteRange(${colorRange.id})">
                                    <i class="fas fa-trash"></i>
                                </button>
                            </td>
                        </tr>
                    `;
                    tableBody.insertAdjacentHTML("beforeend", newRow);
                });
                colorRangeTable.style.display = 'flex';
                colorPanel.style.display = 'none';
        } else {
            alert("Failed to load color ranges");
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("An error occurred. Please try again.");
    });
}





document.getElementById('submit-color-range-button').addEventListener('click', function (e) {
    e.preventDefault();
    const addColorRangeURL = document.getElementById('color-range-form').getAttribute('color-add-url');
    // Get the forms
    var colorRangeTable = document.getElementById('color-range-table');
    var addColorRangeForm = document.getElementById('add-color-range-form');

    // Serialize form data
    var formData = new FormData(document.getElementById('color-range-form'));
    formData.append('activeFamilyId', activeFamilyId);
    const csrfToken = getCSRFToken();

    // Send POST request to save data to the model
    fetch(addColorRangeURL, {
        method: "POST",
        headers: {
            "X-CSRFToken": csrfToken // Include CSRF token
        },
        body: formData
    })
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response was not OK");
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                const colorRanges = data.color_ranges;

                // Update the table with the new family
                const tableBody = document.querySelector("#color-range-table-body"); // Fixed selector
                tableBody.innerHTML = "";
                colorRanges.forEach(colorRange => {
                    const newRow = `
                        <tr>
                            <td>${colorRange.start}</td>
                            <td>${colorRange.end}</td>
                            <td style="background-color: ${colorRange.color}; color: #ffffff; text-align: center;">
                                ${colorRange.color}
                            </td>
                            <td>
                                <button type="button" class="btn btn-danger" delete-range-url="/delete-range/${colorRange.id}/" id="delete-range-${colorRange.id}" onclick="deleteRange(${colorRange.id})">
                                    <i class="fas fa-trash"></i>
                                </button>
                            </td>
                        </tr>
                    `;
                    tableBody.insertAdjacentHTML("beforeend", newRow);
                });

                // Hide the color family form and show the color range form
                colorRangeTable.style.display = 'flex';
                addColorRangeForm.style.display = 'none';

                // Clear the form fields
                document.getElementById('color-family-form').reset();

                alert("Color family added successfully!");
            } else {
                alert("Failed to add color family. Please check the input data.");
                console.error(data.errors);
            }
        })
        .catch(error => {
            console.error("An error occurred:", error);
            alert("Failed to add color family. Please try again.");
        });
});