// Hospital Management System - Custom JavaScript

// Initialize tooltips and popovers
document.addEventListener('DOMContentLoaded', function() {
    initializeTooltips();
    initializePopovers();
    setupFormValidation();
});

// Initialize Bootstrap Tooltips
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Initialize Bootstrap Popovers
function initializePopovers() {
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

// Form Validation
function setupFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
}

// Show confirmation dialog
function confirmAction(message) {
    return confirm(message);
}

// Delete confirmation
function deleteConfirm(message = 'Are you sure you want to delete this item?') {
    return confirm(message);
}

// Show loading spinner
function showLoading() {
    const spinner = document.createElement('div');
    spinner.className = 'spinner';
    spinner.id = 'loading-spinner';
    document.body.appendChild(spinner);
}

// Hide loading spinner
function hideLoading() {
    const spinner = document.getElementById('loading-spinner');
    if (spinner) {
        spinner.remove();
    }
}

// Alert functions
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.setAttribute('role', 'alert');
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    const container = document.querySelector('.container-fluid') || document.body;
    container.insertBefore(alertDiv, container.firstChild);
}

// Fetch API wrapper
async function fetchAPI(url, options = {}) {
    try {
        const response = await fetch(url, options);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Fetch error:', error);
        showAlert('An error occurred. Please try again.', 'danger');
        return null;
    }
}

// Format date
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-US', options);
}

// Format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

// Format time
function formatTime(timeString) {
    const [hours, minutes] = timeString.split(':');
    return `${hours}:${minutes}`;
}

// Search patients
function searchPatients() {
    const searchInput = document.getElementById('patientSearch');
    if (!searchInput) return;
    
    searchInput.addEventListener('input', async function(e) {
        const query = e.target.value;
        if (query.length < 2) {
            clearSearchResults();
            return;
        }
        
        const data = await fetchAPI(`/patients/api/search?q=${encodeURIComponent(query)}`);
        if (data) {
            displaySearchResults(data);
        }
    });
}

// Search doctors
function searchDoctors(specialization = '') {
    const searchInput = document.getElementById('doctorSearch');
    if (!searchInput) return;
    
    searchInput.addEventListener('input', async function(e) {
        const query = e.target.value;
        if (query.length < 2) {
            clearSearchResults();
            return;
        }
        
        const url = specialization 
            ? `/doctors/api/search?q=${encodeURIComponent(query)}&specialization=${encodeURIComponent(specialization)}`
            : `/doctors/api/search?q=${encodeURIComponent(query)}`;
        
        const data = await fetchAPI(url);
        if (data) {
            displaySearchResults(data);
        }
    });
}

// Display search results
function displaySearchResults(results) {
    const resultsContainer = document.getElementById('searchResults');
    if (!resultsContainer) return;
    
    if (results.length === 0) {
        resultsContainer.innerHTML = '<div class="alert alert-info">No results found</div>';
        return;
    }
    
    let html = '<ul class="list-group">';
    results.forEach(item => {
        html += `
            <li class="list-group-item cursor-pointer" onclick="selectResult(${item.id}, '${item.name}')">
                <strong>${item.name}</strong><br>
                <small class="text-muted">${item.email}</small>
            </li>
        `;
    });
    html += '</ul>';
    
    resultsContainer.innerHTML = html;
}

// Clear search results
function clearSearchResults() {
    const resultsContainer = document.getElementById('searchResults');
    if (resultsContainer) {
        resultsContainer.innerHTML = '';
    }
}

// Select search result
function selectResult(id, name) {
    const resultIdInput = document.getElementById('selectedId');
    const resultNameInput = document.getElementById('selectedName');
    
    if (resultIdInput) resultIdInput.value = id;
    if (resultNameInput) resultNameInput.value = name;
    
    clearSearchResults();
}

