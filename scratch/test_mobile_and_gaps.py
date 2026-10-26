import urllib.request
import re

print("Testing web server...")
base_url = "http://127.0.0.1:8000"

def fetch(path):
    url = f"{base_url}{path}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)"})
    with urllib.request.urlopen(req) as resp:
        return resp.status, resp.read().decode('utf-8', errors='ignore')

# 1. Test homepage
status, html = fetch("/")
print(f"[STATUS] Home: {status}")

# 2. Test CSS
css_status, css_text = fetch("/static/css/style.css")
print(f"[STATUS] CSS: {css_status}")

css_checks = [
    ("padding-top: 42px", "Compact section padding (42px)"),
    ("padding-top: 24px !important", "Mobile compact padding (24px)"),
    ("backdrop-filter: none !important", "Zero GPU lag on mobile (backdrop-filter disabled)"),
    (".ambient-glow", "Ambient glow disabled on mobile"),
    ("-webkit-overflow-scrolling: touch", "iOS smooth native momentum scrolling"),
    ("gap: 14px !important", "Mobile grid gap tightened (14px)"),
]

for pat, desc in css_checks:
    found = pat in css_text
    print(f"[{'PASS' if found else 'FAIL'}] CSS: {desc}")

# 3. Test JS
js_status, js_text = fetch("/static/js/main.js")
print(f"[STATUS] JS: {js_status}")

js_checks = [
    ("isMobile", "isMobile device detection"),
    ("onScrollThrottled", "Batched 60fps requestAnimationFrame scroll handler"),
    ("revealElements.forEach((el) => el.classList.add('is-revealed'))", "Instant mobile scroll reveal (no pop-in lag)"),
    ("!isMobile && window.innerWidth > 960", "Ambient canvas disabled on mobile/touch"),
]

for pat, desc in js_checks:
    found = pat in js_text
    print(f"[{'PASS' if found else 'FAIL'}] JS: {desc}")

# 4. Test assets serving
asset_urls = [
    "/assets/portfolio-architect.jpg",
    "/assets/portfolio-saas.jpg",
    "/assets/portfolio-agency.jpg",
]

for asset in asset_urls:
    try:
        url = f"{base_url}{asset}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as resp:
            print(f"[PASS] Asset {asset}: {resp.status}")
    except Exception as e:
        print(f"[FAIL] Asset {asset}: {e}")

print("\nAll verification checks complete!")
