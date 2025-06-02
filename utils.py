"""
Utility functions for the digital menu system
"""

import os
import json
import qrcode
from PIL import Image
from datetime import datetime
import uuid
import logging

def generate_unique_id():
    """Generate a unique 8-character ID"""
    return str(uuid.uuid4())[:8]

def format_price(price_str):
    """Format price string for display"""
    if not price_str:
        return ""
    
    # Remove any non-numeric characters except dots and commas
    cleaned = ''.join(c for c in price_str if c.isdigit() or c in '.,')
    
    try:
        # Handle different decimal separators
        if ',' in cleaned and '.' in cleaned:
            # Assume comma is thousands separator
            cleaned = cleaned.replace(',', '')
        elif ',' in cleaned:
            # Assume comma is decimal separator
            cleaned = cleaned.replace(',', '.')
        
        # Convert to float and back to format consistently
        price_float = float(cleaned)
        return f"${price_float:,.2f}"
    except ValueError:
        return price_str

def validate_url(url):
    """Basic URL validation"""
    if not url:
        return True
    
    # Add protocol if missing
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    # Basic validation
    return '.' in url and len(url) > 4

def format_social_url(username, platform):
    """Format social media URL from username"""
    if not username:
        return ""
    
    # Remove @ symbol if present
    username = username.lstrip('@')
    
    if platform == 'instagram':
        return f"https://instagram.com/{username}"
    elif platform == 'facebook':
        return f"https://facebook.com/{username}"
    
    return username

def sanitize_filename(filename):
    """Sanitize filename for safe storage"""
    if not filename:
        return ""
    
    # Remove path components
    filename = os.path.basename(filename)
    
    # Replace unsafe characters
    unsafe_chars = '<>:"/\\|?*'
    for char in unsafe_chars:
        filename = filename.replace(char, '_')
    
    return filename

def resize_image(image_path, max_width=800, max_height=600, quality=85):
    """Resize image while maintaining aspect ratio"""
    try:
        with Image.open(image_path) as img:
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            # Calculate new size
            img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
            
            # Save optimized image
            img.save(image_path, 'JPEG', optimize=True, quality=quality)
            
            return True
    except Exception as e:
        logging.error(f"Error resizing image {image_path}: {e}")
        return False

def create_qr_code(data, size=10, border=4):
    """Create QR code image"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    return qr.make_image(fill_color="black", back_color="white")

def format_phone(phone):
    """Format phone number for display"""
    if not phone:
        return ""
    
    # Remove all non-numeric characters
    digits = ''.join(c for c in phone if c.isdigit())
    
    # Format based on length
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11 and digits[0] == '1':
        return f"+1 ({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
    else:
        return phone

def truncate_text(text, max_length=100):
    """Truncate text with ellipsis"""
    if not text or len(text) <= max_length:
        return text
    
    return text[:max_length-3] + "..."

def get_file_extension(filename):
    """Get file extension in lowercase"""
    if not filename or '.' not in filename:
        return ""
    
    return filename.rsplit('.', 1)[1].lower()

def is_valid_image_extension(filename):
    """Check if file has valid image extension"""
    valid_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    return get_file_extension(filename) in valid_extensions

def format_datetime(dt_string):
    """Format datetime string for display"""
    try:
        dt = datetime.fromisoformat(dt_string.replace('Z', '+00:00'))
        return dt.strftime('%d/%m/%Y %H:%M')
    except:
        return dt_string

def calculate_menu_stats(menu):
    """Calculate statistics for a menu"""
    total_sections = len(menu.get('sections', []))
    total_dishes = sum(len(section.get('dishes', [])) for section in menu.get('sections', []))
    
    return {
        'total_sections': total_sections,
        'total_dishes': total_dishes,
        'has_images': any(
            dish.get('image') 
            for section in menu.get('sections', []) 
            for dish in section.get('dishes', [])
        )
    }

def backup_data(data, backup_dir='backups'):
    """Create a backup of the data"""
    os.makedirs(backup_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = os.path.join(backup_dir, f'restaurants_backup_{timestamp}.json')
    
    try:
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return backup_file
    except Exception as e:
        logging.error(f"Error creating backup: {e}")
        return None
