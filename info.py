import logging
from pyrogram import Client, filters
import requests

# Enable logging
logging.basicConfig(level=logging.INFO)

# ================== CONFIG (Your Details) ==================
API_ID = 20035684
API_HASH = "987a8b7ee93d55e76bb29fce4d8ebf52"
BOT_TOKEN = "8315587555:AAEB8hCCcXn_FN6SHWyUA_ZWuMWcZf6V8ts"

MONGO_URI = "mongodb+srv://YOUR_MONGO_URI"   # Add MongoDB if you have one

SHORTENER_API = "ef9e633750559"
SHORTENER_URL = "https://earnlinks.in/api"
# ===========================================================

bot = Client(
    "MovieFilterBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

def shorten_url(url: str) -> str:
    try:
        resp = requests.get(f"{SHORTENER_URL}?api={SHORTENER_API}&url={url}")
        data = resp.json()
        return data.get("shortenedUrl", url)
    except Exception as e:
        logging.error(f"Shortener error: {e}")
        return url

@bot.on_message(filters.command("start"))
async def cmd_start(_, message):
    await message.reply_text(
        "👋 Hello! I am your Auto Filter Movie Bot with Shortener.\n\n"
        "Send me a movie name and I’ll fetch you the links 📽️"
    )

@bot.on_message(filters.text & ~filters.command("start"))
async def handle_movie_query(_, message):
    query = message.text.strip()
    sanitized = query.replace(" ", "_")
    movie_link = f"https://example.com/download/{sanitized}"  # Dummy link
    short_link = shorten_url(movie_link)

    await message.reply_text(
        f"🎬 **Movie:** `{query}`\n"
        f"🔗 **Link:** {short_link}"
    )

if __name__ == "__main__":
    bot.run()
