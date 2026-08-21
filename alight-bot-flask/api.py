import requests
import json
from flask import Flask, request, jsonify
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ========== KONFIGURASI ==========
TOKEN = "8277774482:AAG-g5wFCw-1XMWHdtAs6TJMbhXS6J58ims"  # GANTI INI!
API_KEY = "alight_live_a74eeaf872c56e0d9a23b41a7bc5fb8b"
API_URL = "https://am.rafaelxd.my.id/api/v1/auto-activate"

# ========== HEADERS API ==========
HEADERS = {
    "Content-Type": "application/json",
    "x-api-key": API_KEY
}

# ========== BUAT APPLICATION TELEGRAM ==========
app = Application.builder().token(TOKEN).build()

# ========== FUNGSI PANGGIL API ==========
async def create_account():
    try:
        response = requests.post(API_URL, json={}, headers=HEADERS, timeout=30)
        return response.json()
    except Exception as e:
        return {"status": "error", "message": f"Gagal konek ke API: {str(e)}"}

# ========== COMMAND /START ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🚀 Buat Akun Premium", callback_data="buat_akun")],
        [InlineKeyboardButton("📊 Cek Kuota", callback_data="cek_kuota")],
        [InlineKeyboardButton("📖 Panduan", callback_data="panduan")],
        [InlineKeyboardButton("👨‍💻 Developer", callback_data="dev")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "👋 *Selamat Datang!*\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "⚡ *ALIGHT MOTION PREMIUM BOT*\n\n"
        "Klik tombol di bawah untuk mulai:\n",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# ========== CALLBACK BUAT AKUN ==========
async def buat_akun(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        "⏳ *Sedang membuat akun...*\nMohon tunggu 3-5 detik...",
        parse_mode="Markdown"
    )
    
    result = await create_account()
    
    if result.get("status") == "success":
        email = result.get("email", "gak tersedia")
        password = result.get("password", "cek email")
        
        await query.edit_message_text(
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "✅ *AKUN PREMIUM SIAP!*\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"📧 *Email* : `{email}`\n"
            f"🔑 *Password* : `{password}`\n\n"
            "📲 *Cara Login:*\n"
            "1. Buka Alight Motion\n"
            "2. Pilih Login dengan Email\n"
            "3. Masukkan email & password di atas\n\n"
            "🎉 Selamat berkarya!",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 Buat Lagi", callback_data="buat_akun")],
                [InlineKeyboardButton("🏠 Menu Utama", callback_data="menu")]
            ])
        )
    else:
        await query.edit_message_text(
            f"❌ *Gagal membuat akun!*\nError: {result.get('message', 'Coba lagi nanti')}",
            parse_mode="Markdown"
        )

# ========== CEK KUOTA ==========
async def cek_kuota(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "📊 *CEK KUOTA*\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "⚡ *Limit Standar:* 5 Akun/Jam\n"
        "⚡ *Limit API:* 15 Request/Jam\n"
        "📌 *Sisa Kuota Hari Ini:*\n"
        "  • 0 / 5 Akun terpakai\n"
        "  • 0 / 15 Request terpakai\n\n"
        "🔄 Reset setiap awal jam\n\n"
        "Gunakan dengan bijak! 🚀",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Kembali ke Menu", callback_data="menu")]
        ])
    )

# ========== PANDUAN ==========
async def panduan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "📖 *PANDUAN PENGGUNAAN*\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "1️⃣ Klik *'Buat Akun Premium'*\n"
        "2️⃣ Tunggu 3-5 detik\n"
        "3️⃣ Dapatkan email & password\n"
        "4️⃣ Login ke Alight Motion!\n\n"
        "⚠️ *Batasan:*\n"
        "• 5 akun per jam\n"
        "• Reset setiap awal jam\n\n"
        "🔒 Aman & terpercaya!",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Kembali ke Menu", callback_data="menu")]
        ])
    )

# ========== DEVELOPER ==========
async def developer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "👨‍💻 *DEVELOPER BOT*\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "📌 *Nama* : Princee\n"
        "📱 *Telegram* : @limprincee\n"
        "📧 *Email* : limprincee@gmail.com\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "🌟 *Fitur Bot:*\n"
        "• Aktivasi Akun Alight Motion Premium\n"
        "• Auto-generate email & password\n"
        "• Cepat & Mudah\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "💬 *Kritik & Saran:*\n"
        "Hubungi developer langsung ya!\n\n"
        "🙏 Terima kasih sudah menggunakan bot ini!",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Kembali ke Menu", callback_data="menu")],
            [InlineKeyboardButton("📱 Hubungi Developer", url="https://t.me/limprincee")]
        ])
    )

# ========== MENU UTAMA ==========
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("🚀 Buat Akun Premium", callback_data="buat_akun")],
        [InlineKeyboardButton("📊 Cek Kuota", callback_data="cek_kuota")],
        [InlineKeyboardButton("📖 Panduan", callback_data="panduan")],
        [InlineKeyboardButton("👨‍💻 Developer", callback_data="dev")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "👋 *MENU UTAMA*\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "⚡ *ALIGHT MOTION PREMIUM BOT*\n\n"
        "Pilih menu di bawah ini:\n",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# ========== REGISTER HANDLERS ==========
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buat_akun, pattern="buat_akun"))
app.add_handler(CallbackQueryHandler(cek_kuota, pattern="cek_kuota"))
app.add_handler(CallbackQueryHandler(panduan, pattern="panduan"))
app.add_handler(CallbackQueryHandler(developer, pattern="dev"))
app.add_handler(CallbackQueryHandler(menu, pattern="menu"))

# ========== FLASK APP ==========
flask_app = Flask(__name__)

@flask_app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return "Bot is running! Use /start in Telegram."
    
    if request.method == "POST":
        try:
            body = request.get_json()
            if not body:
                return jsonify({"status": "error", "message": "Invalid JSON"}), 400
            
            update = Update.de_json(body, app.bot)
            app.process_update(update)
            return jsonify({"status": "ok"}), 200
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

@flask_app.route("/webhook", methods=["POST"])
def webhook():
    try:
        body = request.get_json()
        if not body:
            return jsonify({"status": "error", "message": "Invalid JSON"}), 400
        
        update = Update.de_json(body, app.bot)
        app.process_update(update)
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# ========== UNTUK LOCAL TESTING ==========
if __name__ == "__main__":
    print("✅ Bot running on http://localhost:5000")
    flask_app.run(debug=True, port=5000)
