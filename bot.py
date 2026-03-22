import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, ConversationHandler, CallbackQueryHandler
import sqlite3
from datetime import datetime
import os

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
    user = update.message.from_user
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
async def handle_roadmaps(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    
    if text == "Назад в меню":
        await update.message.reply_text(
            "Возвращаемся в главное меню:",
            reply_markup=main_menu_keyboard()
        )
        return MAIN_MENU
    
    elif text == "Рак кишечника":
        # Путь к PDF файлу на PythonAnywhere
        # Создайте папку 'files' в вашей директории и поместите туда PDF
        pdf_path = os.path.join(os.path.dirname(__file__), 'files', 'colorectal_cancer_roadmap.pdf')
        
        try:
            # Проверяем, существует ли файл
            if os.path.exists(pdf_path):
                # Отправляем PDF документ
                with open(pdf_path, 'rb') as pdf_file:
                    await update.message.reply_document(
                        document=pdf_file,
                        filename='roadmap_colorectal_cancer.pdf',
                        caption="Дорожная карта по раку кишечника"
                    )
            else:
                # Если файл не найден
                await update.message.reply_text(
                    "Файл с дорожной картой временно недоступен. Пожалуйста, попробуйте позже.",
                    reply_markup=roadmaps_menu_keyboard()
                )
        except Exception as e:
            logger.error(f"Ошибка при отправке PDF: {e}")
            await update.message.reply_text(
                "Произошла ошибка при отправке файла. Пожалуйста, попробуйте позже.",
                reply_markup=roadmaps_menu_keyboard()
            )
        
        return MAIN_MENU
    
    else:
        await update.message.reply_text(
            "Пожалуйста, выберите тип рака из меню:",
            reply_markup=roadmaps_menu_keyboard()
        )
        return MAIN_MENU

# Обработка неизвестных сообщений
async def handle_unknown(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text(
        "Пожалуйста, используйте кнопки меню для навигации.",
        reply_markup=main_menu_keyboard()
    )
    return MAIN_MENU

def main() -> None:
    # Замените 'YOUR_BOT_TOKEN' на токен вашего бота
    application = Application.builder().token("8299961523:AAEmzLW_-6BgXxspdxEGweUZ30b3oLqWb-s").build()
    
    # ConversationHandler для управления состояниями
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
    )
    
    application.add_handler(conv_handler)
    # Добавляем обработчик для дорожных карт (без сохранения состояния)
    application.add_handler(MessageHandler(
        filters.Regex('^(Рак кишечника|Назад в меню)$') & ~filters.COMMAND,
        handle_roadmaps
    ))
    
    # Запуск бота
    print("Бот запущен...")
    application.run_polling()

if __name__ == '__main__':
    main()