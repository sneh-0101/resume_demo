// Custom JavaScript for AI Resume Analyzer

document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap components
    initializePopovers();
    initializeTooltips();
    initializeFileUpload();
});

/**
 * Initialize Bootstrap popovers
 */
function initializePopovers() {
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

/**
 * Initialize Bootstrap tooltips
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Handle file upload with validation
 */
function initializeFileUpload() {
    const fileInputs = document.querySelectorAll('input[type="file"]');
    
    fileInputs.forEach(fileInput => {
        fileInput.addEventListener('change', function(e) {
            const file = this.files[0];
            
            if (file) {
                // Check file size (16MB max)
                const maxSize = 16 * 1024 * 1024;
                if (file.size > maxSize) {
                    alert('File size exceeds 16MB limit!');
                    this.value = '';
                    return;
                }
                
                // Check file type
                const allowedTypes = ['application/pdf'];
                if (!allowedTypes.includes(file.type)) {
                    alert('Only PDF files are allowed!');
                    this.value = '';
                    return;
                }
                
                // Show file name
                const label = this.previousElementSibling;
                if (label) {
                    label.textContent = file.name;
                }
            }
        });
    });
}

/**
 * Show loading spinner
 */
function showLoading() {
    const loader = document.getElementById('loading-spinner');
    if (loader) {
        loader.style.display = 'block';
    }
}

/**
 * Hide loading spinner
 */
function hideLoading() {
    const loader = document.getElementById('loading-spinner');
    if (loader) {
        loader.style.display = 'none';
    }
}

/**
 * Copy text to clipboard
 */
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        alert('Copied to clipboard!');
    }, function(err) {
        console.error('Could not copy text: ', err);
    });
}

/**
 * Format percentage value
 */
function formatPercentage(value) {
    return Math.round(value * 100) / 100;
}

/**
 * Get color based on score
 */
function getScoreColor(score) {
    if (score >= 75) return '#10B981'; // green
    if (score >= 50) return '#F59E0B'; // orange
    return '#EF4444'; // red
}

/**
 * Smooth scroll to element
 */
function smoothScroll(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
    }
}

/**
 * Validate email format
 */
function isValidEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

/**
 * Export table to CSV
 */
function exportTableToCSV(filename) {
    const csv = [];
    const rows = document.querySelectorAll('table tr');
    
    for (let i = 0; i < rows.length; i++) {
        const row = [], cols = rows[i].querySelectorAll('td, th');
        
        for (let j = 0; j < cols.length; j++) {
            row.push(cols[j].innerText);
        }
        
        csv.push(row.join(','));
    }
    
    downloadCSV(csv.join('\n'), filename);
}

/**
 * Download CSV file
 */
function downloadCSV(csv, filename) {
    const csvFile = new Blob([csv], { type: 'text/csv' });
    const downloadLink = document.createElement('a');
    downloadLink.href = URL.createObjectURL(csvFile);
    downloadLink.download = filename;
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
}

/**
 * Confirm action
 */
function confirmAction(message) {
    return confirm(message || 'Are you sure?');
}

// Auto-dismiss alerts after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});
