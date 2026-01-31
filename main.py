import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import CommandStart

import config
import db
import keyboards as kb
import downloader

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()

# vaqtincha link saqlash
user_links = {}

@dp.message(CommandStart())
async def start(message: Message):
    db.init_db()
    await message.answer(
        "👋 Assalomu alaykum!\n\n"
        "Men Instagram, TikTok, YouTube va boshqa platformalardan "
        "video yuklab beruvchi botman.\n\n"
        "⬇️ Quyidagi tugmalardan foydalaning:",
        reply_markup=kb.menu()
    )

@dp.callback_query(F.data == "download")
async def ask_link(call: CallbackQuery):
    await call.message.answer("🔗 Iltimos, video havolasini yuboring:")
    await call.answer()

@dp.message(F.text.startswith("http"))
async def get_link(message: Message):
    user_links[message.from_user.id] = message.text
    user = db.get_user(message.from_user.id)

    await message.answer(
        "🎞 Video sifatini tanlang:",
        reply_markup=kb.quality(user["premium"])
    )

@dp.callback_query(F.data.in_(["q360", "q720", "q1080"]))
async def download_video(call: CallbackQuery):
    user_id = call.from_user.id
    user = db.get_user(user_id)

    if user["daily"] >= config.FREE_DAILY_LIMIT and not user["premium"]:
        await call.message.answer(
            "❌ Bugungi bepul limit tugadi.\n"
            "⭐ Premium bilan cheksiz yuklab olish mumkin."
        )
        await call.answer()
        return

    if user_id not in user_links:
        await call.message.answer("❌ Avval video havolasini yuboring.")
        await call.answer()
        return

    quality_map = {
        "q360": "360",
        "q720": "720",
        "q1080": "1080"
    }

    quality = quality_map[call.data]
    url = user_links[user_id]

    await call.message.answer("⏳ Video yuklab olinmoqda, kuting...")

    try:
        file_path = downloader.download(url, quality)
        await call.message.answer_video(
            FSInputFile(file_path),
            caption="✅ Video tayyor!"
        )
        db.inc_download(user_id)
        os.remove(file_path)

    except Exception as e:
        await call.message.answer(
            "❌ Video yuklab olishda xatolik yuz berdi.\n"
            "Boshqa link bilan urinib ko‘ring."
        )

    await call.answer()

@dp.callback_query(F.data == "stats")
async def stats(call: CallbackQuery):
    user = db.get_user(call.from_user.id)
    await call.message.answer(
        f"📊 Statistika:\n\n"
        f"⭐ Premium: {'Ha' if user['premium'] else 'Yo‘q'}\n"
        f"📥 Bugungi yuklashlar: {user['daily']}/{config.FREE_DAILY_LIMIT}"
    )
    await call.answer()

@dp.callback_query(F.data == "help")
async def help_menu(call: CallbackQuery):
    await call.message.answer(
        "ℹ️ Yordam:\n\n"
        "1️⃣ 📥 Video yuklab olish tugmasini bosing\n"
        "2️⃣ Video havolasini yuboring\n"
        "3️⃣ Sifatni tanlang\n\n"
        "Bot avtomatik yuklab beradi ✅"
    )
    await call.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
