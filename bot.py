import os
import telegram
from telegram.ext import Updater, CommandHandler
import requests

# 从环境变量获取 Telegram Bot Token
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

# 查询 USDT 余额（这里以 Tron 网络为例，占位实现）
def get_usdt_balance(address):
    try:
        # 示例 API 请求（替换为真实的 TronGrid 或其他 API）
        url = f"https://api.trongrid.io/v1/accounts/{address}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            # 假设返回数据中包含 USDT 余额（需根据实际 API 调整）
            usdt_balance = data.get("trc20", {}).get("USDT", 0) / 10**6  # USDT 有 6 位小数
            return usdt_balance
        return "无法获取余额，请检查地址或网络"
    except Exception as e:
        return f"查询失败：{str(e)}"

# /start 命令处理
def start(update, context):
    user = update.message.from_user
    message = f"你好，{user.first_name}！我是 USDT 余额查询机器人。\n请使用 /balance <你的地址> 查询余额。"
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

# /balance 命令处理
def balance(update, context):
    try:
        address = context.args[0]
        usdt_balance = get_usdt_balance(address)
        message = f"地址 {address} 的 USDT 余额为：{usdt_balance} USDT"
    except IndexError:
        message = "请提供一个地址，例如：/balance TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

# 主函数
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # 注册命令
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("balance", balance))

    # 启动机器人
    updater.start_polling()
    print("Bot is running...")
    updater.idle()

if __name__ == "__main__":
    main()
