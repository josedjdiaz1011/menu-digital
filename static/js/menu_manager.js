/**
 * Menu Manager JavaScript
 * Handles interactive functionality for the digital menu system
 */

document.addEventListener('DOMContentLoaded', function() {
    initializeMenuManager();
});

function initializeMenuManager() {
    // Initialize all components
    initializeImagePreviews();
    initializeFormValidation();
    initializeDeleteConfirmations();
    initializePriceFormatting();
    initializeAutoSave();
    initializeKeyboardShortcuts();
    initializeTooltips();
    initializeProgressIndicators();
}

/**
 * Image Preview Functionality
 */
function initializeImagePreviews() {
    const imageInputs = document.querySelectorAll('input[type="file"][accept*="image"]');
    
    imageInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            handleImagePreview(e.target);
        });
    });
}

function handleImagePreview(input) {
    if (input.files && input.files[0]) {
        const file = input.files[0];
        
        // Validate file size (max 5MB)
        if (file.size > 5 * 1024 * 1024) {
            showAlert('El archivo es demasiado grande. Máximo 5MB.', 'warning');
            input.value = '';
            return;
        }
        
        // Validate file type
        if (!file.type.startsWith('image/')) {
            showAlert('Por favor selecciona un archivo de imagen válido.', 'warning');
            input.value = '';
            return;
        }
        
        const reader = new FileReader();
        reader.onload = function(e) {
            createImagePreview(input, e.target.result, file.name);
        };
        reader.readAsDataURL(file);
    }
}

