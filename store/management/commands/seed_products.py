from django.core.management.base import BaseCommand
from store.models import Product
from decimal import Decimal

class Command(BaseCommand):
    help = 'Seeds database with 12 initial high-quality sample products across categories'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.MIGRATE_HEADING("Seeding initial products into database..."))

        SAMPLE_PRODUCTS = [
            {
                'name': 'Pro Ultra Smartphone 5G',
                'category': 'Electronics',
                'price': Decimal('74699.17'),
                'stock': 15,
                'description': 'Latest flagship 5G smartphone featuring a dynamic AMOLED display, triple camera setup, 120Hz refresh rate, all-day battery life, and ultra-fast charging.',
                'image_url': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=800&q=80'
            },
            {
                'name': 'Bazaar Slim Laptop 15"',
                'category': 'Electronics',
                'price': Decimal('107858.50'),
                'stock': 10,
                'description': 'High performance lightweight laptop powered by a modern 12-core processor, 16GB DDR5 RAM, 1TB NVMe SSD, and vivid Retina IPS screen.',
                'image_url': 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=800&q=80'
            },
            {
                'name': 'Aero Wireless ANC Headphones',
                'category': 'Electronics',
                'price': Decimal('16599.17'),
                'stock': 25,
                'description': 'Over-ear noise-cancelling headphones delivering rich spatial audio, deep bass, ergonomic memory foam cushions, and up to 40 hours playtime.',
                'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=800&q=80'
            },
            {
                'name': 'Smart Health Fitness Watch',
                'category': 'Electronics',
                'price': Decimal('12367.00'),
                'stock': 20,
                'description': 'Track heart rate, sleep quality, oxygen level, and sports modes with a sleek waterproof touch display and GPS tracking.',
                'image_url': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=800&q=80'
            },
            {
                'name': 'Premium Cotton Oxford Shirt',
                'category': 'Fashion',
                'price': Decimal('4149.17'),
                'stock': 30,
                'description': 'Classic tailored button-down shirt crafted from 100% breathable organic cotton. Suitable for casual and formal wear.',
                'image_url': 'https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?auto=format&fit=crop&w=800&q=80'
            },
            {
                'name': 'Denim Jacket Urban Edition',
                'category': 'Fashion',
                'price': Decimal('6635.85'),
                'stock': 18,
                'description': 'Timeless vintage denim jacket featuring durable stitching, dual chest pockets, and a comfy relaxed fit for all seasons.',
                'image_url': 'https://images.unsplash.com/photo-1576995853123-5a10305d93c0?auto=format&fit=crop&w=800&q=80'
            },
            {
                'name': 'Air-Sprint Athletic Running Shoes',
                'category': 'Shoes',
                'price': Decimal('9959.17'),
                'stock': 14,
                'description': 'Ultra lightweight cushioned sneakers engineered for maximum comfort, responsiveness, and airflow during daily runs.',
                'image_url': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=800&q=80'
            },
            {
                'name': 'Classic Leather Urban Sneakers',
                'category': 'Shoes',
                'price': Decimal('7387.00'),
                'stock': 12,
                'description': 'Minimalist handcrafted genuine leather sneakers with vulcanized rubber sole and padded insole for all-day comfort.',
                'image_url': 'https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?auto=format&fit=crop&w=800&q=80'
            },
            {
                'name': 'Minimalist Waterproof Backpack',
                'category': 'Accessories',
                'price': Decimal('5353.50'),
                'stock': 22,
                'description': 'Sleek commuting backpack with dedicated 15.6-inch laptop compartment, hidden anti-theft pocket, and water-repellent fabric.',
                'image_url': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=800&q=80'
            },
            {
                'name': 'Polarized Aviator Sunglasses',
                'category': 'Accessories',
                'price': Decimal('2904.17'),
                'stock': 40,
                'description': 'Stylish metallic frame aviators with UV400 protection and scratch-resistant polarized lenses for crystal clear vision.',
                'image_url': 'https://images.unsplash.com/photo-1511499767150-a48a237f0083?auto=format&fit=crop&w=800&q=80'
            },
            {
                'name': 'Portable Surround Sound Speaker',
                'category': 'Home',
                'price': Decimal('4979.17'),
                'stock': 16,
                'description': 'Compact Bluetooth 5.2 speaker with 360-degree bass surround sound, IPX7 waterproof rating, and 12-hour continuous battery life.',
                'image_url': 'https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?auto=format&fit=crop&w=800&q=80'
            },
            {
                'name': 'Ergonomic Desk LED Lamp',
                'category': 'Home',
                'price': Decimal('3486.00'),
                'stock': 25,
                'description': 'Adjustable dimmable LED table lamp with eye-caring technology, multiple color modes, wireless charging pad, and USB output.',
                'image_url': 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=800&q=80'
            },
        ]

        created_count = 0
        updated_count = 0

        for prod_data in SAMPLE_PRODUCTS:
            product, created = Product.objects.update_or_create(
                name=prod_data['name'],
                defaults=prod_data
            )
            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully seeded database! Created {created_count} products, updated {updated_count} products."
            )
        )
