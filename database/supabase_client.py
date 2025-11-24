from supabase import create_client, Client
import os

SUPABASE_URL = "https://toonzkjgytoknfruuqvo.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRvb256a2pneXRva25mcnV1cXZvIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NDAwNTg1MCwiZXhwIjoyMDc5NTgxODUwfQ.EI-xRmpx7PyIohLVv5XT06Yh4OwiWVYHEHEEVcsVE4g"
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