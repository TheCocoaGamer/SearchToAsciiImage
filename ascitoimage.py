import requests
from PIL import Image
from io import BytesIO
import numpy as np
from serpapi import GoogleSearch  # for image search
import os

def search_image(query):
    """Search for an image using SerpAPI"""
    params = {
        "api_key": "key",  # Replace with your API key
        "engine": "google",
        "q": query,
        "tbm": "isch"
    }
    
    search = GoogleSearch(params)
    results = search.get_dict()
    
    if "images_results" in results and len(results["images_results"]) > 0:
        return results["images_results"][0]["original"]
    return None

def download_image(url):
    """Download image from URL"""
    response = requests.get(url)
    return Image.open(BytesIO(response.content))

def image_to_ascii(image, width=150):
    """Convert image to ASCII art"""
    # ASCII characters from dark to light
    ascii_chars = "@%#*+=-:. "
    
    # Resize image maintaining aspect ratio
    aspect_ratio = image.height / image.width
    height = int(width * aspect_ratio * 0.55)
    image = image.resize((width, height))
    
    # Convert to grayscale
    image = image.convert('L')
    pixels = np.array(image)
    
    # Convert pixels to ASCII (fixed version)
    ascii_str = ""
    for row in pixels:
        for pixel in row:
            # Normalize the pixel value to fit within the ascii_chars range
            index = int(pixel / 255 * (len(ascii_chars) - 1))
            ascii_str += ascii_chars[index]
        ascii_str += "\n"
    
    return ascii_str


def main():
    query = input("Enter what kind of image you want to convert to ASCII: ")
    
    print("Searching for image...")
    image_url = search_image(query)
    
    if not image_url:
        print("No image found for your query!")
        return
    
    print("Converting image to ASCII...")
    try:
        image = download_image(image_url)
        ascii_art = image_to_ascii(image)
        print("\nYour ASCII Art:")
        print(ascii_art)
        
        # Optionally save to file
        with open("ascii_art.txt", "w") as f:
            f.write(ascii_art)
            
    except Exception as e:
        print(f"Error processing image: {str(e)}")

if __name__ == "__main__":
    main()
