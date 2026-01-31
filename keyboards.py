from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📥 Video yuklab olish", callback_data="download")]
    ])

def quality():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎥 360p", callback_data="q360")],
        [InlineKeyboardButton(text="🎬 720p", callback_data="q720")]
    ])
