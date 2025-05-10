import requests
from urllib.parse import urlparse

def extract_github_username(url):
    try:
        parsed = urlparse(url)
        path_parts = [part for part in parsed.path.split('/') if part]
        
        if path_parts:
            return path_parts[0] 
        return None
    except:
        return None

def get_github_user_data(username):
    api_url = f"https://api.github.com/users/{username}"
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        return {"error": f"HTTP error: {str(e)}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Request error: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

def display_user_info(data):
    if "error" in data:
        print(f"\n❌ {data['error']}")
        return

    print("\n✅ GitHub Profile Info:")
    print("------------------------")
    print(f"👤 Username      : {data.get('login', 'N/A')}")
    print(f"🧑 Name          : {data.get('name', 'Not set')}")
    print(f"📄 Bio           : {data.get('bio', 'Not set')}")
    print(f"📸 Profile Image : {data.get('avatar_url')}")
    print(f"📦 Public Repos  : {data.get('public_repos')}")
    print(f"👥 Followers     : {data.get('followers')}")
    print(f"🔗 Profile URL   : {data.get('html_url')}\n")

def main():
    print("🔍 GitHub Profile Image & Info Extractor")
    print("----------------------------------------")
    url = input("Enter GitHub profile or repo URL: ").strip()
    
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    username = extract_github_username(url)
    
    if not username:
        print("\n❌ Could not extract GitHub username from URL.")
        return

    user_data = get_github_user_data(username)
    display_user_info(user_data)

if __name__ == "__main__":
    main()