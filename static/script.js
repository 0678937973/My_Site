// script.js - Form validation and interactive features

// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    
    // ===== CONTACT FORM VALIDATION =====
    const contactForm = document.getElementById('contact-form');
    
    if (contactForm) {
        // Add real-time validation as user types
        const formInputs = contactForm.querySelectorAll('input, textarea');
        formInputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateField(this);
            });
            
            input.addEventListener('input', function() {
                // Clear error message while typing
                const errorId = this.id + '-error';
                const existingError = document.getElementById(errorId);
                if (existingError) {
                    existingError.remove();
                }
                this.style.borderColor = '#e0e0e0';
            });
        });

        // AJAX form submission
        contactForm.addEventListener('submit', function(event) {
            event.preventDefault();
            
            if (validateForm()) {
                // Show loading state
                const submitBtn = this.querySelector('button[type="submit"]');
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '⏳ Sending...';
                submitBtn.disabled = true;
                
                // Collect form data
                const formData = new FormData(this);
                
                // Send AJAX request
                fetch(this.action, {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        showFormMessage('success', data.message);
                        contactForm.reset();
                    } else {
                        if (data.errors) {
                            for (const [field, error] of Object.entries(data.errors)) {
                                const fieldElement = document.getElementById(field);
                                if (fieldElement) {
                                    showFieldError(fieldElement, error);
                                }
                            }
                        }
                        showFormMessage('error', 'Please fix the errors above.');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    showFormMessage('error', 'An error occurred. Please try again later.');
                })
                .finally(() => {
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                });
            }
        });
    }

    // ===== VALIDATION FUNCTIONS =====
    function validateForm() {
        let isValid = true;
        
        const fields = ['name', 'email', 'subject', 'message'];
        fields.forEach(fieldId => {
            const field = document.getElementById(fieldId);
            if (field && !validateField(field)) {
                isValid = false;
            }
        });
        
        return isValid;
    }

    function validateField(field) {
        const value = field.value.trim();
        const fieldId = field.id;
        const fieldName = fieldId.charAt(0).toUpperCase() + fieldId.slice(1);
        
        // Remove existing error
        const existingError = document.getElementById(fieldId + '-error');
        if (existingError) {
            existingError.remove();
        }
        
        field.style.borderColor = '#e0e0e0';
        
        if (value === '') {
            showFieldError(field, `${fieldName} is required`);
            return false;
        }
        
        switch (fieldId) {
            case 'email':
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (!emailRegex.test(value)) {
                    showFieldError(field, 'Please enter a valid email address');
                    return false;
                }
                break;
            case 'name':
                if (value.length < 2) {
                    showFieldError(field, 'Name must be at least 2 characters');
                    return false;
                }
                break;
            case 'subject':
                if (value.length < 3) {
                    showFieldError(field, 'Subject must be at least 3 characters');
                    return false;
                }
                break;
            case 'message':
                if (value.length < 10) {
                    showFieldError(field, 'Message must be at least 10 characters');
                    return false;
                }
                break;
        }
        
        return true;
    }

    function showFieldError(field, message) {
        field.style.borderColor = '#e74c3c';
        
        const errorDiv = document.createElement('div');
        errorDiv.id = field.id + '-error';
        errorDiv.className = 'error-message';
        errorDiv.style.color = '#e74c3c';
        errorDiv.style.fontSize = '0.85rem';
        errorDiv.style.marginTop = '-15px';
        errorDiv.style.marginBottom = '15px';
        errorDiv.innerHTML = '⚠ ' + message;
        
        field.parentNode.insertBefore(errorDiv, field.nextSibling);
    }

    function showFormMessage(type, message) {
        const existingMessage = document.querySelector('.form-message');
        if (existingMessage) {
            existingMessage.remove();
        }
        
        const messageDiv = document.createElement('div');
        messageDiv.className = 'form-message';
        messageDiv.style.padding = '15px';
        messageDiv.style.borderRadius = '6px';
        messageDiv.style.marginBottom = '20px';
        messageDiv.style.fontWeight = '600';
        
        if (type === 'success') {
            messageDiv.style.backgroundColor = '#d4edda';
            messageDiv.style.color = '#155724';
            messageDiv.innerHTML = '✓ ' + message;
        } else {
            messageDiv.style.backgroundColor = '#f8d7da';
            messageDiv.style.color = '#721c24';
            messageDiv.innerHTML = '✗ ' + message;
        }
        
        const form = document.getElementById('contact-form');
        form.insertBefore(messageDiv, form.firstChild);
        
        if (type === 'success') {
            setTimeout(() => {
                messageDiv.style.opacity = '0';
                messageDiv.style.transition = 'opacity 0.5s ease';
                setTimeout(() => messageDiv.remove(), 500);
            }, 5000);
        }
    }

    // ===== CHARACTER COUNTER =====
    const messageField = document.getElementById('message');
    if (messageField) {
        const counterDiv = document.createElement('div');
        counterDiv.id = 'char-counter';
        counterDiv.style.fontSize = '0.85rem';
        counterDiv.style.color = '#7f8c8d';
        counterDiv.style.marginTop = '5px';
        counterDiv.style.textAlign = 'right';
        messageField.parentNode.insertBefore(counterDiv, messageField.nextSibling);
        
        messageField.addEventListener('input', function() {
            counterDiv.textContent = this.value.length + '/5000 characters';
            
            if (this.value.length > 4500) {
                counterDiv.style.color = '#e67e22';
            }
            if (this.value.length > 4900) {
                counterDiv.style.color = '#e74c3c';
            }
        });
    }
});