// Load available slots
async function loadAvailableSlots() {
    const doctorSelect = document.getElementById('doctorId');
    const dateInput = document.getElementById('appointmentDate');
    const slotsContainer = document.getElementById('availableSlots');
    
    if (!doctorSelect || !dateInput || !slotsContainer) return;
    
    if (!doctorSelect.value || !dateInput.value) {
        slotsContainer.innerHTML = '';
        return;
    }
    
    const slots = await fetchAPI(
        `/appointments/api/available-slots?doctor_id=${doctorSelect.value}&date=${dateInput.value}`
    );
    
    if (slots && slots.length > 0) {
        let html = '<label class="form-label">Available Slots</label><div class="btn-group-vertical w-100">';
        slots.forEach(slot => {
            html += `<input type="radio" class="btn-check" name="appointmentTime" id="slot${slot}" value="${slot}">
                     <label class="btn btn-outline-primary w-100 text-start" for="slot${slot}">${formatTime(slot)}</label>`;
        });
        html += '</div>';
        slotsContainer.innerHTML = html;
    } else {
        slotsContainer.innerHTML = '<div class="alert alert-warning">No available slots for this date</div>';
    }
}

// Load available rooms
async function loadAvailableRooms(roomType = '') {
    const url = roomType 
        ? `/rooms/api/available-rooms?room_type=${encodeURIComponent(roomType)}`
        : '/rooms/api/available-rooms';
    
    const rooms = await fetchAPI(url);
    
    if (rooms && rooms.length > 0) {
        const roomsContainer = document.getElementById('availableRooms');
        if (roomsContainer) {
            let html = '';
            rooms.forEach(room => {
                html += `
                    <div class="card mb-2">
                        <div class="card-body">
                            <div class="d-flex justify-content-between">
                                <div>
                                    <h6 class="card-title">${room.room_number}</h6>
                                    <small class="text-muted">${room.room_type} | ${room.available_beds} bed(s) available</small>
                                </div>
                                <div class="text-end">
                                    <strong>${formatCurrency(room.rate_per_day)}/day</strong>
                                    <button class="btn btn-sm btn-primary ms-2" onclick="selectRoom(${room.id})">Select</button>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
            });
            roomsContainer.innerHTML = html;
        }
    }
}

// Select room
function selectRoom(roomId) {
    const roomIdInput = document.getElementById('roomId');
    if (roomIdInput) {
        roomIdInput.value = roomId;
        showAlert('Room selected successfully', 'success');
    }
}

// Export table to CSV
function exportTableToCSV(filename = 'export.csv') {
    const table = document.querySelector('table');
    if (!table) return;
    
    const csv = [];
    const rows = table.querySelectorAll('tr');
    
    rows.forEach(row => {
        const cols = row.querySelectorAll('td, th');
        const rowData = [];
        cols.forEach(col => {
            rowData.push('"' + col.textContent.trim().replace(/"/g, '""') + '"');
        });
        csv.push(rowData.join(','));
    });
    
    downloadCSV(csv.join('\n'), filename);
}

// Download CSV
function downloadCSV(csv, filename) {
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
}

// Print page
function printPage() {
    window.print();
}

// Chart initialization (if using Chart.js)
function initializeCharts() {
    const chartElements = document.querySelectorAll('[data-chart]');
    chartElements.forEach(element => {
        const chartType = element.dataset.chart;
        const chartData = JSON.parse(element.dataset.data || '{}');
        
        // Chart initialization logic here
        // This is a placeholder for Chart.js implementation
    });
}

// Initialize on page load
window.addEventListener('load', function() {
    searchPatients();
    searchDoctors();
    initializeCharts();
});

// Trigger available slots load
document.addEventListener('DOMContentLoaded', function() {
    const doctorSelect = document.getElementById('doctorId');
    const dateInput = document.getElementById('appointmentDate');
    
    if (doctorSelect) doctorSelect.addEventListener('change', loadAvailableSlots);
    if (dateInput) dateInput.addEventListener('change', loadAvailableSlots);
});

// Handle form submission
function handleFormSubmit(event) {
    event.preventDefault();
    const form = event.target;
    
    if (!form.checkValidity()) {
        event.stopPropagation();
        form.classList.add('was-validated');
        return false;
    }
    
    form.submit();
}
