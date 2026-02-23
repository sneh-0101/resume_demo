/**
 * Job Portal - Main JavaScript
 * Client-side utilities and interactions
 */

// Initialize Bootstrap components
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});

/**
 * Format match score with color
 * @param {number} score - Match score (0-100)
 * @returns {string} HTML badge with color
 */
function getMatchScoreBadge(score) {
    if (score >= 80) {
        return `<span class="badge bg-success">Excellent (${score}%)</span>`;
    } else if (score >= 60) {
        return `<span class="badge bg-warning">Good (${score}%)</span>`;
    } else if (score >= 40) {
        return `<span class="badge bg-info">Fair (${score}%)</span>`;
    } else {
        return `<span class="badge bg-danger">Poor (${score}%)</span>`;
    }
}

/**
 * Format date to readable format
 * @param {string} dateString - ISO date string
 * @returns {string} Formatted date
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

/**
 * Copy text to clipboard
 * @param {string} text - Text to copy
 */
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        alert('Copied to clipboard!');
    }).catch(() => {
        alert('Failed to copy');
    });
}

/**
 * Validate file upload
 * @param {File} file - File to validate
 * @param {string} type - File type (pdf, doc, etc)
 * @returns {boolean} True if valid
 */
function validateFile(file, type = 'pdf') {
    const validTypes = {
        'pdf': ['application/pdf'],
        'doc': ['application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'],
        'image': ['image/jpeg', 'image/png', 'image/gif'],
    };

    const maxSize = 16 * 1024 * 1024; // 16MB

    if (file.size > maxSize) {
        alert('File size exceeds 16MB limit');
        return false;
    }

    if (!validTypes[type] || !validTypes[type].includes(file.type)) {
        alert(`Invalid file type. Allowed: ${type}`);
        return false;
    }

    return true;
}

/**
 * Show loading spinner
 * @param {string} element - Element selector
 */
function showSpinner(element = 'body') {
    const spinner = document.createElement('div');
    spinner.className = 'spinner-border text-primary';
    spinner.setAttribute('role', 'status');
    spinner.innerHTML = '<span class="visually-hidden">Loading...</span>';
    document.querySelector(element).appendChild(spinner);
}

/**
 * Hide loading spinner
 */
function hideSpinner() {
    const spinner = document.querySelector('.spinner-border');
    if (spinner) spinner.remove();
}

/**
 * Format currency
 * @param {number} amount - Amount to format
 * @param {string} currency - Currency code (USD, EUR, etc)
 * @returns {string} Formatted currency
 */
function formatCurrency(amount, currency = 'USD') {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: currency,
    }).format(amount);
}

/**
 * Export table data to CSV
 * @param {string} tableId - Table ID to export
 * @param {string} filename - Output filename
 */
function exportTableToCSV(tableId, filename = 'export.csv') {
    const table = document.getElementById(tableId);
    const csv = [];

    // Get headers
    const headers = Array.from(table.querySelectorAll('th')).map(th => th.textContent.trim());
    csv.push(headers.join(','));

    // Get rows
    table.querySelectorAll('tbody tr').forEach(row => {
        const cells = Array.from(row.querySelectorAll('td')).map(td => `"${td.textContent.trim()}"`);
        csv.push(cells.join(','));
    });

    // Download
    const blob = new Blob([csv.join('\n')], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    window.URL.revokeObjectURL(url);
}

/**
 * Smooth scroll to element
 * @param {string} selector - Element selector
 */
function smoothScroll(selector) {
    document.querySelector(selector).scrollIntoView({ behavior: 'smooth' });
}
