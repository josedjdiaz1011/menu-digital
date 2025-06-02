import os
import json
import logging
from datetime import datetime
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory, jsonify
from PIL import Image
import qrcode
from io import BytesIO
import base64
import uuid

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default_secret_key_for_dev")

# Configuration
UPLOAD_FOLDER = 'uploads'
QR_FOLDER = 'qr_codes'
DATA_FILE = 'data/restaurants.json'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
ACCESS_CODE = "73961"

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(QR_FOLDER, exist_ok=True)
os.makedirs('data', exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_data():
    """Load restaurant data from JSON file"""
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_data(data):
    """Save restaurant data to JSON file"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def generate_qr_code(url, restaurant_id):
    """Generate QR code for restaurant menu"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    filename = f"{restaurant_id}_qr.png"
    filepath = os.path.join(QR_FOLDER, filename)
    img.save(filepath)
    return filename

def process_image(file):
    """Process and resize uploaded image"""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Add timestamp to avoid conflicts
        name, ext = os.path.splitext(filename)
        filename = f"{name}_{int(datetime.now().timestamp())}{ext}"
        
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        
        # Resize image
        image = Image.open(file)
        # Resize to max 800x600 while maintaining aspect ratio
        image.thumbnail((800, 600), Image.Resampling.LANCZOS)
        image.save(filepath, optimize=True, quality=85)
        
        return filename
    return None

@app.route('/')
def index():
    """Landing page - redirect to login"""
    if 'authenticated' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Authentication page"""
    if request.method == 'POST':
        code = request.form.get('access_code')
        if code == ACCESS_CODE:
            session['authenticated'] = True
            flash('¡Acceso exitoso!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Código de acceso incorrecto', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    flash('Sesión cerrada exitosamente', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    """Main dashboard showing all restaurants"""
    if 'authenticated' not in session:
        return redirect(url_for('login'))
    
    data = load_data()
    restaurants = list(data.values())
    
    return render_template('dashboard.html', restaurants=restaurants)

@app.route('/restaurant/new', methods=['GET', 'POST'])
def new_restaurant():
    """Create new restaurant"""
    if 'authenticated' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        data = load_data()
        
        # Generate unique ID
        restaurant_id = str(uuid.uuid4())[:8]
        
        # Process logo upload
        logo_filename = None
        if 'logo' in request.files:
            logo_file = request.files['logo']
            logo_filename = process_image(logo_file)
        
        # Create restaurant data
        restaurant = {
            'id': restaurant_id,
            'name': request.form.get('name', ''),
            'description': request.form.get('description', ''),
            'logo': logo_filename,
            'address': request.form.get('address', ''),
            'phone': request.form.get('phone', ''),
            'email': request.form.get('email', ''),
            'whatsapp': request.form.get('whatsapp', ''),
            'instagram': request.form.get('instagram', ''),
            'facebook': request.form.get('facebook', ''),
            'tiktok': request.form.get('tiktok', ''),
            'website': request.form.get('website', ''),
            'created_at': datetime.now().isoformat(),
            'visits': 0,
            'menu': {
                'sections': []
            }
        }
        
        data[restaurant_id] = restaurant
        save_data(data)
        
        # Generate QR code
        menu_url = url_for('view_menu', restaurant_id=restaurant_id, _external=True)
        generate_qr_code(menu_url, restaurant_id)
        
        flash(f'Restaurante "{restaurant["name"]}" creado exitosamente', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('restaurant_form.html')

@app.route('/restaurant/<restaurant_id>/edit', methods=['GET', 'POST'])
def edit_restaurant(restaurant_id):
    """Edit restaurant details"""
    if 'authenticated' not in session:
        return redirect(url_for('login'))
    
    data = load_data()
    if restaurant_id not in data:
        flash('Restaurante no encontrado', 'error')
        return redirect(url_for('dashboard'))
    
    restaurant = data[restaurant_id]
    
    if request.method == 'POST':
        # Process logo upload
        if 'logo' in request.files and request.files['logo'].filename:
            logo_file = request.files['logo']
            logo_filename = process_image(logo_file)
            if logo_filename:
                restaurant['logo'] = logo_filename
        
        # Update restaurant data
        restaurant.update({
            'name': request.form.get('name', ''),
            'description': request.form.get('description', ''),
            'address': request.form.get('address', ''),
            'phone': request.form.get('phone', ''),
            'email': request.form.get('email', ''),
            'whatsapp': request.form.get('whatsapp', ''),
            'instagram': request.form.get('instagram', ''),
            'facebook': request.form.get('facebook', ''),
            'tiktok': request.form.get('tiktok', ''),
            'website': request.form.get('website', ''),
            'updated_at': datetime.now().isoformat()
        })
        
        data[restaurant_id] = restaurant
        save_data(data)
        
        flash(f'Restaurante "{restaurant["name"]}" actualizado exitosamente', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('restaurant_form.html', restaurant=restaurant, edit_mode=True)

@app.route('/restaurant/<restaurant_id>/menu')
def edit_menu(restaurant_id):
    """Edit restaurant menu"""
    if 'authenticated' not in session:
        return redirect(url_for('login'))
    
    data = load_data()
    if restaurant_id not in data:
        flash('Restaurante no encontrado', 'error')
        return redirect(url_for('dashboard'))
    
    restaurant = data[restaurant_id]
    return render_template('menu_edit.html', restaurant=restaurant)

@app.route('/restaurant/<restaurant_id>/menu/section', methods=['POST'])
def add_section(restaurant_id):
    """Add new menu section"""
    if 'authenticated' not in session:
        return redirect(url_for('login'))
    
    data = load_data()
    if restaurant_id not in data:
        flash('Restaurante no encontrado', 'error')
        return redirect(url_for('dashboard'))
    
    section_name = request.form.get('section_name', '').strip()
    if section_name:
        section = {
            'id': str(uuid.uuid4())[:8],
            'name': section_name,
            'dishes': []
        }
        data[restaurant_id]['menu']['sections'].append(section)
        save_data(data)
        flash(f'Sección "{section_name}" agregada exitosamente', 'success')
    
    return redirect(url_for('edit_menu', restaurant_id=restaurant_id))

@app.route('/restaurant/<restaurant_id>/menu/section/<section_id>/dish', methods=['POST'])
def add_dish(restaurant_id, section_id):
    """Add new dish to section"""
    if 'authenticated' not in session:
        return redirect(url_for('login'))
    
    data = load_data()
    if restaurant_id not in data:
        flash('Restaurante no encontrado', 'error')
        return redirect(url_for('dashboard'))
    
    # Process dish image
    image_filename = None
    if 'dish_image' in request.files:
        image_file = request.files['dish_image']
        image_filename = process_image(image_file)
    
    # Find section and add dish
    for section in data[restaurant_id]['menu']['sections']:
        if section['id'] == section_id:
            dish = {
                'id': str(uuid.uuid4())[:8],
                'name': request.form.get('dish_name', ''),
                'description': request.form.get('dish_description', ''),
                'price': request.form.get('dish_price', ''),
                'image': image_filename
            }
            section['dishes'].append(dish)
            save_data(data)
            flash(f'Platillo "{dish["name"]}" agregado exitosamente', 'success')
            break
    
    return redirect(url_for('edit_menu', restaurant_id=restaurant_id))

@app.route('/restaurant/<restaurant_id>/menu/section/<section_id>/delete', methods=['POST'])
def delete_section(restaurant_id, section_id):
    """Delete menu section"""
    if 'authenticated' not in session:
        return redirect(url_for('login'))
    
    data = load_data()
    if restaurant_id not in data:
        flash('Restaurante no encontrado', 'error')
        return redirect(url_for('dashboard'))
    
    sections = data[restaurant_id]['menu']['sections']
    data[restaurant_id]['menu']['sections'] = [s for s in sections if s['id'] != section_id]
    save_data(data)
    flash('Sección eliminada exitosamente', 'success')
    
    return redirect(url_for('edit_menu', restaurant_id=restaurant_id))

@app.route('/restaurant/<restaurant_id>/menu/dish/<dish_id>/delete', methods=['POST'])
def delete_dish(restaurant_id, dish_id):
    """Delete dish from menu"""
    if 'authenticated' not in session:
        return redirect(url_for('login'))
    
    data = load_data()
    if restaurant_id not in data:
        flash('Restaurante no encontrado', 'error')
        return redirect(url_for('dashboard'))
    
    # Find and remove dish
    for section in data[restaurant_id]['menu']['sections']:
        section['dishes'] = [d for d in section['dishes'] if d['id'] != dish_id]
    
    save_data(data)
    flash('Platillo eliminado exitosamente', 'success')
    
    return redirect(url_for('edit_menu', restaurant_id=restaurant_id))

@app.route('/restaurant/<restaurant_id>/qr')
def view_qr_codes(restaurant_id):
    """View QR codes for restaurant"""
    if 'authenticated' not in session:
        return redirect(url_for('login'))
    
    data = load_data()
    if restaurant_id not in data:
        flash('Restaurante no encontrado', 'error')
        return redirect(url_for('dashboard'))
    
    restaurant = data[restaurant_id]
    menu_url = url_for('view_menu', restaurant_id=restaurant_id, _external=True)
    qr_filename = f"{restaurant_id}_qr.png"
    
    # Regenerate QR code if it doesn't exist
    qr_path = os.path.join(QR_FOLDER, qr_filename)
    if not os.path.exists(qr_path):
        generate_qr_code(menu_url, restaurant_id)
    
    return render_template('qr_codes.html', restaurant=restaurant, menu_url=menu_url, qr_filename=qr_filename)

@app.route('/menu/<restaurant_id>')
def view_menu(restaurant_id):
    """Public menu view"""
    data = load_data()
    if restaurant_id not in data:
        return render_template('menu_view.html', error="Menú no encontrado")
    
    restaurant = data[restaurant_id]
    
    # Increment visit counter
    restaurant['visits'] = restaurant.get('visits', 0) + 1
    data[restaurant_id] = restaurant
    save_data(data)
    
    return render_template('menu_view.html', restaurant=restaurant)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/qr/<filename>')
def qr_file(filename):
    """Serve QR code files"""
    return send_from_directory(QR_FOLDER, filename)

@app.route('/restaurant/<restaurant_id>/delete', methods=['POST'])
def delete_restaurant(restaurant_id):
    """Delete restaurant"""
    if 'authenticated' not in session:
        return redirect(url_for('login'))
    
    data = load_data()
    if restaurant_id in data:
        restaurant_name = data[restaurant_id]['name']
        del data[restaurant_id]
        save_data(data)
        flash(f'Restaurante "{restaurant_name}" eliminado exitosamente', 'success')
    
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
