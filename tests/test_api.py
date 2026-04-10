import requests

BASE_URL = "http://localhost:8000"

# Test public routes
def test_get_all_tracks():
    response = requests.get(f"{BASE_URL}/api/tracks")
    print(f"GET /api/tracks: {response.status_code}")
    print(f"Total tracks: {len(response.json())}")
    print(response.json()[:2])  # Show first 2

def test_get_track_detail():
    response = requests.get(f"{BASE_URL}/api/tracks/1")
    print(f"\nGET /api/tracks/1: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Title: {data.get('title')}")
        print(f"Artist: {data.get('artist_name')}")

def test_get_categories():
    response = requests.get(f"{BASE_URL}/api/categories")
    print(f"\nGET /api/categories: {response.status_code}")
    print(f"Categories: {len(response.json())}")

def test_get_artists():
    response = requests.get(f"{BASE_URL}/api/artists")
    print(f"\nGET /api/artists: {response.status_code}")
    print(f"Artists: {len(response.json())}")

def test_search():
    response = requests.get(f"{BASE_URL}/api/tracks/search?q=Jazz")
    print(f"\nGET /api/tracks/search?q=Jazz: {response.status_code}")
    print(f"Found: {len(response.json())} tracks")

def test_new_releases():
    response = requests.get(f"{BASE_URL}/api/new-releases")
    print(f"\nGET /api/new-releases: {response.status_code}")
    print(f"New releases: {len(response.json())}")

if __name__ == "__main__":
    print("="*50)
    print("TESTING MUSIC API")
    print("="*50)
    
    test_get_all_tracks()
    test_get_track_detail()
    test_get_categories()
    test_get_artists()
    test_search()
    test_new_releases()
    
    print("\n" + "="*50)
    print("✅ ALL TESTS COMPLETE")
    print("="*50)