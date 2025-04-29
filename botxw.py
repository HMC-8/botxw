import random
from collections import Counter
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters

# Các mã màu sẽ không dùng trực tiếp trên Telegram, thay vào đó sẽ hiển thị văn bản thuần túy

# Định nghĩa các phòng và nhân vật
phong = {
    "Nhà kho": "NK",
    "Phòng họp": "PH",
    "Phòng giám đốc": "PGD",
    "Phòng trò chuyện": "PTC",
    "Phòng giám sát": "PGS",
    "Văn phòng": "VP",
    "Phòng tài vụ": "PTV",
    "Phòng nhân sự": "PNS",
}

phong_keys = list(phong.values())
SO_LAN_MO_PHONG = 10000

nhan_vat = {
    "Bậc thầy tấn công": "BTTC",
    "Quyền sắt": "QS",
    "Thợ lặn sâu": "TLD",
    "Cơn lốc sân cỏ": "CLSC",
    "Hiệp sĩ phi nhanh": "HSPN",
    "Vua home run": "VHR",
}

nhan_vat_keys = list(nhan_vat.values())
SO_LAN_MO_NHAN_VAT = 10000

lich_su_chon = []

# Hàm hiển thị danh sách phòng
def hien_thi_danh_sach_phong():
    return "\n".join([f"{name} ({code})" for name, code in phong.items()])

# Hàm hiển thị danh sách nhân vật
def hien_thi_danh_sach_nhan_vat():
    return "\n".join([f"{name} ({code})" for name, code in nhan_vat.items()])

# Tạo một hàm xử lý lệnh /start
async def start(update: Update, context):
    await update.message.reply_text(
        "1. Vua thoát hiểm \n2. Chạy đua tốc độ \n\nNhập số tương ứng để tiếp tục.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("1", callback_data='function1')],
            [InlineKeyboardButton("2", callback_data='function2')]
        ])
    )

# Chức năng 1 - Sát thủ vào phòng
async def function1(update: Update, context):
    await update.callback_query.answer()
    await update.callback_query.message.reply_text(
        "Chọn phòng sát thủ vừa đi vào :\n" + hien_thi_danh_sach_phong() +
        "\nNhập 'exit' để kết thúc.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(key, callback_data=key) for key in phong_keys]
        ])
    )
    context.user_data['function'] = 'function1'

# Chức năng 2 - Chọn nhân vật
async def function2(update: Update, context):
    await update.callback_query.answer()
    await update.callback_query.message.reply_text(
        "Chọn nhân vật vừa được top 1 :\n" + hien_thi_danh_sach_nhan_vat() +
        "\nNhập 'exit' để kết thúc.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(key, callback_data=key) for key in nhan_vat_keys]
        ])
    )
    context.user_data['function'] = 'function2'

# Xử lý khi người dùng chọn phòng hoặc nhân vật từ các nút bấm
async def handle_callback(update: Update, context):
    choice = update.callback_query.data
    await update.callback_query.answer()

    if 'function' in context.user_data:
        if context.user_data['function'] == 'function1':
            if choice in phong_keys:
                lich_su_chon.append(choice)
                if len(lich_su_chon) > 10:
                    lich_su_chon.pop(0)

                trong_so_phong = {key: lich_su_chon.count(key) + 1 for key in phong_keys}
                adjusted_weights = []
                for key in phong_keys:
                    base_weight = trong_so_phong[key]
                    adjusted_weight = 0.05 + (0.80 - 0.05) * (base_weight / max(trong_so_phong.values()))
                    adjusted_weights.append(adjusted_weight)

                ket_qua_chon = random.choices(phong_keys, weights=adjusted_weights, k=SO_LAN_MO_PHONG)
                dem_phong = Counter(ket_qua_chon)
                xac_suat_phong = {phong_key: dem_phong[phong_key] / SO_LAN_MO_PHONG for phong_key in phong_keys}

                sorted_xac_suat = sorted(xac_suat_phong.items(), key=lambda x: x[1], reverse=True)
                top_phong = sorted_xac_suat[:3]

                result = f"Top phòng có tỉ lệ thắng cao nhất:\n"
                for i, (phong_key, xac_suat) in enumerate(top_phong):
                    ten_phong = [name for name, code in phong.items() if code == phong_key][0]
                    result += f"Top {i+1}: {ten_phong} ({phong_key}): {xac_suat * 100:.2f}%\n"

                await update.callback_query.message.reply_text(result)
                # Sau khi gửi kết quả, yêu cầu người dùng chọn phòng khác
                await update.callback_query.message.reply_text(
                    "Chọn phòng bị sát thủ vào :\n" + hien_thi_danh_sach_phong(),
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton(key, callback_data=key) for key in phong_keys]
                    ])
                )

        elif context.user_data['function'] == 'function2':
            if choice in nhan_vat_keys:
                lich_su_chon.append(choice)
                if len(lich_su_chon) > 10:
                    lich_su_chon.pop(0)

                trong_so_nhan_vat = {key: lich_su_chon.count(key) + 1 for key in nhan_vat_keys}
                adjusted_weights = []
                for key in nhan_vat_keys:
                    base_weight = trong_so_nhan_vat[key]
                    adjusted_weight = 0.05 + (0.80 - 0.05) * (base_weight / max(trong_so_nhan_vat.values()))
                    adjusted_weights.append(adjusted_weight)

                ket_qua_chon = random.choices(nhan_vat_keys, weights=adjusted_weights, k=SO_LAN_MO_NHAN_VAT)
                dem_nhan_vat = Counter(ket_qua_chon)
                xac_suat_nhan_vat = {nhan_vat_key: dem_nhan_vat[nhan_vat_key] / SO_LAN_MO_NHAN_VAT for nhan_vat_key in nhan_vat_keys}

                sorted_xac_suat = sorted(xac_suat_nhan_vat.items(), key=lambda x: x[1], reverse=True)
                top_nhan_vat = sorted_xac_suat[:3]

                result = f"Nhân vật có tỉ lệ thắng cao nhất:\n"
                for i, (nhan_vat_key, xac_suat) in enumerate(top_nhan_vat):
                    ten_nhan_vat = [name for name, code in nhan_vat.items() if code == nhan_vat_key][0]
                    result += f"Top {i+1}: {ten_nhan_vat} ({nhan_vat_key}): {xac_suat * 100:.2f}%\n"

                await update.callback_query.message.reply_text(result)
                # Sau khi gửi kết quả, yêu cầu người dùng chọn nhân vật tiếp theo
                await update.callback_query.message.reply_text(
                    "Chọn nhân vật Top 1 ván trước đó :\n" + hien_thi_danh_sach_nhan_vat(),
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton(key, callback_data=key) for key in nhan_vat_keys]
                    ])
                )

# Xử lý khi người dùng nhập tin nhắn (cho chức năng exit)
async def handle_message(update: Update, context):
    text = update.message.text.strip().upper()
    if text == 'EXIT':
        await update.message.reply_text("Đã tắt tool.")
        return

# Khởi tạo bot
def main():
    application = Application.builder().token("8098068745:AAEcbWON14O-1HldsUEE34144u-wMPMKxPk").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(function1, pattern='function1'))
    application.add_handler(CallbackQueryHandler(function2, pattern='function2'))
    application.add_handler(CallbackQueryHandler(handle_callback))

    application.run_polling()

if __name__ == '__main__':
    main()