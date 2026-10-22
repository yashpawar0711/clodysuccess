from django.contrib import admin
from django.utils.html import format_html
from .models import ProjectEnquiry, QuoteCalculation, PortfolioProject, FAQItem, PricingTier

# Custom Admin Site Branding for Cloudy Success
admin.site.site_header = "Cloudy Success — Executive Admin Portal"
admin.site.site_title = "Cloudy Success Management"
admin.site.index_title = "Agency CRM & Project Telemetry"


@admin.register(ProjectEnquiry)
class ProjectEnquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'service', 'budget', 'phone', 'email', 'status', 'created_at')
    list_filter = ('status', 'service', 'created_at')
    search_fields = ('name', 'email', 'phone', 'message', 'notes')
    list_editable = ('status',)
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at', 'ip_address')

    fieldsets = (
        ('Client Identification', {
            'fields': ('name', 'email', 'phone', 'ip_address')
        }),
        ('Project Requirements', {
            'fields': ('service', 'budget', 'message')
        }),
        ('CRM Pipeline Status & Notes', {
            'fields': ('status', 'notes', 'created_at', 'updated_at')
        }),
    )

    def status_badge(self, obj):
        colors = {
            'pending': '#f59e0b',
            'contacted': '#3b82f6',
            'in_discussion': '#8b5cf6',
            'converted': '#10b981',
            'closed': '#6b7280',
        }
        color = colors.get(obj.status, '#38bdf8')
        return format_html(
            '<span style="background-color: {}; color: #fff; padding: 3px 10px; border-radius: 999px; font-weight: 600; font-size: 11px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = "Status"


@admin.register(QuoteCalculation)
class QuoteCalculationAdmin(admin.ModelAdmin):
    list_display = ('project_type', 'pages', 'addons', 'estimate_range', 'whatsapp_clicked', 'created_at')
    list_filter = ('project_type', 'whatsapp_clicked', 'created_at')
    date_hierarchy = 'created_at'

    def estimate_range(self, obj):
        return f"₹{obj.low_estimate:,} – ₹{obj.high_estimate:,}"
    estimate_range.short_description = "Estimate Range"


@admin.register(PortfolioProject)
class PortfolioProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category_label', 'year', 'order', 'is_featured')
    list_filter = ('category', 'is_featured')
    search_fields = ('title', 'summary', 'description')
    list_editable = ('order', 'is_featured')
    prepopulated_fields = {'project_slug': ('title',)}


@admin.register(FAQItem)
class FAQItemAdmin(admin.ModelAdmin):
    list_display = ('question', 'order', 'is_published')
    list_editable = ('order', 'is_published')
    search_fields = ('question', 'answer')


@admin.register(PricingTier)
class PricingTierAdmin(admin.ModelAdmin):
    list_display = ('name', 'currency_symbol', 'price', 'period', 'is_popular', 'is_active', 'order')
    list_editable = ('price', 'is_popular', 'is_active', 'order')
    search_fields = ('name', 'tagline', 'price')
    list_filter = ('is_popular', 'is_active')
    fieldsets = (
        ('Package Details', {
            'fields': ('name', 'tagline', 'order', 'is_active')
        }),
        ('Pricing Display (Editable by Admin)', {
            'fields': ('currency_symbol', 'price', 'period', 'usd_equivalent')
        }),
        ('Promotional Badge', {
            'fields': ('is_popular', 'popular_badge_text')
        }),
        ('Features & Call to Action', {
            'fields': ('features', 'cta_text')
        }),
    )

