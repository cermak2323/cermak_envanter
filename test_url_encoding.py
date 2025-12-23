#!/usr/bin/env python3
"""Test URL encoding with Flask path converter"""

from flask import Flask, url_for
from urllib.parse import quote

app = Flask(__name__)

@app.route('/parts/<path:part_code>')
def part_detail(part_code):
    return f"Part: {part_code}"

# Test
with app.test_request_context():
    # Test case 1: part_code with slash
    part_code_with_slash = "948/756"
    url = url_for('part_detail', part_code=part_code_with_slash)
    print(f"✅ Flask url_for result: {url}")
    print(f"   Part code: {part_code_with_slash}")
    print(f"   URL: {url}")
    
    # Test case 2: decoding
    from urllib.parse import unquote
    decoded = unquote(url.replace('/parts/', ''))
    print(f"   Decoded back: {decoded}")
    print(f"   Match: {decoded == part_code_with_slash}")