function createImagePreview(input, src, filename) {
    // Find or create preview container
    let previewContainer = input.parentNode.querySelector('.image-preview');
    if (!previewContainer) {
        previewContainer = document.createElement('div');
        previewContainer.className = 'image-preview mt-2';
        input.parentNode.appendChild(previewContainer);
    }
    
    previewContainer.innerHTML = `
        <div class="d-flex align-items-center p-2 border rounded">
            <img src="${src}" alt="Preview" class="me-2 rounded" style="width: 60px; height: 60px; object-fit: cover;">
            <div class="flex-grow-1">
                <div class="small fw-bold">${filename}</div>
                <div class="small text-muted">Vista previa</div>
            </div>
            <button type="button" class="btn btn-sm btn-outline-danger" onclick="removeImagePreview(this)">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;
}

function removeImagePreview(button) {
    const previewContainer = button.closest('.image-preview');
    const input = previewContainer.parentNode.querySelector('input[type="file"]');
    
    if (input) {
        input.value = '';
    }
    
    previewContainer.remove();
}

/**
 * Form Validation
 */
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(form)) {
                e.preventDefault();
            }
        });
        
        // Real-time validation
        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateField(input);
            });
        });
    });
}

function validateForm(form) {
    let isValid = true;
    const requiredFields = form.querySelectorAll('[required]');
    
    requiredFields.forEach(field => {
        if (!validateField(field)) {
            isValid = false;
        }
    });
    
    return isValid;
}

function validateField(field) {
    const value = field.value.trim();
    let isValid = true;
    let message = '';
    
    // Required field validation
    if (field.hasAttribute('required') && !value) {
        isValid = false;
        message = 'Este campo es obligatorio';
    }
    
    // Email validation
    if (field.type === 'email' && value && !isValidEmail(value)) {
        isValid = false;
        message = 'Ingresa un email válido';
    }
    
    // URL validation
    if (field.type === 'url' && value && !isValidUrl(value)) {
        isValid = false;
        message = 'Ingresa una URL válida';
    }
    
    // Minimum length validation
    if (field.hasAttribute('minlength') && value.length < parseInt(field.getAttribute('minlength'))) {
        isValid = false;
        message = `Mínimo ${field.getAttribute('minlength')} caracteres`;
    }
    
    updateFieldValidation(field, isValid, message);
    return isValid;
}

function updateFieldValidation(field, isValid, message) {
    // Remove existing validation classes
    field.classList.remove('is-valid', 'is-invalid');
    
    // Remove existing feedback
    const existingFeedback = field.parentNode.querySelector('.invalid-feedback, .valid-feedback');
    if (existingFeedback) {
        existingFeedback.remove();
    }
    
    if (!isValid) {
        field.classList.add('is-invalid');
        
        if (message) {
            const feedback = document.createElement('div');
            feedback.className = 'invalid-feedback';
            feedback.textContent = message;
            field.parentNode.appendChild(feedback);
        }
    } else if (field.value.trim()) {
        field.classList.add('is-valid');
    }
}

/**
 * Delete Confirmations
 */
function initializeDeleteConfirmations() {
    const deleteButtons = document.querySelectorAll('form[action*="delete"] button[type="submit"]');
    
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const form = button.closest('form');
            const confirmMessage = getDeleteConfirmMessage(form);
            
            if (!confirm(confirmMessage)) {
                e.preventDefault();
            }
        });
    });
}

function getDeleteConfirmMessage(form) {
    if (form.action.includes('section')) {
        return '¿Estás seguro de eliminar esta sección y todos sus platillos? Esta acción no se puede deshacer.';
    } else if (form.action.includes('dish')) {
        return '¿Estás seguro de eliminar este platillo? Esta acción no se puede deshacer.';
    } else if (form.action.includes('restaurant')) {
        return '¿Estás seguro de eliminar este restaurante y todo su contenido? Esta acción no se puede deshacer.';
    }
    
    return '¿Estás seguro de que quieres eliminar este elemento?';
}

/**
 * Price Formatting
 */
function initializePriceFormatting() {
    const priceInputs = document.querySelectorAll('input[name*="price"]');
    
    priceInputs.forEach(input => {
        input.addEventListener('blur', function() {
            formatPrice(input);
        });
        
        input.addEventListener('input', function() {
            // Only allow numbers, dots, and commas
            input.value = input.value.replace(/[^\d.,]/g, '');
        });
    });
}

function formatPrice(input) {
    let value = input.value.trim();
    
    if (!value) return;
    
    // Remove any non-numeric characters except dots and commas
    value = value.replace(/[^\d.,]/g, '');
    
    // Handle different decimal separators
    if (value.includes(',') && value.includes('.')) {
        // Assume comma is thousands separator
        value = value.replace(/,/g, '');
    } else if (value.includes(',')) {
        // Assume comma is decimal separator
        value = value.replace(',', '.');
    }
    
    // Parse and format
    const number = parseFloat(value);
    if (!isNaN(number)) {
        input.value = number.toFixed(2);
    }
}

/**
 * Auto-save functionality (for future implementation)
 */
function initializeAutoSave() {
    // This can be implemented to save draft data to localStorage
    // For now, we'll just add the foundation
    
    const draftKey = 'menu_draft_' + window.location.pathname;
    
    // Save form data to localStorage on input
    const formInputs = document.querySelectorAll('form input, form textarea, form select');
    formInputs.forEach(input => {
        input.addEventListener('input', debounce(() => {
            saveDraft(draftKey);
        }, 1000));
    });
    
    // Load draft on page load
    loadDraft(draftKey);
}

function saveDraft(key) {
    const formData = {};
    const inputs = document.querySelectorAll('form input, form textarea, form select');
    
    inputs.forEach(input => {
        if (input.name && input.type !== 'file') {
            formData[input.name] = input.value;
        }
    });
    
    localStorage.setItem(key, JSON.stringify(formData));
    showDraftSavedIndicator();
}

function loadDraft(key) {
    const draftData = localStorage.getItem(key);
    
    if (draftData) {
        try {
            const formData = JSON.parse(draftData);
            
            Object.keys(formData).forEach(name => {
                const input = document.querySelector(`[name="${name}"]`);
                if (input && !input.value) {
                    input.value = formData[name];
                }
            });
            
            showDraftLoadedIndicator();
        } catch (e) {
            console.warn('Error loading draft:', e);
        }
    }
}

function showDraftSavedIndicator() {
    // Show a subtle indicator that draft was saved
    const indicator = document.createElement('div');
    indicator.className = 'toast-container position-fixed bottom-0 end-0 p-3';
    indicator.innerHTML = `
        <div class="toast show" role="alert">
            <div class="toast-body">
                <i class="fas fa-save me-2 text-success"></i>Borrador guardado
            </div>
        </div>
    `;
    
    document.body.appendChild(indicator);
    
    setTimeout(() => {
        indicator.remove();
    }, 3000);
}

function showDraftLoadedIndicator() {
    showAlert('Se cargó un borrador guardado anteriormente', 'info');
}

/**
 * Keyboard Shortcuts
 */
function initializeKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Ctrl+S to save form
        if (e.ctrlKey && e.key === 's') {
            e.preventDefault();
            const submitButton = document.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.click();
            }
        }
        
        // Escape to cancel/close modals
        if (e.key === 'Escape') {
            const openModal = document.querySelector('.modal.show');
            if (openModal) {
                const modal = bootstrap.Modal.getInstance(openModal);
                if (modal) {
                    modal.hide();
                }
            }
        }
    });
}

/**
 * Initialize Tooltips
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Progress Indicators
 */
function initializeProgressIndicators() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            showLoadingIndicator(form);
        });
    });
}

function showLoadingIndicator(form) {
    const submitButton = form.querySelector('button[type="submit"]');
    
    if (submitButton) {
        const originalText = submitButton.innerHTML;
        submitButton.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Guardando...';
        submitButton.disabled = true;
        
        // Re-enable after 5 seconds as fallback
        setTimeout(() => {
            submitButton.innerHTML = originalText;
            submitButton.disabled = false;
        }, 5000);
    }
}

/**
 * Utility Functions
 */
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function isValidUrl(url) {
    try {
        new URL(url.startsWith('http') ? url : 'https://' + url);
        return true;
    } catch {
        return false;
    }
}

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

function showAlert(message, type = 'info') {
    const alertContainer = document.querySelector('.container');
    
    if (alertContainer) {
        const alert = document.createElement('div');
        alert.className = `alert alert-${type} alert-dismissible fade show mt-3`;
        alert.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        alertContainer.insertBefore(alert, alertContainer.firstChild);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            if (alert.parentNode) {
                alert.remove();
            }
        }, 5000);
    }
}

/**
 * Menu Statistics
 */
function updateMenuStats() {
    const sections = document.querySelectorAll('.menu-section');
    const dishes = document.querySelectorAll('.dish-card');
    
    // Update counters if they exist
    const sectionCounter = document.querySelector('[data-stat="sections"]');
    const dishCounter = document.querySelector('[data-stat="dishes"]');
    
    if (sectionCounter) {
        sectionCounter.textContent = sections.length;
    }
    
    if (dishCounter) {
        dishCounter.textContent = dishes.length;
    }
}

/**
 * Image Optimization
 */
function optimizeImage(file, maxWidth = 800, maxHeight = 600, quality = 0.8) {
    return new Promise((resolve) => {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        const img = new Image();
        
        img.onload = function() {
            // Calculate new dimensions
            let { width, height } = img;
            
            if (width > maxWidth || height > maxHeight) {
                const ratio = Math.min(maxWidth / width, maxHeight / height);
                width *= ratio;
                height *= ratio;
            }
            
            canvas.width = width;
            canvas.height = height;
            
            // Draw and compress
            ctx.drawImage(img, 0, 0, width, height);
            
            canvas.toBlob(resolve, 'image/jpeg', quality);
        };
        
        img.src = URL.createObjectURL(file);
    });
}

/**
 * Export functionality for menu data
 */
function exportMenuData() {
    const menuData = collectMenuData();
    const dataStr = JSON.stringify(menuData, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
    
    const exportFileDefaultName = `menu_${new Date().toISOString().split('T')[0]}.json`;
    
    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
}

function collectMenuData() {
    // This would collect all menu data from the current page
    // Implementation depends on the page structure
    return {
        restaurant: document.querySelector('h1').textContent,
        exportDate: new Date().toISOString(),
        sections: Array.from(document.querySelectorAll('.menu-section')).map(section => ({
            name: section.querySelector('h2').textContent,
            dishes: Array.from(section.querySelectorAll('.dish-card')).map(dish => ({
                name: dish.querySelector('.card-title').textContent,
                description: dish.querySelector('.card-text')?.textContent || '',
                price: dish.querySelector('.badge')?.textContent || ''
            }))
        }))
    };
}

// Global functions for template use
window.removeImagePreview = removeImagePreview;
window.exportMenuData = exportMenuData;
