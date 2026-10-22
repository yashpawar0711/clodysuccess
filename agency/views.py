import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from .models import ProjectEnquiry, QuoteCalculation, PortfolioProject, FAQItem, PricingTier


DEFAULT_PROJECTS = [
    {
        "slug": "corporate",
        "title": "Apex Horizon Capital",
        "category": "corporate",
        "category_label": "Corporate Business Website",
        "year": "2026 Production Standard",
        "image_url": "/static/assets/portfolio-corporate.jpg",
        "summary": "An institutional web presence designed for a boutique private equity and financial consulting firm with interactive data metrics and investor portal UX.",
        "description": "An institutional web presence designed for a boutique private equity and financial consulting firm. The project emphasizes executive credibility, clear client service pathways, and real-time interactive financial performance telemetry.",
        "highlights": [
            "Dark mode aesthetic with electric cyan data visualizations and custom growth metrics",
            "Intuitive investor portal UX with secure document request workflows",
            "Sub-1.2s average load performance across all global test locations",
            "Full lead-capture integration with automated email alerts and WhatsApp routing"
        ],
        "tech_stack": ["Vanilla HTML5", "High-Performance CSS", "Chart.js", "Responsive Grid", "SEO Schema"],
        "order": 1
    },
    {
        "slug": "restaurant",
        "title": "The Obsidian Room",
        "category": "restaurant",
        "category_label": "Hospitality & Fine Dining",
        "year": "2026 Production Standard",
        "image_url": "/static/assets/portfolio-restaurant.jpg",
        "summary": "Luxury gastronomic dining experience website with dark slate aesthetics, dynamic seasonal wine card, and table reservation booking flow.",
        "description": "A luxury fine-dining gastronomic showcase engineered with dark slate textures, ambient gold lighting, dynamic seasonal menu categorizations, and an integrated frictionless table reservation flow.",
        "highlights": [
            "Interactive culinary dish explorer with dietary filters (Vegan, Gluten-Free, Chef Special)",
            "Table reservation booking bar with instant guest count and date selection",
            "Mobile-first digital menu with touch-friendly navigation and wine pairings",
            "Zero layout shifts (CLS < 0.01) for seamless mobile dining reservations"
        ],
        "tech_stack": ["Custom CSS Tokens", "Touch Gestures", "Booking Engine UX", "Mobile Menu", "WebP Artistry"],
        "order": 2
    },
    {
        "slug": "portfolio",
        "title": "Aeterna Architecture",
        "category": "portfolio",
        "category_label": "Personal & Studio Portfolio",
        "year": "2026 Production Standard",
        "image_url": "/static/assets/portfolio-architect.jpg",
        "summary": "Minimalist Swiss-inspired architect portfolio featuring blueprints viewer, monochromatic gallery grid, and editorial typography.",
        "description": "A Swiss-inspired minimalist editorial portfolio designed for an award-winning architectural firm. The site allows spatial photography and floorplan blueprints to take center stage with refined typography and smooth transitions.",
        "highlights": [
            "Interactive architectural blueprint viewer and split-screen comparison mode",
            "Smooth gallery transitions and full-screen image lightboxes",
            "Editorial serif and mono typography pairing with high legibility",
            "Direct inquiry button with pre-selected project type"
        ],
        "tech_stack": ["Editorial Typography", "Parallax Scrolling", "Blueprint Lightbox", "CSS Grid", "Minimalist UI"],
        "order": 3
    },
    {
        "slug": "ecommerce",
        "title": "Velo Audio Elite",
        "category": "ecommerce",
        "category_label": "E-Commerce Storefront",
        "year": "2026 Production Standard",
        "image_url": "/static/assets/portfolio-ecommerce.jpg",
        "summary": "Direct-to-consumer premium audiophile storefront with interactive product 360 preview, one-click cart drawer, and review system.",
        "description": "A modern direct-to-consumer online storefront for high-end audiophile hardware. Engineered for high conversion with instant cart drawer previews, product color selectors, customer review carousels, and rapid checkout pathways.",
        "highlights": [
            "Instant sliding cart drawer with live subtotal and free shipping progress meter",
            "Interactive color variant toggles with smooth product asset swapping",
            "Secure multi-gateway payment architecture (Stripe, Razorpay, Apple Pay)",
            "Speed-tuned product grid with lazy loading and instant search"
        ],
        "tech_stack": ["E-Commerce Core", "Cart Drawer UX", "Payment Gateways", "Inventory Filter", "Conversion Funnel"],
        "order": 4
    },
    {
        "slug": "saas",
        "title": "Aurora Cloud Analytics",
        "category": "saas",
        "category_label": "SaaS Dashboard Web Application",
        "year": "2026 Production Standard",
        "image_url": "/static/assets/portfolio-saas.jpg",
        "summary": "Full-featured telemetry analytics web platform with dynamic charts, MRR metrics, real-time user activity maps, and dark UI system.",
        "description": "A futuristic telemetry and subscription analytics web app interface designed for SaaS startups. Features glowing neon charts, live MRR tracking, user cohort trends, churn probability monitoring, and role-based access management.",
        "highlights": [
            "Real-time data visualization with neon area charts and custom SVG tooltips",
            "Modular widget dashboard with customizable metric card arrangements",
            "High contrast dark UI complying with WCAG 2.1 accessibility standards",
            "Scalable component architecture ready for backend API hydration"
        ],
        "tech_stack": ["Single Page App", "Data Visualizations", "Custom SVG Charts", "Dark Mode UI", "API Ready"],
        "order": 5
    },
    {
        "slug": "agency",
        "title": "Nebula Digital Studio",
        "category": "agency",
        "category_label": "Creative Agency Website",
        "year": "2026 Production Standard",
        "image_url": "/static/assets/portfolio-agency.jpg",
        "summary": "Boundary-pushing motion-rich creative agency portfolio with electric cyan neon accents, 3D abstract models, and award-grade micro-interactions.",
        "description": "A boundary-pushing motion-heavy digital studio website designed to captivate prospective clients. Incorporates electric laser glows, 3D floating visual layers, magnetic button interactions, and award-winning micro-animations.",
        "highlights": [
            "Advanced CSS keyframe motion choreography and subtle layered depth",
            "Magnetic cursor hover physics on all primary call-to-actions",
            "Interactive project carousel with smooth keyboard and drag navigation",
            "Strictly optimized for 60fps rendering without memory leaks"
        ],
        "tech_stack": ["CSS Keyframes", "Magnetic Physics", "WebGL Ambience", "Fluid Typography", "Custom Motion"],
        "order": 6
    }
]


