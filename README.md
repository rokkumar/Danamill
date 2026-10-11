# Jai Durga Plastic – Official Website

A modern, responsive Django web application for **Jai Durga Plastic**, a leading manufacturer of high-quality plastic granules. The site showcases products, infrastructure, quality standards, and includes a complete enquiry and order system.

---

## ✨ Features

- **Dynamic Homepage** – Hero video background, company intro, product highlights, and 3D flip cards
- **Product Showcase** – Display of HDPE, LDPE, PP, and Recycled Granules with pricing
- **Enquiry System** – AJAX-based form with validation, CSRF protection, and toast notifications
- **Order Management** – Full cart system with add/update/remove functionality
- **Dark / Light Mode** – Persistent theme toggle using localStorage
- **Fully Responsive** – Mobile-first design that works on all devices
- **Admin Panel** – Manage enquiries, orders, and product data
- **Email Notifications** – Automatic emails to admin and customers
- **WhatsApp Button** – Instant chat support

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| Backend | Django 6.0 |
| Language | Python 3.13+ |
| Database | PostgreSQL |
| Frontend | HTML5, CSS3, JavaScript |
| Icons | Font Awesome 6.5 |
| Email | Django SMTP (Gmail) |
| Deployment | Gunicorn + WhiteNoise |

---

## 📁 Project Structure
danamill/
├── danamill/ # Project settings
├── enquiry/ # Enquiry app
├── order/ # Order management
├── cart/ # Shopping cart
├── templates/ # HTML templates
│ ├── partials/ # Header, footer, navbar
│ └── *.html
├── static/ # CSS, JS, images
├── media/ # User uploads
├── manage.py
├── requirements.txt
└── .env

text

---

## 🚀 Installation & Setup

### Prerequisites

- Python 3.13+
- PostgreSQL 16+
- pip

### Step 1 – Clone the Repository

```bash
git clone https://github.com/yourusername/danamill.git
cd danamill
Step 2 – Create Virtual Environment
bash
python -m venv .venv
.venv\Scripts\Activate.ps1     # Windows
source .venv/bin/activate      # Mac/Linux
Step 3 – Install Dependencies
bash
pip install -r requirements.txt
Step 4 – Configure Environment Variables
Create a .env file in the project root:

ini
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=DanaMill
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
ADMIN_EMAIL=your-email@gmail.com
DEFAULT_FROM_EMAIL=Jai Durga Plastic <your-email@gmail.com>
Step 5 – Run Migrations
bash
python manage.py makemigrations
python manage.py migrate
Step 6 – Create Superuser
bash
python manage.py createsuperuser
Step 7 – Collect Static Files
bash
python manage.py collectstatic
Step 8 – Start the Server
bash
python manage.py runserver
Visit http://127.0.0.1:8000

📧 Email Setup (Gmail)
Enable 2-Factor Authentication on your Google account.

Generate an App Password (Security → App passwords).

Add the 16-character password to EMAIL_HOST_PASSWORD in .env.

🖥️ Admin Panel
Access the admin panel at: http://127.0.0.1:8000/admin/

Manage:

Customer enquiries

Orders

Cart items

Products

📱 Responsive Design
Optimised for all devices:

Device	Screen Size
Mobile	480px and below
Tablet	768px and below
Laptop	992px and below
Desktop	992px and above
📬 Contact
Channel	Details
Email	Jaidurgaplastic.hyd@gmail.com
Phone	+91 90329 38392
📄 License
This project is proprietary and intended exclusively for Jai Durga Plastic.