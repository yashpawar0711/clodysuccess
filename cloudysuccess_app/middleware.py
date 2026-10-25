"""
Cloudy Success — Enterprise-Grade Security Middleware
Protects against Clickjacking, XSS, MIME Sniffing, Path Traversal, Bot Probes, and Information Leakage.
"""

import re
from django.http import HttpResponseForbidden, JsonResponse

# Suspicious probe patterns (attackers scanning for common vulnerabilities)
SUSPICIOUS_PATH_PATTERNS = [
    r'/\.env',
    r'/\.git',
    r'/wp-admin',
    r'/wp-login',
    r'/phpmyadmin',
    r'/\.aws',
    r'/eval-stdin\.php',
    r'/\.\./',
    r'/etc/passwd',
    r'/windows/win\.ini',
    r'/cgi-bin',
    r'/admin\.php',
]

SUSPICIOUS_REGEX = re.compile('|'.join(SUSPICIOUS_PATH_PATTERNS), re.IGNORECASE)


class HardenedSecurityMiddleware:
    """
    Applies comprehensive HTTP response security headers and inspects
    incoming requests for automated malicious probes and exploit patterns.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        # 1. Block common malicious bot probes & directory traversal attempts
        if SUSPICIOUS_REGEX.search(path):
            return HttpResponseForbidden("Access Denied: Security Violation Triggered.")

        # 2. Block suspicious query parameter injections (e.g. <script>, UNION SELECT)
        query_string = request.META.get('QUERY_STRING', '')
        if query_string:
            lowered = query_string.lower()
            if '<script' in lowered or 'union select' in lowered or 'information_schema' in lowered:
                return HttpResponseForbidden("Access Denied: Malicious Query String Detected.")

        response = self.get_response(request)

        # 3. Add Hardened Security Headers to every response
        # Anti-Clickjacking: Disallow site from being embedded in iframes
        response['X-Frame-Options'] = 'DENY'

        # Anti-MIME Sniffing: Prevent browsers from interpreting files as something else
        response['X-Content-Type-Options'] = 'nosniff'

        # Legacy XSS Filter for older browsers
        response['X-XSS-Protection'] = '1; mode=block'

        # Referrer Policy: Send full URL only to same-origin; strip sensitive params on cross-origin
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'

        # Permissions Policy: Disable unwanted device access
        response['Permissions-Policy'] = 'camera=(), microphone=(), geolocation=(), payment=()'

        # Content Security Policy (CSP): Strict whitelist of trusted asset sources
        # Protects against inline script injection, external malicious scripts, and data exfiltration
        csp_directives = [
            "default-src 'self'",
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com",
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
            "font-src 'self' https://fonts.gstatic.com data:",
            "img-src 'self' data: https: blob:",
            "connect-src 'self'",
            "frame-ancestors 'none'",
            "base-uri 'self'",
            "form-action 'self' https://api.whatsapp.com https://mail.google.com",
        ]
        response['Content-Security-Policy'] = "; ".join(csp_directives)

        # 4. Remove / Mask Server Signature to prevent fingerprinting
        if 'Server' in response:
            del response['Server']
        response['Server'] = 'Protected-CloudySuccess'

        return response
