from supabase import create_client, Client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def upload_image(local_path, storage_path):
    with open(local_path, "rb") as f:
        res = supabase.storage.from_("yugioh-cards").upload(
            file=f,
            path=storage_path,
            file_options={"content-type": "image/jpeg"}
        )

    print("Upload result:", res)
    
    # generate public URL
    public_url = supabase.storage.from_("yugioh-cards").get_public_url(storage_path)
    print("URL:", public_url)
    return public_url


upload_image(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets/monsters/Blue-Eyes White Dragon.jpg")), "monsters/blue_eyes.png")