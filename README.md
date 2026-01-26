# Ajei Project - Django Landing Pages

## ✅ Completed Setup

### 1. Django Rosetta & i18n Configuration
- ✅ Django Rosetta installed for translation management
- ✅ English (en) and Arabic (ar) language support
- ✅ LocaleMiddleware configured for language switching
- ✅ Locale directories created

### 2. Django Constance - Dynamic Settings
- ✅ Django Constance installed for runtime configuration
- ✅ Database backend configured for storing settings
- ✅ Organized settings groups:
  - **General**: Site name, description, maintenance mode
  - **Contact**: Email, phone, WhatsApp, location
  - **Social**: Facebook URL
  - **Maps & Analytics**: Google Maps, Analytics ID
  - **Features**: Contact form toggle
- ✅ Accessible via `/admin/constance/config/`

### 3. Contact Form Model & Admin
- ✅ ContactSubmission model created with comprehensive fields
- ✅ Professional admin interface features:
  - Status badges with colors (new, contacted, qualified, converted, closed)
  - Investment type icons (🏥 medical, 🏢 commercial, 💊 pharmacy, etc.)
  - Bulk actions for status management
  - Advanced search and filtering
  - Organized fieldsets for better UX
  - IP tracking and user agent logging

### 4. Views Created
Three views have been created in [ajei/views.py](ajei/views.py):
- `ajei_landing_page()` - Main landing page (root URL: `/`)
- `ajei_page()` - Alternative Ajei page (URL: `/ajei/`)
- `ajei_contact_submit()` - Contact form submission handler

### 5. URL Configuration
Updated [config/urls.py](config/urls.py) with routes:
- `/` - Main landing page (ajei_landing.html)
- `/ajei/` - Alternative page (ajei.html)
- `/contact/submit/` - Contact form submission
- `/admin/` - Django admin panel
- `/admin/constance/config/` - Dynamic settings management
- `/rosetta/` - Translation management interface

### 4. Static Files & Media Configuration
- ✅ `STATIC_URL`, `STATIC_ROOT`, `STATICFILES_DIRS` configured
- ✅ `STATICFILES_FINDERS` set up for file discovery
- ✅ `MEDIA_URL` and `MEDIA_ROOT` configured
- ✅ Static and media file serving enabled in DEBUG mode

### 6. Template Updates
Updated [templates/landing_page/ajei_landing.html](templates/landing_page/ajei_landing.html) to use images from [static/images](static/images):
- Hero background: `ajei-background-5-min.png`
- Logo images: `ajei_logo.png`
- About section: `ajei-background-3-min.png`
- Video poster: `ajei-background-4-min.png`
- All favicon and meta tags updated

### 7. Database Models
- ✅ ContactSubmission model with full tracking
- ✅ Migrations created and applied
- ✅ Admin interface configured

## 📁 Project Structure

```
ajei_project/
├── ajei/               # Main app
│   ├── models.py       # ContactSubmission model
│   ├── views.py        # Landing page views & form handler
│   ├── admin.py        # Admin interface configuration
│   └── migrations/     # Database migrations
├── config/             # Project settings
│   ├── settings.py     # Configuration + Constance setup
│   ├── urls.py         # URL routing
│   └── ...
├── templates/          # HTML templates
│   └── landing_page/
│       ├── ajei_landing.html
│       └── ajei.html
├── static/             # Static files
│   ├── images/         # Image assets
│   ├── css/
│   ├── js/
│   └── pdf/
├── media/              # User uploads
├── locale/             # Translation files
│   ├── en/
│   └── ar/
└── manage.py
```

## 🚀 Getting Started

### Create Superuser (First Time Setup)
```bash
pipenv run python manage.py createsuperuser
```

### Run Development Server
```bash
pipenv run python manage.py runserver
```

### Access the Pages
- **Main Landing**: http://localhost:8000/
- **Alternative Page**: http://localhost:8000/ajei/
- **Admin Panel**: http://localhost:8000/admin/
  - View contact submissions
  - Manage submission status
  - Add admin notes
- **Dynamic Settings**: http://localhost:8000/admin/constance/config/
  - Update site constants without code changes
  - Toggle features on/off
- **Rosetta (Translations)**: http://localhost:8000/rosetta/

### Generate Translation Files
```bash
pipenv run python manage.py makemessages -l ar
pipenv run python manage.py compilemessages
```

### Database Migrations
```bash
pipenv run python manage.py makemigrations
pipenv run python manage.py migrate
```

### Collect Static Files (for production)
```bash
pipenv run python manage.py collectstatic
```

## 🔧 Dynamic Settings (Constance)

You can now manage these settings from the admin panel without code changes:

### General Settings
- `SITE_NAME` - Name of the site
- `SITE_DESCRIPTION` - Site description
- `MAINTENANCE_MODE` - Enable/disable maintenance mode

### Contact Information
- `CONTACT_EMAIL` - Contact email address
- `CONTACT_PHONE` - Contact phone number
- `WHATSAPP_NUMBER` - WhatsApp number
- `LOCATION_ADDRESS` - Project location

### Features
- `ENABLE_CONTACT_FORM` - Enable/disable contact form submissions

### Social & Analytics
- `FACEBOOK_URL` - Facebook page URL
- `GOOGLE_MAPS_EMBED` - Google Maps embed URL
- `GOOGLE_ADS_ID` - Google Analytics/Ads ID

## 📊 Contact Form Management

### Admin Features
- **Status Tracking**: New → Contacted → Qualified → Converted → Closed
- **Bulk Actions**: Change status for multiple submissions at once
- **Investment Type Icons**: Visual indicators for different investment types
- **Search & Filter**: Find submissions by name, email, phone, or message
- **Admin Notes**: Add private notes to each submission
- **IP Tracking**: View submitter's IP address and user agent

### Workflow
1. User submits contact form on landing page
2. Submission saved to database with status "New"
3. Admin reviews in admin panel
4. Mark as "Contacted" with timestamp
5. Progress through: Qualified → Converted → Closed

## 🌐 Language Switching
Both templates support language switching via URL parameter:
- English: `/?lang=en`
- Arabic: `/?lang=ar`

## 📸 Available Images
The project includes various images in [static/images](static/images):
- `ajei_logo.png` - Main logo
- `ajei-background-*.png` - Background images (2-6)
- `ajei_video.mp4` - Project video
- `extorior/` - Exterior renderings
- `interior/` - Interior renderings
- Various floor plans and logos

## 🔧 Configuration
All settings are in [config/settings.py](config/settings.py):
- Languages: English and Arabic
- Template directories configured
- Context processors enabled for i18n
- Static and media file paths set up
