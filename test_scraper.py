from bs4 import BeautifulSoup
import scraper as s
import pytest

@pytest.fixture(scope='module')
def html_results():
    html, encoding = s.fetch_search_results(minAsk=300,maxAsk=500,bedrooms=2)
    return html

@pytest.fixture(scope='module')
def json_results():
    json = s.fetch_json_results(minAsk=300,maxAsk=500,bedrooms=2)
    return json

def test_fetch_search_results(html_results):
    html = html_results
    assert "<html" in html
    assert "</html>" in html

def test_fetch_json_results(json_results):
    listings = json_results[0]
    for listing in listings:
        assert u'PostingID' in listing
        assert u'Longitude' in listing
        assert u'Latitude' in listing

def test_read_search_results():
    test = u"""
<! DOCTYPE html><html><body><p>Hello World.</p></body></html>
"""
    with open('test.html', 'w') as file:
        return file.write(test)
    result, encoding = s.read_search_results('test.html')
    import os
    os.remove('test.html')
    assert test == result

def test_parse_source():
    test = """
<! DOCTYPE html><html><body><p>Hello World.</p></body></html>
"""
    parsed = s.parse_source(test)
    assert parsed.body.p.text == u'Hello World.'

def test_extract_listings(html_results):
    parsed = BeautifulSoup(html_results)
    listings = s.extract_listings(parsed)
    for listing in listings:
        assert 'pid' in listing
        assert 'price' in listing
        assert 'description' in listing

def test_add_location(html_results, json_results):
    json = json_results
    search = {j['PostingID']: j for j in json[0]}
    doc = s.parse_source(html_results, 'utf-8')
    for listing in s.extract_listings(doc):
        if (s.add_location(listing, search)):
            check = listing
            break
    assert 'location' in check
        
    
def test_add_address(html_results, json_results):
    json = json_results
    search = {j['PostingID']: j for j in json[0]}
    doc = s.parse_source(html_results, 'utf-8')
    address = False
    for listing in s.extract_listings(doc):
        if (s.add_location(listing,search)):
            listing = s.add_address(listing)
            check = listing
            break
    assert 'address' in check


