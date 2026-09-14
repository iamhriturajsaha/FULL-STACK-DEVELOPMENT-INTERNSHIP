# Full-Stack Development Internship Projects

This repository contains two full-stack web applications developed during a Full-Stack Development Internship. Both applications are built with **Django**, utilize **PostgreSQL** for data persistence, and are configured for serverless deployment on **Vercel**.

## 🚀 Live Demos

*   **E-Commerce Store (NOVA/FORM):** [https://full-stack-development-internship.vercel.app/](https://full-stack-development-internship.vercel.app/) *(Update this link if it changes)*
*   **Social Media Platform (NOIR):** [Add Live Link Here]

---

## 🛠️ Technology Stack

*   **Backend:** Python 3.12, Django 5.x
*   **Database:** PostgreSQL (Hosted on Neon)
*   **Hosting & CI/CD:** Vercel (Serverless Functions)
*   **Static Files:** WhiteNoise (for serving CSS/JS on Vercel Edge Network)
*   **Frontend:** HTML, CSS, JavaScript

---

## 🛍️ Project 1: E-Commerce Store (NOVA/FORM)

A premium, design-forward e-commerce platform offering a curated selection of lighting, furniture, and minimalist objects. 

### Features
*   **Product Catalog:** Browse products by categories (Lighting, Furniture, Objects, etc.) with detailed product views.
*   **Cart System:** Fully functional session-based shopping cart (add, remove, adjust quantities).
*   **Dynamic UI:** Clean, responsive, and minimalist frontend design.
*   **Automated Seeding:** Built-in Django command to populate the store with a realistic catalog and high-quality images.

---

## 📱 Project 2: Social Media Platform (NOIR)

A minimalist social media network designed for photographers, designers, and visual artists to share their work.

### Features
*   **User Authentication:** Registration, login, and secure session management.
*   **Profiles & Following:** User profiles with avatars and bios, plus the ability to follow other creators.
*   **Interactions:** Like and comment on posts dynamically.
*   **Feed Generation:** View a feed of posts based on chronological order and following graphs.
*   **Automated Seeding:** Built-in Django command to generate realistic users, posts, comments, and interactions.

---

## 💻 Local Development Setup

If you wish to run these projects locally, follow these steps:

### 1. Clone the repository
```bash
git clone https://github.com/iamhriturajsaha/FULL-STACK-DEVELOPMENT-INTERNSHIP.git
cd FULL-STACK-DEVELOPMENT-INTERNSHIP
```

### 2. Create a Virtual Environment (Optional but Recommended)
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
Navigate into the specific project folder (e.g., `E-Commerce Store`) and run:
```bash
cd "E-Commerce Store"
pip install -r requirements.txt
```

### 4. Database Setup
By default, the projects are configured to use a `DATABASE_URL` environment variable for PostgreSQL. 
*   To use a local SQLite database for quick testing, ensure no `DATABASE_URL` or `POSTGRES_URL` environment variables are set in your terminal.
*   Run database migrations:
```bash
python manage.py migrate
```

### 5. Seed the Database
Populate the database with realistic demo data:
*   **For E-Commerce Store:** `python manage.py seed_products`
*   **For Social Media Platform:** `python manage.py seed_demo`

### 6. Run the Development Server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your browser.

---

## ☁️ Deployment on Vercel

Both projects are natively configured for 1-click deployment on Vercel.

1.  Import the repository into Vercel as **two separate projects** (one pointing to the `E-Commerce Store` root directory, and the other pointing to `Social Media Platform`).
2.  In Vercel, navigate to the **Storage** tab for each project and add a **Neon Postgres** database.
3.  Vercel will automatically inject the required `DATABASE_URL` and `POSTGRES_URL` environment variables.
4.  The custom `build.sh` scripts in both directories will automatically handle installing dependencies, running database migrations, and executing the data-seeding commands during the build phase.
