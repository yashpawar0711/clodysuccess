from django.db import models


class ProjectEnquiry(models.Model):
    STATUS_CHOICES = [
        ('pending', '🟡 Pending Review'),
        ('contacted', '🔵 Contacted / Pitch Sent'),
        ('in_discussion', '🟣 In Discussion / Scoping'),
        ('converted', '🟢 Project Onboarded'),
        ('closed', '⚪ Closed / Archived'),
    ]

    SERVICE_CHOICES = [
        ('Business Website Development', 'Business Website Development'),
        ('E-commerce Website Development', 'E-commerce Website Development'),
        ('Portfolio Websites', 'Portfolio Websites'),
        ('Responsive Web Design', 'Responsive Web Design'),
        ('UI/UX Design', 'UI/UX Design'),
        ('Web Applications', 'Web Applications'),
        ('Landing Pages', 'Landing Pages'),
        ('Website Maintenance and Support', 'Website Maintenance and Support'),
        ('Custom Project Scope', 'Custom Project Scope'),
    ]

    name = models.CharField(max_length=150, help_text="Client full name")
    email = models.EmailField(help_text="Client email address")
    phone = models.CharField(max_length=40, help_text="Client phone / WhatsApp number")
    service = models.CharField(max_length=100, choices=SERVICE_CHOICES, default='Business Website Development')
    budget = models.CharField(max_length=120, blank=True, help_text="Budget range selected by client")
    message = models.TextField(help_text="Detailed project requirements and vision")
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, help_text="Internal notes for Yash Pawar / agency follow-up")
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Project Enquiry"
        verbose_name_plural = "Project Enquiries"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} — {self.service} ({self.created_at.strftime('%d %b %Y')})"


class QuoteCalculation(models.Model):
    project_type = models.CharField(max_length=100)
    pages = models.PositiveIntegerField(default=5)
    addons = models.CharField(max_length=255, blank=True)
    low_estimate = models.PositiveIntegerField()
    high_estimate = models.PositiveIntegerField()
    whatsapp_clicked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Quote Calculation"
        verbose_name_plural = "Quote Calculations"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.project_type} ({self.pages} pages) — ₹{self.low_estimate:,} to ₹{self.high_estimate:,}"


class PortfolioProject(models.Model):
    CATEGORY_CHOICES = [
        ('corporate', 'Corporate Business'),
        ('restaurant', 'Hospitality & Dining'),
        ('portfolio', 'Personal Portfolio'),
        ('ecommerce', 'E-Commerce'),
        ('saas', 'SaaS Web Application'),
        ('agency', 'Creative Agency'),
    ]

    project_slug = models.SlugField(max_length=100, unique=True)
    title = models.CharField(max_length=160)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    category_label = models.CharField(max_length=100)
    year = models.CharField(max_length=20, default='2026')
    image_url = models.CharField(max_length=255, default='/static/assets/portfolio-corporate.jpg')
    summary = models.TextField()
    description = models.TextField()
    highlights = models.JSONField(default=list, blank=True, help_text="List of bullet point strings")
    tech_stack = models.JSONField(default=list, blank=True, help_text="List of tech tags e.g. ['HTML5', 'CSS']")
    order = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Portfolio Project"
        verbose_name_plural = "Portfolio Projects"
        ordering = ['order', 'title']

    def __str__(self):
        return f"{self.title} ({self.category_label})"


class FAQItem(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        verbose_name = "FAQ Item"
        verbose_name_plural = "FAQ Items"
        ordering = ['order', 'id']

    def __str__(self):
        return self.question


class PricingTier(models.Model):
    name = models.CharField(max_length=120, help_text="Package name e.g. Starter Website, Business Website, Custom Solution")
    tagline = models.CharField(max_length=255, help_text="Brief description of target audience")
    price = models.CharField(max_length=50, help_text="Display price e.g. 14,999 or 29,999 or 59,999+")
    currency_symbol = models.CharField(max_length=10, default="₹")
    period = models.CharField(max_length=60, default="/ one-time estimate")
    usd_equivalent = models.CharField(max_length=120, default="Approx ~$199 USD • Request a Custom Quote")
    is_popular = models.BooleanField(default=False, help_text="Marks this tier as featured/popular card")
    popular_badge_text = models.CharField(max_length=80, default="MOST POPULAR CHOICE", blank=True)
    features = models.JSONField(default=list, help_text="List of feature strings")
    cta_text = models.CharField(max_length=60, default="Select Plan")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Pricing Package"
        verbose_name_plural = "Pricing Packages"
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.name} ({self.currency_symbol}{self.price})"

