# NOVA/FORM

**Contemporary objects for people who appreciate design.**

A premium, Awwwards-level e-commerce website built with Django, featuring sophisticated UI/UX design, cinematic animations, and full e-commerce functionality.

![NOVA/FORM](https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?w=1200&q=80&auto=format)

---

## Features

- **Product Catalog** — 16 curated products across 5 categories with editorial grid layout
- **Shopping Cart** — Session-backed cart with AJAX operations and slide-out drawer
- **Checkout & Orders** — Atomic order processing with server-side validation
- **Authentication** — Registration, login/logout with custom styled forms
- **Account Dashboard** — Order history and order details
- **Search** — Full-text search across products, descriptions, and categories
- **Responsive Design** — Optimized for 320px to 1920px+
- **GSAP Animations** — Cinematic hero entrance, scroll reveals, parallax
- **Custom Cursor** — Context-aware cursor with product card interaction
- **Accessibility** — Semantic HTML, keyboard navigation, reduced-motion support
- **SEO** — Meta tags, Open Graph, semantic headings, canonical URLs

---

## Tech Stack

- **Backend**: Python 3.10+, Django 5.x, SQLite (PostgreSQL-ready)
- **Frontend**: Semantic HTML5, CSS3, Vanilla JavaScript
- **Animations**: GSAP + ScrollTrigger (via CDN)
- **Typography**: Cormorant Garamond + Inter (Google Fonts)

---

## Quick Start

### 1. Clone & Setup Virtual Environment

```bash
cd Project
python -m venv venv

# Windows
.\venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Database Setup

```bash
python manage.py migrate
python manage.py seed_products
```

### 4. Create Superuser (for admin access)

```bash
python manage.py createsuperuser
```

### 5. Run Development Server

```bash
python manage.py runserver
```

Visit: [http://127.0.0.1:8000](http://127.0.0.1:8000)

Admin: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

### 6. Run Tests

```bash
python manage.py test store -v 2
```

---

## Project Structure

```
Project/
├── config/              # Django project settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── store/               # Main application
│   ├── models.py        # Category, Product, Order, OrderItem
│   ├── views.py         # All page and API views
│   ├── services.py      # Cart & Order business logic
│   ├── forms.py         # Registration, Login, Checkout forms
│   ├── admin.py         # Rich admin configuration
│   ├── context_processors.py  # Global cart & site context
│   ├── urls.py          # URL routing
│   ├── tests.py         # 30+ test cases
│   ├── templatetags/    # Custom template filters
│   └── management/      # seed_products command
├── templates/           # Django templates
│   ├── base.html        # Master layout
│   ├── home.html        # Homepage with hero
│   ├── shop.html        # Product catalog
│   ├── product_detail.html
│   ├── cart.html
│   ├── checkout.html
│   ├── order_success.html
│   ├── login.html
│   ├── register.html
│   ├── account.html
│   ├── order_detail.html
│   ├── about.html
│   ├── search.html
│   └── 404.html
├── static/
│   ├── css/             # Design system
│   │   ├── variables.css    # Design tokens
│   │   ├── reset.css        # CSS reset
│   │   ├── global.css       # Typography & layout
│   │   ├── components.css   # UI components
│   │   ├── pages.css        # Page layouts
│   │   └── responsive.css   # Breakpoints
│   └── js/              # Modular JavaScript
│       ├── main.js          # App init & loading
│       ├── navigation.js    # Navbar & mobile menu
│       ├── animations.js    # GSAP animations
│       ├── cart.js          # AJAX cart operations
│       ├── product.js       # Gallery & interactions
│       ├── cursor.js        # Custom cursor
│       └── utils.js         # Utilities & toasts
├── manage.py
├── requirements.txt
├── .gitignore
└── .env.example
```

---

## Design System

| Token | Value |
|-------|-------|
| Background | `#FAF8F5` (warm off-white) |
| Text | `#1A1A1A` (near-black) |
| Accent | `#8B6F4E` (warm bronze) |
| Display Font | Cormorant Garamond |
| Body Font | Inter |
| Transitions | 200ms / 400ms / 700ms |

---

## Production Considerations

1. **Database**: Switch to PostgreSQL via `DATABASE_URL` environment variable
2. **Static Files**: Run `python manage.py collectstatic` and serve via nginx/CDN
3. **Security**: Set `DEBUG=False`, configure `ALLOWED_HOSTS`, use strong `SECRET_KEY`
4. **HTTPS**: Enable `SECURE_SSL_REDIRECT` and related settings
5. **Images**: Host product images on a CDN for production reliability

---

## License

This project is for educational purposes. NOVA/FORM is a fictional brand.
