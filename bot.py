import logging
import os
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, ConversationHandler

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Состояния
MAIN_MENU, TEST_QUESTIONS = range(2)

# Тестовые вопросы и ответы
TEST_QUESTIONS_DATA = {
    "К какому специалисту мне маму отвезти при рмж? К неврологу?": "По вашему вопросу, следует обратиться не к неврологу, а к онкологу, так как диагностика и лечение рака молочной железы относится к их области ответственности. Важно, чтобы маму осмотрели опытные специалисты в области онкологии, которые смогут провести необходимые диагностические процедуры и разработать соответствующее лечение.",
    
    "Надо делать молекулярно-генетическое исследование при раке молочной железы?": "При раке молочной железы молекулярно-генетическое исследование является важным диагностическим инструментом, который помогает в определении типа рака, его агрессивности и выбора оптимальной стратегии лечения. В соответствии с предоставленными документами, это исследование включает анализ экспрессии рецепторов эстрогеновых (РЭ) и прогестероновых (РП) гормонов, а также определение уровня экспрессии HER2 и Ki67. Эти данные используются для разработки индивидуальной программы лечения, включая возможность применения препаратов, блокирующих рецепторы гормонов, или использование антигормональных препаратов. Кроме того, определение мутаций в гене PIK3CA может способствовать принятию решений о назначении дополнительных лекарственных средств. Таким образом, молекулярно-генетическое исследование является неотъемлемой частью диагностики и планирования лечения рака молочной железы.",
    
    "Полипы удаляют из кишки и берут на биопсию. Разве это плохо при раке кишки?": "Удаление полипов из кишки и их последующая биопсия является стандартной процедурой для диагностики рака кишечника, включая рак ободочной кишки и ректосигмоидного перехода. Это позволяет выявить наличие злокачественных клеток и определить тип заболевания. Биопсия помогает точно установить диагноз и определить необходимость дальнейшего лечения. Поэтому удаление и биопсия полипов не являются плохими действиями при раке кишечника."
}

# Главное меню
def main_menu_keyboard():
    keyboard = [
        [KeyboardButton("Вопросы по льготам")],
        [KeyboardButton("Вопросы по диагностике/профилактике/реабилитации")],
        [KeyboardButton("Дорожные карты")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Меню тестовых вопросов
def test_questions_keyboard():
    keyboard = [
        [KeyboardButton("К какому специалисту мне маму отвезти при рмж? К неврологу?")],
        [KeyboardButton("Надо делать молекулярно-генетическое исследование при раке молочной железы?")],
        [KeyboardButton("Полипы удаляют из кишки и берут на биопсию. Разве это плохо при раке кишки?")],
        [KeyboardButton("Назад в меню")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Меню дорожных карт
def roadmaps_menu_keyboard():
    keyboard = [
        [KeyboardButton("Рак кишечника")],
        [KeyboardButton("Назад в меню")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Команда /start
async def start(update: Update, context: CallbackContext) -> int:
    user = update.effective_user
    welcome_text = f"""Привет, {user.first_name}!

Добро пожаловать в ОнкоКонсультант! Я помогу вам с вопросами по онкологическим заболеваниям.

Выберите интересующую вас опцию:"""

    await update.message.reply_text(welcome_text, reply_markup=main_menu_keyboard())
    return MAIN_MENU

# Обработка главного меню
async def handle_main_menu(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    
    if text == "Вопросы по льготам":
        await update.message.reply_text(
            "Бот в разработке, скоро подключим!",
            reply_markup=main_menu_keyboard()
        )
        return MAIN_MENU
    
    elif text == "Вопросы по диагностике/профилактике/реабилитации":
        await update.message.reply_text(
            "Бот в разработке. Выберите тестовые вопросы:",
            reply_markup=test_questions_keyboard()
        )
        return TEST_QUESTIONS
    
    elif text == "Дорожные карты":
        await update.message.reply_text(
            "Выберите тип рака:",
            reply_markup=roadmaps_menu_keyboard()
        )
        return MAIN_MENU
    
    else:
        await update.message.reply_text(
            "Пожалуйста, выберите опцию из меню:",
            reply_markup=main_menu_keyboard()
        )
        return MAIN_MENU

# Обработка тестовых вопросов
async def handle_test_questions(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    
    if text == "Назад в меню":
        await update.message.reply_text(
            "Возвращаемся в главное меню:",
            reply_markup=main_menu_keyboard()
        )
        return MAIN_MENU
    
    elif text in TEST_QUESTIONS_DATA:
        await update.message.reply_text(
            TEST_QUESTIONS_DATA[text],
            reply_markup=test_questions_keyboard()
        )
        return TEST_QUESTIONS
    
    else:
        await update.message.reply_text(
            "Пожалуйста, выберите вопрос из списка:",
            reply_markup=test_questions_keyboard()
        )
        return TEST_QUESTIONS

# Обработка дорожных карт
async def handle_roadmaps(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    
    if text == "Назад в меню":
        await update.message.reply_text(
            "Возвращаемся в главное меню:",
            reply_markup=main_menu_keyboard()
        )
        return
    
    elif text == "Рак кишечника":
        await update.message.reply_text(
            "Дорожная карта по раку кишечника скоро будет доступна.",
            reply_markup=roadmaps_menu_keyboard()
        )
    
    else:
        await update.message.reply_text(
            "Пожалуйста, выберите тип рака из меню:",
            reply_markup=roadmaps_menu_keyboard()
        )

# Обработчик для любых других сообщений
async def handle_message(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "Пожалуйста, используйте /start для начала работы.",
        reply_markup=main_menu_keyboard()
    )

def main():
    # ТОКЕН ВСТАВЛЕН ПРЯМО В КОД
    token = "8637527383:AAHwmJkpd59oek3mAFJUtXW5QWG8EEE8ch8"
    
    if not token:
        logger.error("Токен не найден!")
        return
    
    logger.info("Бот запускается...")
    logger.info(f"Используется токен: {token[:10]}...")  # Логируем первые 10 символов токена
    
    try:
        application = Application.builder().token(token).build()
        
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', start)],
            states={
                MAIN_MENU: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, handle_main_menu)
                ],
                TEST_QUESTIONS: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, handle_test_questions)
                ],
            },
            fallbacks=[CommandHandler('start', start)],
            allow_reentry=True
        )
        
        application.add_handler(conv_handler)
        application.add_handler(MessageHandler(
            filters.Regex('^(Рак кишечника|Назад в меню)$') & ~filters.COMMAND,
            handle_roadmaps
        ))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        logger.info("Бот успешно инициализирован, запускаем polling...")
        application.run_polling()
        
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")

if __name__ == '__main__':
    main()
