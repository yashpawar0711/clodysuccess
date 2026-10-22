# Cloudy Success — Full-Stack Dynamic Web Agency Platform

> **Tagline:** Your Vision. Our Digital Solutions.  
> **Founder:** Yash Pawar (`pawaryash0711@gmail.com` | `+91 93560 47461`)

---

## ⚡ How to Run the Server

### Option 1: Python Django Command (Recommended)
```bash
python manage.py runserver
```
Visit in your browser:
- **Website:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Executive Admin Portal:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

### Option 2: npm Shortcut
```bash
npm run django
```

---

## 🔐 Admin Portal Credentials
- **URL:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
- **Username:** `admin`
- **Password:** `admin123`

---

## 🚀 Dynamic Features & Architecture

1. **Django Backend (`cloudysuccess_app/`, `agency/`)**:
   - Built with Django 6.0 and Python 3.14.
   - SQLite Database (`db.sqlite3`).
   - Clean MVC/MVT architecture.

2. **Database Models**:
   - `ProjectEnquiry`: Stores client leads (Name, Email, Phone, Service, Budget, Message, Status, IP, Timestamp).
   - `QuoteCalculation`: Records estimates configured on the interactive quote builder.
   - `PortfolioProject`: Dynamic projects rendered on the frontend and editable via the admin portal.
   - `FAQItem`: Dynamic FAQs manageable via admin.

3. **REST API Endpoints**:
   - `POST /api/enquiry/` — Receives and stores contact form submissions into SQLite.
   - `POST /api/quote/` — Saves user calculator scopes.
   - `GET /api/project/<slug>/` — Returns project details for case study modals.

4. **Frontend Integration**:
   - High-end dark glassmorphism design.
   - Constellation background canvas.
   - 3D card tilt & smooth cursor follower.
   - Interactive quote estimator with live WhatsApp integration.
   - Confetti celebration upon enquiry dispatch.
   - Founder photo of **Yash Pawar** integrated across the About section and Contact card.
