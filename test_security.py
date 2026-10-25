import urllib.request
import urllib.error
import json

base_url = 'http://127.0.0.1:8000'

print('=== 1. TESTING SECURITY HEADERS ON HOME PAGE ===')
try:
    req = urllib.request.Request(base_url + '/')
    with urllib.request.urlopen(req) as resp:
        print('Status:', resp.status)
        headers = dict(resp.headers)
        print('X-Frame-Options:', headers.get('X-Frame-Options'))
        print('X-Content-Type-Options:', headers.get('X-Content-Type-Options'))
        print('X-XSS-Protection:', headers.get('X-XSS-Protection'))
        print('Referrer-Policy:', headers.get('Referrer-Policy'))
        print('Permissions-Policy:', headers.get('Permissions-Policy'))
        print('Content-Security-Policy present:', 'Content-Security-Policy' in headers)
        print('Server header masked:', headers.get('Server'))
except Exception as e:
    print('Home page test error:', e)

print('\n=== 2. TESTING MALICIOUS PROBE & EXPLOIT BLOCKING ===')
def test_blocked(url, desc):
    try:
        req = urllib.request.Request(url)
        urllib.request.urlopen(req)
        print(f'FAIL (Allowed unexpectedly): {desc}')
    except urllib.error.HTTPError as e:
        if e.code == 403:
            print(f'PASS (Blocked with HTTP 403 Forbidden): {desc}')
        else:
            print(f'Response HTTP {e.code}: {desc}')
    except Exception as e:
        print(f'Error testing {desc}: {e}')

test_blocked(base_url + '/.env', 'Probe for /.env file')
test_blocked(base_url + '/wp-admin', 'Probe for /wp-admin')
test_blocked(base_url + '/.git/config', 'Probe for /.git directory')
test_blocked(base_url + '/?search=<script>alert("xss")</script>', 'Injected <script> in query string')
test_blocked(base_url + '/?id=1+union+select+null,password+from+users', 'Injected SQL UNION SELECT in query string')

print('\n=== 3. TESTING API INPUT VALIDATION & HONEYPOT ===')
def post_enquiry(payload, desc):
    try:
        req = urllib.request.Request(
            base_url + '/api/enquiry/',
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json', 'Host': '127.0.0.1:8000'}
        )
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print(f'{desc}: HTTP {resp.status} - success={data.get("success")}')
            return resp.status, data
    except urllib.error.HTTPError as e:
        error_data = e.read().decode('utf-8')
        print(f'{desc}: HTTP {e.code} - {error_data}')
        return e.code, error_data
    except Exception as e:
        print(f'{desc}: Error {e}')
        return None, None

# Test invalid email rejection
post_enquiry({
    'name': 'Test User',
    'email': 'not-an-email',
    'phone': '+91 9356047461',
    'message': 'Testing security.'
}, 'Invalid email validation')

# Test XSS sanitization
post_enquiry({
    'name': '<script>alert("xss")</script>John Doe',
    'email': 'john.doe@example.com',
    'phone': '+91 9356047461',
    'message': 'Hello from secure test with <img src=x onerror=alert(1)>.'
}, 'Sanitized XSS payload submission')

# Test bot honeypot detection
post_enquiry({
    'name': 'Spam Bot',
    'email': 'spambot@spam.com',
    'phone': '+91 9356047461',
    'message': 'Buy cheap crypto',
    'website_url_hp': 'http://malicious-bot-site.com'
}, 'Bot honeypot submission')

print('\n=== SECURITY AUDIT TEST COMPLETED ===')
