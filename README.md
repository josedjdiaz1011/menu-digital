# Sistema de Menú Digital

Un sistema completo de menús digitales para restaurantes con autenticación de usuarios, gestión de menús, códigos QR y personalización de marca.

## ✨ Características

- 🔐 **Autenticación segura** con código de acceso
- 🏪 **Gestión completa de restaurantes** con información de contacto y redes sociales
- 📱 **Redes sociales integradas**: WhatsApp, Instagram, Facebook, TikTok
- 🍽️ **Gestión completa de menús** con secciones desplegables
- ⚡ **Edición en tiempo real** de secciones y platillos
- 📱 **Menús desplegables** para mejor navegación móvil
- 🔗 **Códigos QR automáticos** para cada menú
- 🎨 **Personalización de marca** con logo y redes sociales
- 📱 **Diseño responsive** optimizado para móviles
- 🖼️ **Subida de imágenes** para platillos y logos
- 📊 **Estadísticas de visitas** simples
- 🔗 **Enlaces únicos** para cada restaurante

## 🚀 Tecnologías

- **Backend**: Flask (Python 3.11)
- **Frontend**: Bootstrap 5, JavaScript vanilla
- **Base de datos**: JSON (fácil migración a PostgreSQL)
- **Imágenes**: Pillow, QRCode
- **Servidor**: Gunicorn

## 📋 Instalación Local

1. **Clonar el repositorio**
```bash
git clone https://github.com/tu-usuario/menu-digital.git
cd menu-digital
```

2. **Crear entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -e .
```

4. **Configurar variables de entorno**
```bash
export SESSION_SECRET="tu-clave-secreta-aqui"
```

5. **Ejecutar la aplicación**
```bash
python main.py
```

6. **Acceder a la aplicación**
- Abre tu navegador en `http://localhost:5000`
- Usa el código de acceso: `73961`

## 🌐 Despliegue Gratuito en Render

### Infraestructura y Alojamiento Gratuito 24/7

Este proyecto está configurado para desplegarse automáticamente en **Render** conectado con **GitHub**, proporcionando:

- ✅ **Hosting gratuito** 24/7
- ✅ **Actualización automática** desde GitHub
- ✅ **SSL/HTTPS** incluido
- ✅ **Dominio personalizable**
- ✅ **Escalabilidad automática**

### Pasos para el despliegue:

1. **Subir a GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/tu-usuario/menu-digital.git
git push -u origin main
```

2. **Configurar en Render**
   - Ve a [render.com](https://render.com)
   - Conecta tu cuenta de GitHub
   - Selecciona el repositorio `menu-digital`
   - Render detectará automáticamente el `render.yaml`

3. **Variables de entorno (automáticas)**
   - `SESSION_SECRET`: Se genera automáticamente
   - `PYTHON_VERSION`: 3.11.0

4. **Despliegue automático**
   - Cada push a `main` despliega automáticamente
   - El proyecto estará disponible en: `https://tu-app.onrender.com`

## 📝 Uso del Sistema

### Código de Acceso
- **Código**: `73961`
- Usado para acceder al panel de administración

### Gestión de Restaurantes
1. **Crear restaurante**: Información básica, logo, contacto
2. **Redes sociales**: WhatsApp, Instagram, Facebook, TikTok
3. **Menú**: Agregar secciones y platillos con imágenes

### Menús Públicos
- **Secciones desplegables** para mejor navegación
- **Responsive** para móviles
- **Enlaces directos** vía QR o URL

### Códigos QR
- **Generación automática** para cada restaurante
- **Descarga** en formato PNG
- **Impresión** optimizada

## 🔧 Configuración Avanzada

### Personalización del Código de Acceso
Edita el archivo `app.py`:
```python
ACCESS_CODE = "tu-nuevo-codigo"
```

### Límites de Archivos
- **Imágenes**: Máximo 5MB
- **Formatos**: PNG, JPG, JPEG, GIF

### Estructura de Datos
```json
{
  "restaurant_id": {
    "name": "Nombre del Restaurante",
    "description": "Descripción",
    "logo": "logo.jpg",
    "phone": "+52 55 1234 5678",
    "email": "contacto@restaurante.com",
    "whatsapp": "52 55 1234 5678",
    "instagram": "usuario",
    "facebook": "usuario",
    "tiktok": "usuario",
    "website": "https://sitio.com",
    "menu": {
      "sections": [
        {
          "name": "Entradas",
          "dishes": [
            {
              "name": "Platillo",
              "description": "Descripción",
              "price": "25.99",
              "image": "platillo.jpg"
            }
          ]
        }
      ]
    }
  }
}
```

## 🎨 Características de Diseño

### Tema Oscuro
- Diseño moderno con tema oscuro
- Bootstrap 5 personalizado
- Iconos Font Awesome

### Mobile First
- Diseño responsive
- Optimizado para móviles
- Secciones desplegables

### Accesibilidad
- Contraste adecuado
- Navegación por teclado
- Textos alternativos

## 🔒 Seguridad

- **Autenticación** por código de acceso
- **Sanitización** de nombres de archivo
- **Validación** de tipos de archivo
- **Límites** de tamaño de archivo

## 📊 Analytics

### Estadísticas Incluidas
- **Visitas** por restaurante
- **Contadores** de secciones y platillos
- **Fecha** de creación y actualización

## 🛠️ Desarrollo

### Estructura del Proyecto
```
menu-digital/
├── app.py              # Aplicación principal
├── main.py             # Punto de entrada
├── models.py           # Modelos de datos
├── utils.py            # Utilidades
├── templates/          # Plantillas HTML
├── static/             # CSS y JavaScript
├── uploads/            # Imágenes subidas
├── qr_codes/          # Códigos QR generados
├── data/              # Datos JSON
├── render.yaml        # Configuración Render
└── Dockerfile         # Contenedor Docker
```

### Comandos de Desarrollo
```bash
# Modo desarrollo
python main.py

# Modo producción
gunicorn --bind 0.0.0.0:5000 main:app
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama: `git checkout -b feature/nueva-funcionalidad`
3. Commit: `git commit -m 'Agregar nueva funcionalidad'`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 🆘 Soporte

Para soporte técnico o preguntas:
- Abre un **Issue** en GitHub
- Consulta la **documentación**
- Revisa los **ejemplos** incluidos

---

**¡Empieza a digitalizar tus menús hoy mismo! 🚀**