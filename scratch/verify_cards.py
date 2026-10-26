import urllib.request
import re

print("Testing Django home page...")
req = urllib.request.Request("http://127.0.0.1:8000/", headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as resp:
    status = resp.status
    html = resp.read().decode("utf-8")

print(f"Status: {status}")

checks = [
    ("service-card-blue", "service-card-blue in HTML"),
    ("service-card-emerald", "service-card-emerald in HTML"),
    ("service-card-purple", "service-card-purple in HTML"),
    ("service-card-amber", "service-card-amber in HTML"),
    ("service-enquire-btn", "service-enquire-btn in HTML"),
    ("service-desc", "service-desc in HTML"),
]

for pattern, desc in checks:
    count = len(re.findall(pattern, html))
    print(f"[{'OK' if count > 0 else 'FAIL'}] {desc} (count={count})")

# Check that service-features list is removed
features_count = len(re.findall(r'service-features', html))
print(f"[{'OK' if features_count == 0 else 'WARN'}] service-features in HTML (count={features_count})")

# Test CSS file
print("\nTesting CSS link...")
css_req = urllib.request.Request("http://127.0.0.1:8000/static/css/style.css", headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(css_req) as css_resp:
    css_status = css_resp.status
    css_text = css_resp.read().decode("utf-8")

print(f"CSS Status: {css_status}")
print(f"[{'OK' if '.service-card-blue' in css_text else 'FAIL'}] .service-card-blue in static CSS")
print(f"[{'OK' if '[data-theme=\"light\"] .service-card.service-card-blue' in css_text else 'FAIL'}] Light theme support in static CSS")
