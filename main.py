import logging
from os import name, system

from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, Updater)

from binance_trader_bot import BinanceTraderBot

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

API_KEY = '-'
bot_instance = BinanceTraderBot()

class TelegramBotHandlers:
    @staticmethod
    def start(update: Update, context: CallbackContext):
        update.message.reply_text('Welcome to the Binance Trader Bot!')

    @staticmethod
    def top_trader(update: Update, context: CallbackContext):
        trader_data = bot_instance.fetch_top_trader_data()
        TelegramBotHandlers.show_trader_data(update, context, trader_data, 0)

    @staticmethod
    def handle_back(update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        query = update.callback_query
        query.answer()
        current_index = int(query.data.split('_')[-1])

        trader_data = bot_instance.fetch_top_trader_data()
        TelegramBotHandlers.show_trader_data(update, context, trader_data, current_index)

    @staticmethod
    def handle_top_traders(update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id

        trader_data = TelegramBotHandlers.top_trader()
        context.user_data['trader_data'] = trader_data

        if trader_data:
            TelegramBotHandlers.show_trader_data(update, context, trader_data, 0)
        else:
            context.bot.send_message(
                chat_id=chat_id, text="Désolé, nous n'avons pas pu récupérer les données du trader. Veuillez réessayer plus tard.")

    @staticmethod
    def generate_submenu_buttons(trader_data, current_index):
        buttons = []
        navigation_buttons = []

        if current_index > 0:
            navigation_buttons.append(InlineKeyboardButton(
                '<< Previous', callback_data=f'prev_trader_{current_index-1}'))

        if current_index < len(trader_data) - 1:
            navigation_buttons.append(InlineKeyboardButton(
                'Next >>', callback_data=f'next_trader_{current_index+1}'))

        buttons.append(navigation_buttons)
        buttons.append([InlineKeyboardButton('Statistiques détaillées',
                       callback_data=f'detailed_stats_{trader_data[current_index]["encryptedUid"]}_{current_index}')])

        return InlineKeyboardMarkup(buttons)

    @staticmethod
    def show_detailed_stats(update: Update, context: CallbackContext, detailed_stats, encrypted_uid, index):
        performance_ret_list = detailed_stats['data']['performanceRetList']

        title = "Statistiques détaillées"
        underline = "─" * len(title)

        message = f"*{title}*\n"
        message += f"{underline}\n\n"

        periods = [
            {'period_type': 'DAILY', 'title': 'DAILY'},
            {'period_type': 'WEEKLY', 'title': 'WEEKLY'},
            {'period_type': 'MONTHLY', 'title': 'MONTHLY'},
            {'period_type': 'ALL', 'title': 'ALL'}
        ]

        for period in periods:
            message += f"{period['title']}\n"
            roi_item = next(
                (item for item in performance_ret_list if item['periodType'] == period['period_type'] and item['statisticsType'] == 'ROI'), None)
            pnl_item = next(
                (item for item in performance_ret_list if item['periodType'] == period['period_type'] and item['statisticsType'] == 'PNL'), None)

            if roi_item is not None:
                message += f"ROI: Valeur: {roi_item['value']*100:.2f}, Rang: {roi_item['rank']}\n"
            if pnl_item is not None:
                message += f"PNL: Valeur: {pnl_item['value']:.2f}, Rang: {pnl_item['rank']}\n"
            message += "\n"

        back_button = InlineKeyboardButton(
            "Back", callback_data=f"back_{index}")
        keyboard = InlineKeyboardMarkup([[back_button]])

        if update.callback_query:
            update.callback_query.edit_message_text(
                text=message, parse_mode="Markdown", reply_markup=keyboard)
        else:
            update.message.reply_text(
                text=message, parse_mode="Markdown", reply_markup=keyboard)

    @staticmethod
    def show_trader_data(update: Update, context: CallbackContext, trader_data, current_index):
        trader = trader_data[current_index]

        title = "Top Rank (ALL) (Share Trade)"
        underline = "─" * len(title)
        trader_name = TelegramBotHandlers.escape_markdown_characters(
            trader['nickName'])

        message = f"*{title}*\n"
        message += f"{underline}\n\n"
        message += f"🏆 Rank: {current_index+1}\n\n"
        message += f"👤 Nickname: {trader_name}\n"
        message += f"📈 ROI: {trader['roi']:.2f}%\n"
        message += f"💰 PNL: {trader['pnl']:.2f}\n"
        message += f"👥 Follower Count: {trader['followerCount']}\n"
        message += "\n"

        buttons = TelegramBotHandlers.generate_submenu_buttons(
            trader_data, current_index)
        if update.callback_query:
            update.callback_query.edit_message_text(
                text=message, reply_markup=buttons, parse_mode="Markdown")
        else:
            update.message.reply_text(
                text=message, reply_markup=buttons, parse_mode="Markdown")

    @staticmethod
    def escape_markdown_characters(text):
        characters = ['_', '*', '[', ']',
                      '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
        for char in characters:
            text = text.replace(char, '\\' + char)
        return text

    @staticmethod
    def navigate_trader(update: Update, context: CallbackContext):
        query = update.callback_query
        query.answer()

        trader_data = bot_instance.fetch_top_trader_data()
        trader_data.sort(key=lambda x: x['rank'])

        current_index = int(query.data.split('_')[-1])
        TelegramBotHandlers.show_trader_data(
            update, context, trader_data, current_index)

    @staticmethod
    def handle_detailed_stats(update: Update, context: CallbackContext):
        query = update.callback_query
        query.answer()

        encrypted_uid = query.data.split('_')[-2]
        current_index = query.data.split('_')[-1]
        detailed_stats = BinanceTraderBot.fetch_detailed_stats(encrypted_uid)

        if detailed_stats:
            TelegramBotHandlers.show_detailed_stats(
                update, context, detailed_stats, encrypted_uid, current_index)
        else:
            query.edit_message_text(
                "Désolé, nous n'avons pas pu récupérer les statistiques détaillées. Veuillez réessayer plus tard.")

from asyncio import Queue
update_queue = Queue()

def main():

    clear, back_slash = "clear", "/"
    if name == "nt":
        clear, back_slash = "cls", "\\"

    system(clear)

    bot = Bot(token=API_KEY)
    updater = Updater(bot=bot, update_queue=update_queue)
    dp = updater.dispatcher

    handlers = TelegramBotHandlers()
    dp.add_handler(CommandHandler("start", handlers.start))
    dp.add_handler(CommandHandler("stat", handlers.top_trader))
    dp.add_handler(CallbackQueryHandler(handlers.navigate_trader,
                   pattern='^(prev_trader|next_trader)_'))
    dp.add_handler(CallbackQueryHandler(
        handlers.handle_detailed_stats, pattern='^detailed_stats_'))
    dp.add_handler(CallbackQueryHandler(
        handlers.handle_back, pattern='^back_'))
    dp.add_handler(CommandHandler('follow', BinanceTraderBot.fetch_trader_data, pass_args=True, pass_update_queue=True))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
