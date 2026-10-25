"""
Cloudy Success — Application-Layer Security Core
Provides:
1. IP Sliding Window Rate Limiting (Anti-Flooding / Anti-Brute-Force / Anti-DoS)
2. Input Sanitization & HTML/XSS Payload Stripping
3. Email & Phone Strict Format Validation
4. Bot Honeypot Detection
5. Origin & Referer Verification (Anti-CSRF for JSON APIs)
"""

import time
import re
import html
from collections import defaultdict
from django.core.validators import EmailValidator, ValidationError

# In-memory sliding window rate tracker: ip -> list of timestamps
_ENQUIRY_RATE_TRACKER = defaultdict(list)
_QUOTE_RATE_TRACKER = defaultdict(list)

# Limits
ENQUIRY_MAX_PER_WINDOW = 5        # Max 5 enquiries per 10 minutes per IP
ENQUIRY_WINDOW_SECONDS = 600       # 10 minutes

QUOTE_MAX_PER_WINDOW = 15          # Max 15 quote calculations per 10 minutes per IP
QUOTE_WINDOW_SECONDS = 600         # 10 minutes

# Clean phone regex: digits, +, -, spaces, parentheses, 7 to 20 chars
PHONE_REGEX = re.compile(r'^[+0-9\s\-()]{7,25}$')

# HTML/Script tag regex for sanitization
TAG_RE = re.compile(r'<[^>]+>')
DANGEROUS_PATTERNS = re.compile(r'(javascript:|data:|vbscript:|onload=|onerror=|onclick=|<script|<\/script)', re.IGNORECASE)

_email_validator = EmailValidator(message="Invalid email address format.")


def get_client_ip(request):
    """
    Extracts client IP address safely, checking X-Forwarded-For first
    if behind a reverse proxy (e.g., Nginx, Cloudflare), otherwise REMOTE_ADDR.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR', '')
    return ip or '127.0.0.1'


def is_rate_limited(ip, tracker, max_requests, window_seconds):
    """
    Sliding window rate limiter algorithm.
    Returns True if request exceeds limit, False if allowed.
    """
    now = time.time()
    cutoff = now - window_seconds
    
    # Filter out timestamps older than the cutoff window
    timestamps = [t for t in tracker[ip] if t > cutoff]
    
    if len(timestamps) >= max_requests:
        tracker[ip] = timestamps
        return True
    
    timestamps.append(now)
    tracker[ip] = timestamps
    return False


def check_enquiry_rate_limit(ip):
    """Checks if IP exceeded maximum allowed enquiry submissions."""
    return is_rate_limited(ip, _ENQUIRY_RATE_TRACKER, ENQUIRY_MAX_PER_WINDOW, ENQUIRY_WINDOW_SECONDS)


def check_quote_rate_limit(ip):
    """Checks if IP exceeded maximum allowed quote calculations."""
    return is_rate_limited(ip, _QUOTE_RATE_TRACKER, QUOTE_MAX_PER_WINDOW, QUOTE_WINDOW_SECONDS)


def sanitize_text(text, max_length=1000):
    """
    Sanitizes arbitrary user input text:
    - Strips leading/trailing whitespace
    - Removes all HTML tags
    - Neutralizes dangerous JavaScript URI schemes & event handlers
    - Escapes special characters
    - Clamps to max_length to prevent buffer/memory attacks
    """
    if not text:
        return ''
    
    # 1. Convert to string and trim
    cleaned = str(text).strip()
    
    # 2. Enforce length boundary
    if len(cleaned) > max_length:
        cleaned = cleaned[:max_length]
        
    # 3. Strip all HTML tags
    cleaned = TAG_RE.sub('', cleaned)
    
    # 4. Remove dangerous executable patterns
    cleaned = DANGEROUS_PATTERNS.sub('', cleaned)
    
    # 5. HTML escape remaining string to prevent injection
    cleaned = html.escape(cleaned, quote=True)
    
    return cleaned.strip()


def validate_email_address(email):
    """
    Validates email format using Django's EmailValidator.
    Returns (is_valid, cleaned_email).
    """
    if not email:
        return False, ''
    
    cleaned = str(email).strip().lower()
    if len(cleaned) > 150:
        return False, ''
    
    try:
        _email_validator(cleaned)
        return True, cleaned
    except ValidationError:
        return False, ''


def validate_phone_number(phone):
    """
    Validates phone format (numbers, optional leading +, dashes, spaces).
    Returns (is_valid, cleaned_phone).
    """
    if not phone:
        return False, ''
    
    cleaned = str(phone).strip()
    if len(cleaned) > 25 or len(cleaned) < 7:
        return False, ''
    
    if PHONE_REGEX.match(cleaned):
        return True, cleaned
    return False, ''


def is_bot_honeypot_triggered(data):
    """
    Honeypot detection: checks if hidden honeypot fields have been filled.
    Human users never see or fill these fields; automated bots fill all form fields.
    """
    honeypot_keys = ['website_url_hp', 'hp_field', 'company_fax', 'middle_name_hp']
    for key in honeypot_keys:
        val = data.get(key, '')
        if val and str(val).strip():
            return True
    return False


def verify_request_origin(request):
    """
    Verifies that the request Origin or Referer matches the host.
    Blocks cross-site forged submissions while allowing same-origin AJAX calls.
    """
    origin = request.META.get('HTTP_ORIGIN') or request.META.get('HTTP_REFERER')
    if not origin:
        # If no origin header (some strict clients/cURL), allow if host header matches
        return True
    
    host = request.get_host()
    # Origin must contain our host
    if host in origin or '127.0.0.1' in origin or 'localhost' in origin:
        return True
    return False
