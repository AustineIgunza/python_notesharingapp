// Notes Sharing App - Main JavaScript

// Initialize tooltips and popovers
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize Bootstrap popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});

// Confirm delete action
function confirmDelete(message = 'Are you sure you want to delete this?') {
    return confirm(message);
}

// Format date
function formatDate(date) {
    if (!date) return '';
    const d = new Date(date);
    return d.toLocaleDateString() + ' ' + d.toLocaleTimeString();
}

// Copy to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showNotification('Copied to clipboard!', 'success');
    }).catch(err => {
        showNotification('Failed to copy', 'error');
    });
}

// Show notification
function showNotification(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alertDiv);
            bsAlert.close();
        }, 5000);
    }
}

// Validate form before submit
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form.checkValidity() === false) {
        event.preventDefault();
        event.stopPropagation();
    }
    form.classList.add('was-validated');
}

// Search notes
function searchNotes() {
    const query = document.getElementById('searchInput')?.value;
    if (query && query.length >= 3) {
        window.location.href = `/search?q=${encodeURIComponent(query)}`;
    }
}

// Toggle favorite
function toggleFavorite(noteId) {
    const button = event.target;
    const isFavorite = button.classList.contains('favorited');
    
    fetch(`/notes/${noteId}/${isFavorite ? 'unfavorite' : 'favorite'}`, {
        method: 'POST'
    }).then(response => {
        if (response.ok) {
            button.classList.toggle('favorited');
            button.textContent = isFavorite ? '☆ Add to Favorites' : '⭐ Unfavorite';
        }
    });
}

// Character counter for textarea
function updateCharCount(textareaId, counterId) {
    const textarea = document.getElementById(textareaId);
    const counter = document.getElementById(counterId);
    
    if (textarea && counter) {
        textarea.addEventListener('input', () => {
            counter.textContent = textarea.value.length;
        });
    }
}

// Debounce function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Export notes as JSON
function exportNotes() {
    const notes = document.querySelectorAll('[data-note-id]');
    const data = [];
    
    notes.forEach(note => {
        data.push({
            id: note.dataset.noteId,
            title: note.querySelector('.note-title')?.textContent,
            content: note.querySelector('.note-content')?.textContent,
            created_at: note.dataset.createdAt
        });
    });
    
    const json = JSON.stringify(data, null, 2);
    downloadFile(json, 'notes.json', 'application/json');
}

// Download file
function downloadFile(content, filename, contentType) {
    const element = document.createElement('a');
    element.setAttribute('href', 'data:' + contentType + ';charset=utf-8,' + encodeURIComponent(content));
    element.setAttribute('download', filename);
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}

// Print note
function printNote() {
    window.print();
}

// Theme toggle
function toggleTheme() {
    const htmlElement = document.documentElement;
    const currentTheme = htmlElement.getAttribute('data-bs-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    htmlElement.setAttribute('data-bs-theme', newTheme);
    localStorage.setItem('theme', newTheme);
}

// Load theme preference
function loadTheme() {
    const saved = localStorage.getItem('theme');
    if (saved) {
        document.documentElement.setAttribute('data-bs-theme', saved);
    }
}

// Initialize on load
loadTheme();
