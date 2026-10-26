import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from .models import ProjectEnquiry, QuoteCalculation, PortfolioProject, FAQItem, PricingTier
from .security import (
    get_client_ip,
    check_enquiry_rate_limit,
    check_quote_rate_limit,
    sanitize_text,
    validate_email_address,
    validate_phone_number,
    is_bot_honeypot_triggered,
    verify_request_origin
)


DEFAULT_PROJECTS = [
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
        "tech_stack": ["CSS Grid", "Minimalist UI", "Blueprint Lightbox", "Parallax Scrolling", "Editorial Typography"],
        "order": 1
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
        "tech_stack": ["API Ready", "Dark Mode UI", "Single Page App", "Custom SVG Charts", "Data Visualizations"],
        "order": 2
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
        "tech_stack": ["CSS Keyframes", "Custom Motion", "WebGL Ambience", "Fluid Typography", "Magnetic Physics"],
        "order": 3
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
            "Interactive Lead Capture & Smart Forms",
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
    """
    Secure Enquiry Endpoint:
    - Verifies request origin (Anti-CSRF)
    - IP Rate Limiting (Anti-DoS / Anti-Spam)
    - Honeypot Bot Detection
    - Deep Input Sanitization (Anti-XSS / Anti-Injection)
    - Strict Email & Phone Format Validation
    """
    try:
        # 1. Origin verification
        if not verify_request_origin(request):
            return JsonResponse({'success': False, 'error': 'Forbidden request origin.'}, status=403)

        # 2. Extract Client IP and enforce rate limiting (max 5 per 10 mins)
        client_ip = get_client_ip(request)
        if check_enquiry_rate_limit(client_ip):
            return JsonResponse({
                'success': False,
                'error': 'Too many submissions detected from your IP. For security reasons, please wait a few minutes before submitting another enquiry.'
            }, status=429)

        # 3. Parse payload
        if request.content_type == 'application/json':
            data = json.loads(request.body.decode('utf-8'))
        else:
            data = request.POST

        # 4. Anti-Bot Honeypot: Drop silently if bot filled hidden field
        if is_bot_honeypot_triggered(data):
            return JsonResponse({
                'success': True,
                'message': 'Your project enquiry has been securely received by Cloudy Success! Yash Pawar will reach out within 24 hours.'
            })

        # 5. Sanitize text fields (Anti-XSS, HTML strip, length clamping)
        raw_name = data.get('name', '')
        raw_email = data.get('email', '')
        raw_phone = data.get('phone', '')
        raw_service = data.get('service', 'Business Website Development')
        raw_budget = data.get('budget', '')
        raw_message = data.get('message', '')

        name = sanitize_text(raw_name, max_length=100)
        service = sanitize_text(raw_service, max_length=100)
        budget = sanitize_text(raw_budget, max_length=100)
        message = sanitize_text(raw_message, max_length=3000)

        # 6. Strict validation checks
        if not name or not raw_email or not raw_phone or not message:
            return JsonResponse({'success': False, 'error': 'All required fields (Name, Email, Phone, Message) must be filled.'}, status=400)

        is_valid_email, email = validate_email_address(raw_email)
        if not is_valid_email:
            return JsonResponse({'success': False, 'error': 'Please provide a valid email address (e.g. yourname@domain.com).'}, status=400)

        is_valid_phone, phone = validate_phone_number(raw_phone)
        if not is_valid_phone:
            return JsonResponse({'success': False, 'error': 'Please provide a valid phone or WhatsApp number.'}, status=400)

        # 7. Secure parameterized DB insert via Django ORM (100% SQL-injection proof)
        enquiry = ProjectEnquiry.objects.create(
            name=name,
            email=email,
            phone=phone,
            service=service,
            budget=budget,
            message=message,
            ip_address=client_ip
        )

        return JsonResponse({
            'success': True,
            'enquiry_id': enquiry.id,
            'message': 'Your project enquiry has been securely received by Cloudy Success! Yash Pawar will reach out within 24 hours.'
        })

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Malformed request payload.'}, status=400)
    except Exception:
        # Never leak stack trace or internal database error messages to clients
        return JsonResponse({'success': False, 'error': 'A secure system error occurred. Please try again or reach out via WhatsApp.'}, status=500)


@csrf_exempt
@require_POST
def api_submit_quote(request):
    """
    Secure Quote Calculation Endpoint:
    - Verifies request origin
    - IP Rate Limiting (max 15 per 10 mins)
    - Validates integer bounds & sanitizes inputs
    """
    try:
        if not verify_request_origin(request):
            return JsonResponse({'success': False, 'error': 'Forbidden request origin.'}, status=403)

        client_ip = get_client_ip(request)
        if check_quote_rate_limit(client_ip):
            return JsonResponse({
                'success': False,
                'error': 'Rate limit exceeded. Please wait a moment before calculating more estimates.'
            }, status=429)

        if request.content_type == 'application/json':
            data = json.loads(request.body.decode('utf-8'))
        else:
            data = request.POST

        # Sanitize and validate inputs
        project_type = sanitize_text(data.get('type', 'Business Website'), max_length=80)
        addons = sanitize_text(data.get('addons', ''), max_length=200)

        try:
            pages = max(1, min(100, int(data.get('pages', 5))))
            low_estimate = max(0, min(10000000, int(data.get('lowEstimate', 0))))
            high_estimate = max(0, min(10000000, int(data.get('highEstimate', 0))))
        except (ValueError, TypeError):
            return JsonResponse({'success': False, 'error': 'Invalid calculation values.'}, status=400)

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

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Malformed request payload.'}, status=400)
    except Exception:
        return JsonResponse({'success': False, 'error': 'Unable to calculate quote securely.'}, status=500)


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
