#Alt text generator from Gemini API key

# --------------------------------------------------------
# Imports
# --------------------------------------------------------
import os
import mimetypes       
from PIL import Image
from google import genai
from google.genai import types



# --------------------------------------------------------
# Setup API client
# --------------------------------------------------------

client = genai.Client(api_key="AIzaSyAv67Fv9hUqxvJ2Zw8WPuc8odho5NNA-DU")

# --------------------------------------------------------
# Function: generate_alt_text
# --------------------------------------------------------
def generate_alt_text(image_path):
    # Verify file existence
    if not os.path.exists(image_path):
        print(" Error: File not found.")
        return None

    try:
        # Open image to confirm it's valid
        img = Image.open(image_path)
        img.verify()  # basic validation
    except Exception as e:
        print(f" Error opening image: {e}")
        return None

    # Guess mime type (fallback to jpeg)
    mime_type, _ = mimetypes.guess_type(image_path)
    if mime_type is None:
        mime_type = "image/jpeg"

    # Read bytes for Gemini
    try:
        with open(image_path, "rb") as f:
            image_bytes = f.read()
    except Exception as e:
        print(f" Error reading image bytes: {e}")
        return None

    image_part = types.Part.from_bytes(
        data=image_bytes,
        mime_type=mime_type,
    )

    # Call Gemini Vision (multimodal) model
    print(" Generating alt-text with Gemini... Please wait.")

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",  # fast, multimodal model
            contents=[
                image_part,
                "Generate a concise and accessible alt-text for this image.",
            ],
        )
    except Exception as e:
        print(f" Error from Gemini API: {e}")
        return None

    # Extract generated text
    alt_text = (response.text or "").strip()
    return alt_text if alt_text else None


# --------------------------------------------------------
# Main CLI function
# --------------------------------------------------------
def main():
    print("===  Alt-Text Generator (Gemini) ===")
    print("This tool uses Google's Gemini multimodal model to create descriptive alt-text for accessibility.\n")

    while True:
        image_path = input("Enter the path to your image file (or 'quit' to exit): ").strip()

        if image_path.lower() == "quit":
            print("Program terminated.")
            break

        alt_text = generate_alt_text(image_path)

        if alt_text:
            print(f"\n Generated Alt-Text:\n{alt_text}\n")
        else:
            print(" Could not generate alt-text. Try again.")

        again = input("Would you like to process another image? (yes/no): ").strip().lower()
        if again in ("no", "n"):
            print("Goodbye!")
            break


# --------------------------------------------------------
# Run program
# --------------------------------------------------------
if __name__ == "__main__":
    main()
