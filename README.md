# 🏭 Jai Durga Plastic – Manufacturing Website

[![Django](https://img.shields.io/badge/Django-5.1-092E20?style=flat&logo=django)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Proprietary-red.svg)](LICENSE)
[![Responsive](https://img.shields.io/badge/Responsive-Yes-28a745)]()

> A complete, production-ready Django web application for **Jai Durga Plastic** – a leading manufacturer of premium plastic granules, spools, tubes, and molded articles.

![Hero Section Preview](https://via.placeholder.com/1200x600/1e3a8a/ffffff?text=Jai+Durga+Plastic+Website)

---

## 📖 Table of Contents

- [About The Project](#-about-the-project)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation & Setup](#-installation--setup)
- [Environment Variables](#-environment-variables)
- [Email Configuration](#-email-configuration)
- [Running the Application](#-running-the-application)
- [Admin Panel](#-admin-panel)
- [Screenshots](#-screenshots)
- [Responsive Design](#-responsive-design)
- [Contributing](#-contributing)
- [License](#-license)
- [Acknowledgements](#-acknowledgements)

---

## 🏗️ About The Project

**Jai Durga Plastic** is a complete digital presence for a plastic manufacturing company. Built with Django, this platform serves as both a **corporate website** and a **business tool** – enabling customers to explore products, submit enquiries, place orders, and connect with the sales team.

The platform is designed with a **mobile-first approach**, ensuring a seamless experience across all devices – from desktop computers to smartphones.

### Why This Project?

- ✅ **Modern UI/UX** – Clean, professional design with dark/light mode.
- ✅ **Business Ready** – Fully functional enquiry and order management.
- ✅ **Scalable** – Built on Django, ready for production deployment.
- ✅ **Customizable** – Easy to extend with new features or integrate with existing systems.

---

## ⭐ Key Features

| Feature | Description |
|---------|-------------|
| **Dynamic Homepage** | Hero video background, company intro, product highlights, and a “Why Choose Us” section with 3D flip cards |
| **Product Showcase** | Display of HDPE, LDPE, PP, and recycled granules with pricing and quick enquiry buttons |
| **Order Management** | Full‑fledged cart system with add/update/remove functionality, integrated with a dedicated order form |
| **Quick Enquiry Form** | AJAX‑based form with client‑side validation, CSRF protection, and toast notifications |
| **Dark / Light Mode** | Persistent theme toggle using `localStorage` – remembers user preference |
| **Responsive Design** | Mobile‑first layout that adapts to tablets, desktops, and all screen sizes |
| **Admin Panel** | Custom Django admin for managing enquiries, orders, products, and logs |
| **Email Notifications** | Automated emails to admin and customers upon enquiry submission |
| **WhatsApp Floating Button** | Instant chat support with a single click |
| **SEO Friendly** | Clean URLs, semantic HTML, and meta tags for better search visibility |

---

## 🛠️ Tech Stack

| Category | Technology | Version |
|----------|------------|---------|
| **Backend** | Django | 5.1 |
| **Language** | Python | 3.10+ |
| **Database** | SQLite (Dev) / MySQL (Prod) | – |
| **Frontend** | HTML5, CSS3, JavaScript | – |
| **Icons** | Font Awesome | 6.5 |
| **Email** | Django SMTP (Gmail / SMTP) | – |
| **Version Control** | Git & GitHub | – |
| **Deployment** | (Your preferred platform) | – |

---

## 📁 Project Structure

danamill/
│
├── danamill/ # Project configuration
│ ├── settings.py # Django settings (with environment variables)
│ ├── urls.py # Main URL routing
│ └── wsgi.py # WSGI entry point
│
├── apps/ # Core application
│ ├── models.py # Enquiry & EnquiryLog models
│ ├── views.py # Page views & API endpoints
│ ├── forms.py # Form validation
│ ├── utils.py # Email utilities
│ └── admin.py # Custom admin interface
│
├── cart/ # Shopping cart app
│ ├── models.py # Cart & CartItem models
│ ├── views.py # Cart logic (add, update, remove)
│ ├── urls.py # Cart routes
│ └── context_processors.py # Cart count for templates
│
├── order/ # Order form app
│ ├── models.py # Order models
│ ├── views.py # Order processing
│ └── urls.py # Order routes
│
├── static/ # Static assets
│ ├── css/ # Stylesheets (header, footer, home, etc.)
│ ├── js/ # JavaScript (header, home, footer, etc.)
│ └── images/ # Logo and static images
│
├── templates/ # Django templates
│ ├── partials/ # Reusable components
│ │ ├── header.html
│ │ ├── footer.html
│ │ └── navbar.html
│ ├── home.html
│ ├── about.html
│ ├── products.html
│ ├── contact.html
│ └── ...
│
├── media/ # User-uploaded content
│ ├── images/ # Product images, banners
│ └── videos/ # Hero background video
│
├── manage.py # Django CLI entry point
├── requirements.txt # Python dependencies
├── .env # Environment variables (not committed)
└── .gitignore # Git ignore rules




---

## 🚀 Installation & Setup

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Git (optional, for cloning)

### Step 1 – Clone the Repository

```bash
git clone https://github.com/yourusername/danamill.git
cd danamill