DEFAULT_PRICING_TIERS = [
    {
        "name": "Static Website",
        "tagline": "Fast, lightweight & responsive website for local shops, personal brands & portfolios",
        "price": "4,000",
        "currency_symbol": "₹",
        "period": "/ one-time estimate",
        "usd_equivalent": "Approx ~$49 USD • Fast 3-Day Delivery",
        "is_popular": False,
        "popular_badge_text": "",
        "features": [
            "1 to 5 Fast-Loading Pages",
            "100% Mobile & Tablet Responsive",
            "Blazing-Fast Loading (< 1.5s)",
            "Direct WhatsApp & Call Integration",
            "Contact Form with Email Routing",
            "Basic On-Page SEO & Google Meta Setup",
            "1 Month Support & Free Tweaks"
        ],
        "cta_text": "Select Static Plan",
        "order": 1
    },
    {
        "name": "Dynamic Website",
        "tagline": "Interactive, feature-rich & database-backed website for growing businesses",
        "price": "8,000",
        "currency_symbol": "₹",
        "period": "/ one-time estimate",
        "usd_equivalent": "Approx ~$99 USD • Best Value for Growth",
        "is_popular": True,
        "popular_badge_text": "MOST POPULAR CHOICE",
        "features": [
            "Up to 10 Tailored Dynamic Pages",
            "CMS / Admin Panel for Easy Updates",
            "Interactive Lead Capture & Calculator",
            "Custom Micro-Interactions & Modern UI",
            "Complete Technical & Local SEO Setup",
            "Speed Score 95+ Guarantee",
            "3 Months Priority Support"
        ],
        "cta_text": "Select Dynamic Plan",
        "order": 2
    },
    {
        "name": "Custom Solution",
        "tagline": "For ambitious enterprises needing bespoke web applications & portals",
        "price": "15,000+",
        "currency_symbol": "₹",
        "period": "/ bespoke scope",
        "usd_equivalent": "Approx ~$189+ USD • Scoped to Requirements",
        "is_popular": False,
        "popular_badge_text": "",
        "features": [
            "Custom Web App / Portal Architecture",
            "Advanced Database & REST API Integrations",
            "Interactive Dashboard & Client Telemetry",
            "Payment Gateway Integration (Razorpay/Stripe)",
            "High-Volume Performance & Hardening",
            "6 Months Dedicated VIP Support"
        ],
        "cta_text": "Request Custom Plan",
        "order": 3
    }
]


