from flask import Flask, request, jsonify
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import requests
import json

# ========== KONFIGURASI ==========
TOKEN = "8277774482:AAG-g5wFCw-1XMWHdtAs6TJMbhXS6J58ims"  # GANTI INI!!!
API_KEY = "alight_live_a74eeaf872c56e0d9a23b41a7bc5fb8b"
API_URL = "https://am.rafaelxd.my.id/api/v1/auto-activate"

HEADERS = {
    "Content-Type": "application/json",
    "x-api-key": API_KEY
}

# ========== BUAT FLASK APP ==========
flask_app = Flask(__name__)

# ========== BUAT APPLICATION TELEGRAM ==========
bot_app = Application.builder().token(TOKEN).build()

# ========== FUNGSI API ==========
async def create_account():
    try:
        response = requests.post(API_URL, json={}, headers=HEADERS, timeout=30)
        return response.json()
    except Exception as e:
        return {"status": "error", "message": f"Gagal: {str(e)}"}

# ========== COMMAND START ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🚀 Buat Akun Premium", callback_data="buat_akun")],
        [InlineKeyboardButton("📊 Cek Kuota", callback_data="cek_kuota")],
        [InlineKeyboardButton("📖 Panduan", callback_data="panduan")],
        [InlineKeyboardButton("👨‍💻 Developer", callback_data="dev")]
    ]
    await update.message.reply_text(
        "👋 *Selamat Datang!*\n\n⚡ *ALIGHT MOTION PREMIUM BOT*\nKlik tombol di bawah:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

# ========== BUAT AKUN ==========
async def buat_akun(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("⏳ *Sedang membuat akun...*", parse_mode="Markdown")
    
    result = await create_account()
    
    if result.get("status") == "success":
        email = result.get("email", "gak tersedia")
        password = result.get("password", "cek email")
        await query.edit_message_text(
            f"✅ *AKUN PREMIUM SIAP!*\n\n📧 Email: `{email}`\n🔑 Password: `{password}`\n\n🎉 Selamat berkarya!",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 Buat Lagi", callback_data="buat_akun")],
                [InlineKeyboardButton("🏠 Menu", callback_data="menu")]
            ])
        )
    else:
        await query.edit_message_text(f"❌ *Gagal!*", parse_mode="Markdown")

# ========== CEK KUOTA ==========
async def cek_kuota(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "📊 *CEK KUOTA*\n\n⚡ Limit: 5 Akun/Jam\n🔄 Reset setiap jam",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Kembali", callback_data="menu")]
        ])
    )

# ========== PANDUAN ==========
async def panduan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "📖 *PANDUAN*\n\n1. Klik 'Buat Akun Premium'\n2. Tunggu 3-5 detik\n3. Login ke Alight Motion!",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Kembali", callback_data="menu")]
        ])
    )

# ========== DEVELOPER ==========
async def developer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "👨‍💻 *DEVELOPER*\n\n📱 Telegram: @limprincee",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Kembali", callback_data="menu")],
            [InlineKeyboardButton("📱 Hubungi", url="https://t.me/limprincee")]
        ])
    )

# ========== MENU ==========
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("🚀 Buat Akun Premium", callback_data="buat_akun")],
        [InlineKeyboardButton("📊 Cek Kuota", callback_data="cek_kuota")],
        [InlineKeyboardButton("📖 Panduan", callback_data="panduan")],
        [InlineKeyboardButton("👨‍💻 Developer", callback_data="dev")]
    ]
    await query.edit_message_text(
        "👋 *MENU UTAMA*\n\nPilih menu di bawah:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

# ========== REGISTER HANDLER ==========
bot_app.add_handler(CommandHandler("start", start))
bot_app.add_handler(CallbackQueryHandler(buat_akun, pattern="buat_akun"))
bot_app.add_handler(CallbackQueryHandler(cek_kuota, pattern="cek_kuota"))
bot_app.add_handler(CallbackQueryHandler(panduan, pattern="panduan"))
bot_app.add_handler(CallbackQueryHandler(developer, pattern="dev"))
bot_app.add_handler(CallbackQueryHandler(menu, pattern="menu"))

# ========== ROUTE FLASK ==========
@flask_app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return "Bot is running!"
    
    if request.method == "POST":
        try:
            body = request.get_json()
            if body:
                update = Update.de_json(body, bot_app.bot)
                bot_app.process_update(update)
                return jsonify({"status": "ok"}), 200
            return jsonify({"status": "error"}), 400
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

# ========== INI YANG DI PANGGIL VERCEL ==========
app = flask_app  # <--- INI PENTING! VERCEL CARI VARIABLE NAMA 'app'
