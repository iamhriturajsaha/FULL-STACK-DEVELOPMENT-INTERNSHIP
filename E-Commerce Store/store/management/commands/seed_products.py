"""
NOVA/FORM — Seed Products Management Command

Populates the database with 16 realistic products across 5 categories.
Uses high-quality Unsplash images with consistent visual style.

Usage: python manage.py seed_products
"""

from django.core.management.base import BaseCommand
from store.models import Category, Product


class Command(BaseCommand):
    help = 'Seed the database with NOVA/FORM product catalog'

    def handle(self, *args, **options):
        self.stdout.write('Seeding NOVA/FORM catalog...')

        # Create categories
        categories_data = [
            {'name': 'Lighting', 'slug': 'lighting', 'description': 'Sculptural light objects that define space.', 'order': 1},
            {'name': 'Furniture', 'slug': 'furniture', 'description': 'Essential forms for considered living.', 'order': 2},
            {'name': 'Objects', 'slug': 'objects', 'description': 'Everyday objects elevated through design.', 'order': 3},
            {'name': 'Accessories', 'slug': 'accessories', 'description': 'Refined details for the modern interior.', 'order': 4},
            {'name': 'Essentials', 'slug': 'essentials', 'description': 'Foundational pieces for any space.', 'order': 5},
        ]

        cats = {}
        for cat_data in categories_data:
            cat, created = Category.objects.update_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            cats[cat_data['slug']] = cat
            status = 'Created' if created else 'Updated'
            self.stdout.write(f'  {status} category: {cat.name}')

        # Product data with Unsplash images (stable, high-quality, royalty-free)
        products_data = [
            {
                'name': 'Arc Table Lamp',
                'slug': 'arc-table-lamp',
                'short_description': 'A sculptural arc of warm light, reimagined for the modern desk.',
                'description': 'The Arc Table Lamp draws inspiration from mid-century forms and contemporary minimalism. Its sweeping aluminum arm creates a graceful parabola, directing warm 2700K light precisely where needed. The weighted travertine base provides stability while adding material richness. Dimmable via a discreet touch sensor integrated into the base.\n\nDimensions: H 52cm × W 18cm × D 35cm\nMaterials: Brushed aluminum, travertine stone, LED module\nWeight: 3.2kg',
                'price': '285.00',
                'compare_at_price': '340.00',
                'category': cats['lighting'],
                'image': 'https://images.unsplash.com/photo-1517991104123-1d56a6e81ed9?w=800&q=80&auto=format',
                'secondary_image': 'https://images.unsplash.com/photo-1513506003901-1e6a229e2d15?w=800&q=80&auto=format',
                'stock_quantity': 15,
                'featured': True,
                'new_arrival': True,
            },
            {
                'name': 'Mono Chair',
                'slug': 'mono-chair',
                'short_description': 'A single-shell form that cradles the body with quiet confidence.',
                'description': 'The Mono Chair is a study in reduction. A single shell of molded oak plywood creates seat, back, and armrest in one continuous gesture. The result is a chair that feels inevitable — as though no other form could exist. Stacked for compact storage.\n\nDimensions: H 78cm × W 56cm × D 52cm\nSeat height: 45cm\nMaterials: Molded oak plywood, natural oil finish\nWeight: 5.8kg',
                'price': '445.00',
                'category': cats['furniture'],
                'image': 'https://images.unsplash.com/photo-1506439773649-6e0eb8cfb237?w=800&q=80&auto=format',
                'secondary_image': 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=800&q=80&auto=format',
                'stock_quantity': 8,
                'featured': True,
                'new_arrival': False,
            },
            {
                'name': 'Forma Vase',
                'slug': 'forma-vase',
                'short_description': 'Hand-formed ceramic with an intentionally imperfect silhouette.',
                'description': 'Each Forma Vase is individually hand-formed by ceramicist Yuki Tanaka in her Kyoto studio. The gentle asymmetry of each piece celebrates the beauty of the handmade — no two are identical. A matte reactive glaze creates depth and subtle color variation across the surface.\n\nDimensions: H 28cm × Ø 14cm\nMaterials: Stoneware clay, matte reactive glaze\nCare: Hand wash recommended',
                'price': '165.00',
                'category': cats['objects'],
                'image': 'https://images.unsplash.com/photo-1612196808214-b8e1d6145a8c?w=800&q=80&auto=format',
                'secondary_image': 'https://images.unsplash.com/photo-1578500494198-246f612d3b3d?w=800&q=80&auto=format',
                'stock_quantity': 22,
                'featured': True,
                'new_arrival': True,
            },
            {
                'name': 'Axis Desk Lamp',
                'slug': 'axis-desk-lamp',
                'short_description': 'Articulated precision lighting with three axes of rotation.',
                'description': 'The Axis Desk Lamp offers three points of articulation, allowing infinite positioning. Machined from solid brass with a matte black powder coat finish, each joint moves with satisfying, dampened resistance. The integrated LED provides 800 lumens of flicker-free task lighting.\n\nDimensions: H 45–65cm (adjustable) × Reach 40cm\nMaterials: Machined brass, powder-coated steel, LED module\nWeight: 2.8kg',
                'price': '320.00',
                'category': cats['lighting'],
                'image': 'https://images.unsplash.com/photo-1534105615256-13940a56ff44?w=800&q=80&auto=format',
                'secondary_image': 'https://images.unsplash.com/photo-1494438639946-1ebd1d20bf85?w=800&q=80&auto=format',
                'stock_quantity': 12,
                'featured': False,
                'new_arrival': True,
            },
            {
                'name': 'Fold Side Table',
                'slug': 'fold-side-table',
                'short_description': 'A single sheet of steel, folded into functional geometry.',
                'description': 'The Fold Side Table begins as a flat sheet of 3mm steel, precision-bent into a stable three-dimensional form. The result is a table that appears to defy physics — thin yet remarkably strong. Available in matte black or warm bronze powder coat.\n\nDimensions: H 45cm × W 40cm × D 40cm\nMaterials: Folded steel, powder-coat finish\nWeight: 6.5kg\nLoad capacity: 25kg',
                'price': '195.00',
                'category': cats['furniture'],
                'image': 'https://images.unsplash.com/photo-1532372576444-dda954194ad0?w=800&q=80&auto=format',
                'secondary_image': 'https://images.unsplash.com/photo-1530018607912-eff2daa1bac4?w=800&q=80&auto=format',
                'stock_quantity': 18,
                'featured': True,
                'new_arrival': False,
            },
            {
                'name': 'No. 01 Ceramic Bowl',
                'slug': 'no-01-ceramic-bowl',
                'short_description': 'The first in a numbered series of essential ceramic forms.',
                'description': 'No. 01 is the foundational piece in our numbered ceramics series — a wide, shallow bowl suited equally to a fruit display or a centerpiece. Slip-cast in porcelain with a semi-matte exterior and glossy interior glaze.\n\nDimensions: H 8cm × Ø 26cm\nMaterials: Porcelain, food-safe glaze\nCare: Dishwasher safe',
                'price': '85.00',
                'category': cats['objects'],
                'image': 'https://images.unsplash.com/photo-1610701596007-11502861dcfa?w=800&q=80&auto=format',
                'secondary_image': 'https://images.unsplash.com/photo-1565193566173-7a0ee3dbe261?w=800&q=80&auto=format',
                'stock_quantity': 30,
                'featured': False,
                'new_arrival': False,
            },
            {
                'name': 'Orbit Tray',
                'slug': 'orbit-tray',
                'short_description': 'An elliptical tray carved from a single block of marble.',
                'description': 'The Orbit Tray is CNC-milled from a solid block of Carrara marble, then hand-finished by our stone workshop in Tuscany. Its elliptical form and shallow walls create an elegant vessel for keys, jewelry, or as a serving piece.\n\nDimensions: 32cm × 22cm × H 3cm\nMaterials: Carrara marble\nWeight: 2.1kg\nCare: Wipe clean with damp cloth',
                'price': '145.00',
                'category': cats['accessories'],
                'image': 'https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?w=800&q=80&auto=format',
                'secondary_image': 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=800&q=80&auto=format',
                'stock_quantity': 14,
                'featured': True,
                'new_arrival': False,
            },
            {
                'name': 'Linear Mirror',
                'slug': 'linear-mirror',
                'short_description': 'A frameless mirror defined by a single brass accent line.',
                'description': 'The Linear Mirror strips away the traditional frame, replacing it with a single vertical brass accent that creates visual tension and draws the eye. The mirror appears to float, mounted 15mm from the wall via a concealed French cleat system.\n\nDimensions: H 120cm × W 60cm\nMaterials: Float glass mirror, solid brass accent, steel mounting\nWeight: 12kg',
                'price': '395.00',
                'compare_at_price': '450.00',
                'category': cats['accessories'],
                'image': 'https://images.unsplash.com/photo-1618220179428-22790b461013?w=800&q=80&auto=format',
                'secondary_image': 'https://images.unsplash.com/photo-1595428774223-ef52624120d2?w=800&q=80&auto=format',
                'stock_quantity': 6,
                'featured': False,
                'new_arrival': True,
            },
            {
                'name': 'Frame Stool',
                'slug': 'frame-stool',
                'short_description': 'An open oak frame supporting a woven Danish cord seat.',
                'description': 'The Frame Stool combines Japanese joinery techniques with Scandinavian material sensibility. The open oak frame is assembled without visible hardware, and the seat is hand-woven with 120 meters of natural Danish cord. It ages beautifully with use.\n\nDimensions: H 45cm × W 42cm × D 36cm\nMaterials: Solid white oak, natural Danish cord\nWeight: 4.2kg',
                'price': '265.00',
                'category': cats['furniture'],
                'image': 'https://images.unsplash.com/photo-1503602642458-232111445657?w=800&q=80&auto=format',
                'secondary_image': 'https://images.unsplash.com/photo-1581539250439-c96689b516dd?w=800&q=80&auto=format',
                'stock_quantity': 10,
                'featured': False,
                'new_arrival': False,
            },
            {
                'name': 'Halo Pendant Light',
                'slug': 'halo-pendant-light',
                'short_description': 'A ring of light suspended in space.',
                'description': 'The Halo Pendant creates an unbroken circle of warm, diffused light. The minimal aluminum ring houses an integrated LED strip behind a frosted polycarbonate diffuser, producing zero visible hotspots. Suspended by three ultra-thin steel cables that virtually disappear.\n\nDimensions: Ø 60cm × H 6cm\nCable length: Adjustable up to 200cm\nMaterials: Anodized aluminum, frosted polycarbonate, steel cable\nLight output: 2400 lumens, 2700K, dimmable',
                'price': '520.00',
                'category': cats['lighting'],
                'image': 'https://images.unsplash.com/photo-1524484485831-a92ffc0de03f?w=800&q=80&auto=format',
                'secondary_image': 'https://images.unsplash.com/photo-1540932239986-30128078f3c5?w=800&q=80&auto=format',
                'stock_quantity': 5,
                'featured': True,
                'new_arrival': True,
            },
            {
                'name': 'Plinth Coffee Table',
                'slug': 'plinth-coffee-table',
                'short_description': 'A monolithic slab of limestone that commands any room.',
                'description': 'The Plinth Coffee Table is cut from a single block of Portuguese limestone, preserving the natural fossil inclusions and subtle veining unique to each piece. Its intentionally oversized proportions create a sense of grounding permanence.\n\nDimensions: H 35cm × W 100cm × D 60cm\nMaterials: Portuguese limestone\nWeight: 85kg\nNote: Due to weight, white-glove delivery included',
                'price': '1250.00',
                'category': cats['furniture'],
                'image': 'https://images.unsplash.com/photo-1611269154421-4e27233ac5c7?w=800&q=80&auto=format',
                'secondary_image': 'https://images.unsplash.com/photo-1634712282287-14ed57b9cc89?w=800&q=80&auto=format',
                'stock_quantity': 3,
                'featured': True,
                'new_arrival': False,
            },
            {
                'name': 'Signal Bookend',
                'slug': 'signal-bookend',
                'short_description': 'Geometric brass bookends that elevate any shelf.',
                'description': 'The Signal Bookend is machined from a solid brass block into a precise geometric form. The substantial weight (1.4kg each) ensures your books stay upright. Sold as a set of two. Over time, the unlacquered brass develops a rich, living patina.\n\nDimensions: H 16cm × W 10cm × D 10cm (each)\nMaterials: Solid unlacquered brass\nWeight: 1.4kg each (2.8kg set)',
                'price': '125.00',
                'category': cats['accessories'],
                'image': 'https://images.unsplash.com/photo-1544457070-4cd773b4d71e?w=800&q=80&auto=format',
                'secondary_image': 'https://images.unsplash.com/photo-1481277542470-605612bd2d61?w=800&q=80&auto=format',
                'stock_quantity': 20,
                'featured': False,
                'new_arrival': True,
            },
            {
                'name': 'Reed Diffuser',
                'slug': 'reed-diffuser',
                'short_description': 'A hand-blown glass vessel holding our signature scent.',
                'description': 'Our Reed Diffuser combines a hand-blown borosilicate glass vessel with our signature No. 04 scent — notes of cedar, vetiver, and bergamot. The minimalist cylindrical form allows the amber liquid to become part of the decor. Lasts approximately 3 months.\n\nDimensions: H 22cm × Ø 6cm\nVolume: 200ml\nMaterials: Hand-blown borosilicate glass, natural rattan reeds\nScent: Cedar, vetiver, bergamot',
                'price': '68.00',
                'category': cats['essentials'],
                'image': 'https://images.unsplash.com/photo-1602028915047-37269d1a73f7?w=800&q=80&auto=format',
                'secondary_image': 'https://images.unsplash.com/photo-1595440982104-56a928266736?w=800&q=80&auto=format',
                'stock_quantity': 35,
                'featured': False,
                'new_arrival': False,
            },
            {
                'name': 'Linen Throw',
                'slug': 'linen-throw',
                'short_description': 'Stonewashed French linen in a perfectly imperfect drape.',
                'description': 'Our Linen Throw is woven from 100% French flax linen in a family-owned mill in Normandy. Each throw is individually stonewashed for an impossibly soft hand-feel from the first use. The raw, selvedge edges are left intentionally unfinished.\n\nDimensions: 180cm × 130cm\nMaterials: 100% French flax linen\nWeight: 650g\nCare: Machine wash cold, tumble dry low',
                'price': '135.00',
                'category': cats['essentials'],
                'image': 'https://images.unsplash.com/photo-1616627561950-9f746e330187?w=800&q=80&auto=format',
                'secondary_image': 'https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=800&q=80&auto=format',
                'stock_quantity': 25,
                'featured': False,
                'new_arrival': False,
            },
            {
                'name': 'Sphere Pendant',
                'slug': 'sphere-pendant',
                'short_description': 'A perfect opal glass sphere that softens any light.',
                'description': 'The Sphere Pendant is the purest possible form for a light fixture — a perfect sphere of hand-blown opal glass suspended from a slim brass rod. The glass evenly diffuses light in all directions, creating a warm, ambient glow without glare.\n\nDimensions: Ø 25cm\nRod length: 100cm (adjustable)\nMaterials: Hand-blown opal glass, solid brass\nLight: E27 socket, max 60W (LED recommended)',
                'price': '245.00',
                'category': cats['lighting'],
                'image': 'https://images.unsplash.com/photo-1513506003901-1e6a229e2d15?w=800&q=80&auto=format',
                'secondary_image': 'https://images.unsplash.com/photo-1517991104123-1d56a6e81ed9?w=800&q=80&auto=format',
                'stock_quantity': 9,
                'featured': True,
                'new_arrival': False,
            },
            {
                'name': 'Stone Coaster Set',
                'slug': 'stone-coaster-set',
                'short_description': 'Four travertine coasters with cork backing.',
                'description': 'Our Stone Coaster Set features four individually selected travertine discs, each with unique natural patterning. The underside is fitted with a precision-cut cork pad to protect surfaces. Packaged in a linen-lined box, making them an ideal gift.\n\nDimensions: Ø 10cm × H 0.8cm (each)\nMaterials: Natural travertine, cork\nSet: 4 coasters\nCare: Wipe clean, seal annually with stone sealer',
                'price': '55.00',
                'category': cats['essentials'],
                'image': 'https://images.unsplash.com/photo-1616046229478-9901c5536a45?w=800&q=80&auto=format',
                'secondary_image': 'https://images.unsplash.com/photo-1583847268964-b28dc8f51f92?w=800&q=80&auto=format',
                'stock_quantity': 40,
                'featured': False,
                'new_arrival': True,
            },
        ]

        for product_data in products_data:
            product, created = Product.objects.update_or_create(
                slug=product_data['slug'],
                defaults=product_data
            )
            status = 'Created' if created else 'Updated'
            self.stdout.write(f'  {status} product: {product.name}')

        self.stdout.write(self.style.SUCCESS(
            f'\nDone! {len(categories_data)} categories and {len(products_data)} products seeded.'
        ))
