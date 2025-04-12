import telebot
from telebot import types

token = '8154534703:AAHLLUapRWpb3yh-JPOirGp_DAYy4gy-dOM'
bot = telebot.TeleBot(token)

# Словарь для хранения состояний пользователей
user_states = {}


@bot.message_handler(commands=['start'])
def main(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('📢 Реклама', callback_data='advertising')
    btn2 = types.InlineKeyboardButton('🛠 Заказать услугу', callback_data='order_service')
    btn3 = types.InlineKeyboardButton('🤝 Партнёрство', callback_data='partnership')
    markup.row(btn1, btn2)
    markup.row(btn3)

    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! Выберите интересующий вас раздел:',
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'advertising':
        bot.send_message(callback.message.chat.id,
                         '📢 Рекламные услуги:\n- Настройка таргетированной рекламы\n- Контекстная реклама\n- SMM продвижение\n\nСвяжитесь с менеджером @RodionScriptSquad')
    elif callback.data == 'order_service':
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('🌐 Сайты', callback_data='sites')
        btn2 = types.InlineKeyboardButton('🤖 Боты', callback_data='bots')
        btn3 = types.InlineKeyboardButton('🎮 Игры', callback_data='games')
        btn4 = types.InlineKeyboardButton('📈 Маркетинг', callback_data='marketing')
        btn5 = types.InlineKeyboardButton('📢 Ведение каналов', callback_data='channel_management')
        btn6 = types.InlineKeyboardButton('💻 Софт/Программы', callback_data='software')
        btn7 = types.InlineKeyboardButton('👥 Инвайтинг', callback_data='inviting')
        btn8 = types.InlineKeyboardButton('❓ Другое', callback_data='other_services')
        markup.row(btn1, btn2)
        markup.row(btn3, btn4)
        markup.row(btn5, btn6)
        markup.row(btn7, btn8)
        bot.send_message(callback.message.chat.id, '🛠 Выберите категорию услуги:', reply_markup=markup)
    elif callback.data == 'partnership':
        bot.send_message(callback.message.chat.id,
                         '🤝 Партнёрские предложения:\n- Совместные проекты\n- Реферальные программы\n- White Label решения\n\nСвяжитесь с менеджером @RodionScriptSquad')

    # Подкатегории основных услуг
    elif callback.data == 'sites':
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Вёрстка сайтов', callback_data='web_development')
        btn2 = types.InlineKeyboardButton('Веб-приложения', callback_data='web_apps')
        markup.row(btn1, btn2)
        bot.send_message(callback.message.chat.id, '🌐 Выберите тип веб-услуги:', reply_markup=markup)

    elif callback.data == 'bots':
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Масслукинг боты', callback_data='masslooking')
        btn2 = types.InlineKeyboardButton('Нейрокомментинг', callback_data='neurocommenting')
        btn3 = types.InlineKeyboardButton('Другие виды ботов', callback_data='other_bots')
        markup.row(btn1, btn2)
        markup.row(btn3)
        bot.send_message(callback.message.chat.id, '🤖 Выберите тип бота:', reply_markup=markup)

    # Подкатегория "Другое"
    elif callback.data == 'other_services':
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('📂 Сбор папки по тематике', callback_data='folder_collection')
        btn2 = types.InlineKeyboardButton('🔍 Парсинг данных', callback_data='parsing')
        btn3 = types.InlineKeyboardButton('🎨 Дизайн (посты/группы)', callback_data='design')
        btn4 = types.InlineKeyboardButton('😊 Стикеры/Эмодзи', callback_data='stickers')
        markup.row(btn1, btn2)
        markup.row(btn3, btn4)
        bot.send_message(callback.message.chat.id, '🔍 Дополнительные услуги:', reply_markup=markup)

    # Обработка всех услуг
    service_names = {
        'web_development': 'Вёрстка сайтов',
        'web_apps': 'Создание веб-приложений',
        'masslooking': 'Боты для масслукинга',
        'neurocommenting': 'Боты с нейрокомментингом',
        'other_bots': 'Другие виды ботов',
        'games': 'Разработка игр',
        'marketing': 'Маркетинговые услуги',
        'channel_management': 'Ведение каналов',
        'software': 'Написание софта/программ',
        'inviting': 'Инвайтинг',
        'folder_collection': 'Сбор папки по вашей тематике',
        'parsing': 'Парсинг данных',
        'design': 'Дизайн постов/оформление группы',
        'stickers': 'Создание стикеров или эмодзи'
    }

    if callback.data in service_names:
        # Сохраняем выбранную услугу для пользователя
        user_states[callback.from_user.id] = {
            'service': service_names[callback.data],
            'waiting_for_description': True
        }

        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton('Пропустить', callback_data='skip_description')
        markup.add(btn)

        bot.send_message(
            callback.message.chat.id,
            f'✅ Вы выбрали: {service_names[callback.data]}\n\n'
            'Пожалуйста, опишите ваш проект или задайте вопросы (или нажмите "Пропустить"):',
            reply_markup=markup
        )

    elif callback.data == 'skip_description':
        if callback.from_user.id in user_states:
            service = user_states[callback.from_user.id]['service']
            del user_states[callback.from_user.id]  # Удаляем состояние пользователя

            # Отправляем уведомление менеджеру
            manager_chat_id = -1002293114929  # Замените на реальный chat_id менеджера
            bot.send_message(
                manager_chat_id,
                f'Новая заявка на услугу: {service}\n'
                f'Пользователь: @{callback.from_user.username or callback.from_user.first_name}\n'
                f'ID: {callback.from_user.id}\n'
                'Описание: не предоставлено'
            )

            bot.send_message(
                callback.message.chat.id,
                '✅ Ваша заявка принята!\n\n'
                'Все данные переданы менеджеру. Ожидайте ответа в ближайшее время.\n'
                'Менеджер свяжется с вами @RodionScriptSquad\nы\n'
                'Для возврата в меню нажмите /start'
            )


@bot.message_handler(content_types=['text'])
def handle_text(message):
    # Проверяем, ожидаем ли мы описание от этого пользователя
    if message.from_user.id in user_states and user_states[message.from_user.id]['waiting_for_description']:
        service = user_states[message.from_user.id]['service']
        user_description = message.text
        del user_states[message.from_user.id]  # Удаляем состояние пользователя

        # 1. Сначала отправляем подтверждение пользователю
        bot.send_message(
            message.chat.id,
            '✅ Спасибо! Ваша заявка принята.\n\n'
            f'<b>Услуга:</b> {service}\n'
            f'<b>Ваше описание:</b> {user_description}\n\n'
            'Все данные переданы менеджеру. Ожидайте ответа в ближайшее время.\n'
            'Менеджер свяжется с вами @RodionScriptSquad\n\n'
            'Для возврата в меню нажмите /start',
            parse_mode='HTML'
        )
        try:
            bot.send_message(
                -1002293114929,  # Замените на реальный chat_id менеджера
                f'📩 Новая заявка на услугу:\n\n'
                f'<b>Услуга:</b> {service}\n'
                f'<b>Пользователь:</b> @{message.from_user.username or message.from_user.first_name}\n'
                f'<b>ID:</b> {message.from_user.id}\n'
                f'<b>Описание:</b>\n{user_description}',
                parse_mode='HTML'
            )
        except Exception as e:
            print(f"Ошибка при отправке сообщения менеджеру: {e}")

    else:
        # Если это обычное сообщение, не связанное с заказом услуги
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton('Меню услуг', callback_data='order_service')
        markup.add(btn)

        bot.send_message(
            message.chat.id,
            "ℹ️ Пожалуйста, используйте кнопки меню или команду /start для взаимодействия с ботом.\n"
            "Если вы хотите заказать услугу, нажмите кнопку ниже:",
            reply_markup=markup
        )


bot.infinity_polling()

