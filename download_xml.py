import urllib.request

url = "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml"
filename = "haarcascade_frontalface.xml"

print(f"Downloading {filename}...")
try:
    urllib.request.urlretrieve(url, filename)
    print("Download complete.")
except Exception as e:
    print(f"Error downloading: {e}")
