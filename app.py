#!/usr/bin/env python3
"""
Mpho Dynal Mabena - Personal Website
Flask Application with Contact Form Handling
"""

import os
import logging
from datetime import datetime
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import re

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
# Configure database - use absolute path for SQLite
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'messages.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============= DATABASE MODELS =============

class ContactMessage(db.Model):
    """Model for storing contact form submissions"""
    __tablename__ = 'contact_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<Message {self.id}: {self.name} - {self.subject[:30]}>'
    
    def to_dict(self):
        """Convert message to dictionary for JSON responses"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'subject': self.subject,
            'message': self.message[:100] + '...' if len(self.message) > 100 else self.message,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M'),
            'is_read': self.is_read
        }


class VisitLog(db.Model):
    """Model for tracking page visits (optional, for analytics)"""
    __tablename__ = 'visit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    page = db.Column(db.String(50), nullable=False)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(200))
    visited_at = db.Column(db.DateTime, default=datetime.utcnow)


# Create database tables
with app.app_context():
    db.create_all()
    logger.info("Database tables created/verified")


# ============= VALIDATION FUNCTIONS =============

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_name(name):
    """Validate name (2-100 chars, letters, spaces, hyphens)"""
    if not name or len(name) < 2 or len(name) > 100:
        return False
    pattern = r'^[a-zA-Z\s\'-]+$'
    return re.match(pattern, name) is not None

def validate_subject(subject):
    """Validate subject (3-200 chars)"""
    return subject and 3 <= len(subject) <= 200

def validate_message(message):
    """Validate message (10-5000 chars)"""
    return message and 10 <= len(message) <= 5000


# ============= ROUTES =============

@app.route('/')
def home():
    """Home page route"""
    # Log the visit (optional)
    log_visit('home', request)
    return render_template('index.html')


@app.route('/about')
def about():
    """About page route"""
    log_visit('about', request)
    return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page with form handling"""
    if request.method == 'POST':
        return handle_contact_form()
    
    # GET request - just show the form
    log_visit('contact', request)
    return render_template('contact.html')


@app.route('/submit-contact', methods=['POST'])
def submit_contact():
    """API endpoint for AJAX form submissions"""
    return handle_contact_form(ajax=True)


def handle_contact_form(ajax=False):
    """
    Handle contact form submission
    Args:
        ajax: Boolean indicating if this is an AJAX request
    Returns:
        HTML redirect or JSON response
    """
    try:
        # Get form data
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()
        
        # Validate all fields
        errors = {}
        
        if not validate_name(name):
            errors['name'] = 'Please enter a valid name (2-100 characters, letters only)'
        
        if not validate_email(email):
            errors['email'] = 'Please enter a valid email address'
        
        if not validate_subject(subject):
            errors['subject'] = 'Subject must be between 3 and 200 characters'
        
        if not validate_message(message):
            errors['message'] = 'Message must be between 10 and 5000 characters'
        
        # If there are validation errors
        if errors:
            if ajax:
                return jsonify({
                    'success': False,
                    'errors': errors
                }), 400
            else:
                # Flash errors and redirect back to contact page
                for field, error in errors.items():
                    flash(f'{field.capitalize()}: {error}', 'error')
                return redirect(url_for('contact'))
        
        # Save to database
        new_message = ContactMessage(
            name=name,
            email=email,
            subject=subject,
            message=message,
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string[:200] if request.user_agent else None
        )
        
        db.session.add(new_message)
        db.session.commit()
        
        # Log the successful submission
        logger.info(f"New contact message from {name} ({email})")
        
        # Send email notification (optional - will implement if needed)
        # send_email_notification(new_message)
        
        if ajax:
            return jsonify({
                'success': True,
                'message': 'Thank you for your message! I will get back to you soon.'
            })
        else:
            flash('Thank you for your message! I will get back to you soon.', 'success')
            return redirect(url_for('contact'))
            
    except Exception as e:
        logger.error(f"Error processing contact form: {str(e)}")
        
        if ajax:
            return jsonify({
                'success': False,
                'errors': {'form': 'An error occurred. Please try again later.'}
            }), 500
        else:
            flash('An error occurred. Please try again later.', 'error')
            return redirect(url_for('contact'))


@app.route('/api/messages')
def get_messages():
    """API endpoint to retrieve messages (protected - for admin use)"""
    # TODO: Add authentication before using in production
    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return jsonify([msg.to_dict() for msg in messages])


@app.route('/api/stats')
def get_stats():
    """API endpoint for website statistics"""
    total_messages = ContactMessage.query.count()
    unread_messages = ContactMessage.query.filter_by(is_read=False).count()
    
    # Get message count by date (last 7 days)
    seven_days_ago = datetime.utcnow().date()
    messages_by_day = db.session.query(
        func.date(ContactMessage.created_at).label('date'),
        func.count().label('count')
    ).filter(
        ContactMessage.created_at >= seven_days_ago
    ).group_by(
        func.date(ContactMessage.created_at)
    ).all()
    
    return jsonify({
        'total_messages': total_messages,
        'unread_messages': unread_messages,
        'messages_by_day': [
            {'date': str(day.date), 'count': day.count} 
            for day in messages_by_day
        ]
    })


@app.route('/health')
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'database': 'connected' if db.engine else 'error'
    })


# ============= HELPER FUNCTIONS =============

def log_visit(page, request):
    """Log page visits (optional)"""
    try:
        visit = VisitLog(
            page=page,
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string[:200] if request.user_agent else None
        )
        db.session.add(visit)
        db.session.commit()
    except Exception as e:
        logger.error(f"Failed to log visit: {str(e)}")


def send_email_notification(message):
    """
    Send email notification for new contact form submissions
    TODO: Implement with your email service (SendGrid, SMTP, etc.)
    """
    # This is a placeholder - implement based on your email service
    pass


# ============= ERROR HANDLERS =============

@app.errorhandler(404)
def page_not_found(e):
    """Custom 404 page"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    """Custom 500 page"""
    logger.error(f"Internal server error: {str(e)}")
    return render_template('500.html'), 500


# ============= CONTEXT PROCESSORS =============

@app.context_processor
def utility_processor():
    """Make useful functions available to all templates"""
    def current_year():
        return datetime.now().year
    
    return dict(current_year=current_year)


# ============= MAIN ENTRY POINT =============

if __name__ == '__main__':
    # Get port from environment variable or use default
    port = int(os.environ.get('PORT', 5000))
    
    # Run the app
    app.run(
        host='0.0.0.0',  # Allows external access
        port=port,
        debug=False  # Set to False in production
    )