def seed_default_data_if_needed():
    """Ensure database has default portfolio items and pricing tiers if empty."""
    try:
        if PortfolioProject.objects.count() == 0:
            for item in DEFAULT_PROJECTS:
                PortfolioProject.objects.create(
                    project_slug=item["slug"],
                    title=item["title"],
                    category=item["category"],
                    category_label=item["category_label"],
                    year=item["year"],
                    image_url=item["image_url"],
                    summary=item["summary"],
                    description=item["description"],
                    highlights=item["highlights"],
                    tech_stack=item["tech_stack"],
                    order=item["order"],
                    is_featured=True
                )
        if PricingTier.objects.count() == 0:
            for item in DEFAULT_PRICING_TIERS:
                PricingTier.objects.create(
                    name=item["name"],
                    tagline=item["tagline"],
                    price=item["price"],
                    currency_symbol=item["currency_symbol"],
                    period=item["period"],
                    usd_equivalent=item["usd_equivalent"],
                    is_popular=item["is_popular"],
                    popular_badge_text=item["popular_badge_text"],
                    features=item["features"],
                    cta_text=item["cta_text"],
                    order=item["order"],
                    is_active=True
                )
    except Exception:
        pass


@ensure_csrf_cookie
def home_view(request):
    seed_default_data_if_needed()
    projects = PortfolioProject.objects.filter(is_featured=True).order_by('order')
    pricing_tiers = PricingTier.objects.filter(is_active=True).order_by('order')
    faqs = FAQItem.objects.filter(is_published=True).order_by('order')
    context = {
        'projects': projects,
        'pricing_tiers': pricing_tiers,
        'faqs': faqs,
    }
    return render(request, 'index.html', context)


@require_GET
def api_pricing_list(request):
    seed_default_data_if_needed()
    tiers = PricingTier.objects.filter(is_active=True).order_by('order')
    data = []
    for tier in tiers:
        data.append({
            'id': tier.id,
            'name': tier.name,
            'tagline': tier.tagline,
            'price': tier.price,
            'currency_symbol': tier.currency_symbol,
            'period': tier.period,
            'usd_equivalent': tier.usd_equivalent,
            'is_popular': tier.is_popular,
            'popular_badge_text': tier.popular_badge_text,
            'features': tier.features,
            'cta_text': tier.cta_text,
            'order': tier.order
        })
    return JsonResponse({'success': True, 'tiers': data})


@csrf_exempt
@require_POST
def api_submit_enquiry(request):
    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body.decode('utf-8'))
        else:
            data = request.POST

        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        phone = data.get('phone', '').strip()
        service = data.get('service', 'Business Website Development')
        budget = data.get('budget', '')
        message = data.get('message', '').strip()

        if not name or not email or not phone or not message:
            return JsonResponse({'success': False, 'error': 'All required fields must be filled.'}, status=400)

        # Get IP address
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        enquiry = ProjectEnquiry.objects.create(
            name=name,
            email=email,
            phone=phone,
            service=service,
            budget=budget,
            message=message,
            ip_address=ip
        )

        return JsonResponse({
            'success': True,
            'enquiry_id': enquiry.id,
            'message': 'Your project enquiry has been securely received by Cloudy Success! Yash Pawar will reach out within 24 hours.'
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@csrf_exempt
@require_POST
def api_submit_quote(request):
    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body.decode('utf-8'))
        else:
            data = request.POST

        project_type = data.get('type', 'Business Website')
        pages = int(data.get('pages', 5))
        addons = data.get('addons', '')
        low_estimate = int(data.get('lowEstimate', 0))
        high_estimate = int(data.get('highEstimate', 0))
        whatsapp_clicked = bool(data.get('whatsappClicked', False))

        quote = QuoteCalculation.objects.create(
            project_type=project_type,
            pages=pages,
            addons=addons,
            low_estimate=low_estimate,
            high_estimate=high_estimate,
            whatsapp_clicked=whatsapp_clicked
        )

        return JsonResponse({'success': True, 'quote_id': quote.id})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@require_GET
def api_portfolio_details(request, slug):
    try:
        project = PortfolioProject.objects.get(project_slug=slug)
        return JsonResponse({
            'success': True,
            'title': project.title,
            'category': project.category_label,
            'year': project.year,
            'image': project.image_url,
            'desc': project.description,
            'highlights': project.highlights,
            'tech': project.tech_stack
        })
    except PortfolioProject.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Project not found'}, status=404)
