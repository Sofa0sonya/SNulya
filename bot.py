import logging
import os
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Токен бота
TOKEN = "8637527383:AAHwmJkpd59oek3mAFJUtXW5QWG8EEE8ch8"

# Тестовые вопросы и ответы
TEST_QUESTIONS_DATA = {
    "К какому специалисту мне маму отвезти при рмж? К неврологу?": "По вашему вопросу, следует обратиться не к неврологу, а к онкологу, так как диагностика и лечение рака молочной железы относится к их области ответственности. Важно, чтобы маму осмотрели опытные специалисты в области онкологии, которые смогут провести необходимые диагностические процедуры и разработать соответствующее лечение.",
    
    "Надо делать молекулярно-генетическое исследование при раке молочной железы?": "При раке молочной железы молекулярно-генетическое исследование является важным диагностическим инструментом, который помогает в определении типа рака, его агрессивности и выбора оптимальной стратегии лечения. В соответствии с предоставленными документами, это исследование включает анализ экспрессии рецепторов эстрогеновых (РЭ) и прогестероновых (РП) гормонов, а также определение уровня экспрессии HER2 и Ki67. Эти данные используются для разработки индивидуальной программы лечения, включая возможность применения препаратов, блокирующих рецепторы гормонов, или использование антигормональных препаратов. Кроме того, определение мутаций в гене PIK3CA может способствовать принятию решений о назначении дополнительных лекарственных средств. Таким образом, молекулярно-генетическое исследование является неотъемлемой частью диагностики и планирования лечения рака молочной железы.",
    
    "Полипы удаляют из кишки и берут на биопсию. Разве это плохо при раке кишки?": "Удаление полипов из кишки и их последующая биопсия является стандартной процедурой для диагностики рака кишечника, включая рак ободочной кишки и ректосигмоидного перехода. Это позволяет выявить наличие злокачественных клеток и определить тип заболевания. Биопсия помогает точно установить диагноз и определить необходимость дальнейшего лечения. Поэтому удаление и биопсия полипов не являются плохими действиями при раке кишечника."
}

# Состояния для ConversationHandler
MAIN_MENU, TEST_QUESTIONS_MENU, ROADMAPS_MENU = range(3)

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
        [KeyboardButton("◀️ Назад в главное меню")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Меню дорожных карт
def roadmaps_menu_keyboard():
    keyboard = [
        [KeyboardButton("📄 Рак кишечника")],
        [KeyboardButton("◀️ Назад в главное меню")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправляет приветствие и показывает меню"""
    user = update.effective_user
    logger.info(f"Пользователь {user.id} ({user.first_name}) запустил бота")
    
    welcome_text = f"""Привет, {user.first_name}!

Добро пожаловать в ОнкоКонсультант! Я помогу вам с вопросами по онкологическим заболеваниям.

Выберите интересующую вас опцию:"""
    
    await update.message.reply_text(welcome_text, reply_markup=main_menu_keyboard())
    return MAIN_MENU

# Обработка главного меню
async def handle_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает сообщения в главном меню"""
    text = update.message.text
    user = update.effective_user
    
    logger.info(f"Главное меню, сообщение от {user.id}: {text}")
    
    if text == "Вопросы по льготам":
        await update.message.reply_text(
            "Бот в разработке, скоро подключим!",
            reply_markup=main_menu_keyboard()
        )
        return MAIN_MENU
    
    elif text == "Вопросы по диагностике/профилактике/реабилитации":
        await update.message.reply_text(
            "Выберите интересующий вас вопрос:",
            reply_markup=test_questions_keyboard()
        )
        return TEST_QUESTIONS_MENU
    
    elif text == "Дорожные карты":
        await update.message.reply_text(
            "Выберите тип рака для получения дорожной карты:",
            reply_markup=roadmaps_menu_keyboard()
        )
        return ROADMAPS_MENU
    
    else:
        await update.message.reply_text(
            "Пожалуйста, используйте кнопки меню для навигации.",
            reply_markup=main_menu_keyboard()
        )
        return MAIN_MENU

# Обработка тестовых вопросов
async def handle_test_questions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает выбор тестовых вопросов"""
    text = update.message.text
    user = update.effective_user
    
    logger.info(f"Тестовые вопросы, сообщение от {user.id}: {text}")
    
    if text == "◀️ Назад в главное меню":
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
        return TEST_QUESTIONS_MENU
    
    else:
        await update.message.reply_text(
            "Пожалуйста, выберите вопрос из списка:",
            reply_markup=test_questions_keyboard()
        )
        return TEST_QUESTIONS_MENU

# Обработка дорожных карт
async def handle_roadmaps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает выбор дорожных карт и отправляет PDF"""
    text = update.message.text
    user = update.effective_user
    
    logger.info(f"Дорожные карты, сообщение от {user.id}: {text}")
    
    if text == "◀️ Назад в главное меню":
        await update.message.reply_text(
            "Возвращаемся в главное меню:",
            reply_markup=main_menu_keyboard()
        )
        return MAIN_MENU
    
    elif text == "📄 Рак кишечника":
        # Путь к PDF файлу
        pdf_path = os.path.join(os.path.dirname(__file__), 'files', 'colorectal_cancer_roadmap.pdf')
        
        logger.info(f"Ищем PDF файл по пути: {pdf_path}")
        
        # Проверяем, существует ли файл
        if os.path.exists(pdf_path):
            try:
                # Отправляем PDF документ
                with open(pdf_path, 'rb') as pdf_file:
                    await update.message.reply_document(
                        document=pdf_file,
                        filename="dorozhnaya_karta_rak_kishechnika.pdf",
                        caption="📄 Дорожная карта по раку кишечника\n\nСохраните этот файл для ознакомления."
                    )
                logger.info(f"PDF файл успешно отправлен пользователю {user.id}")
                
                # После отправки возвращаемся в меню дорожных карт
                await update.message.reply_text(
                    "✅ Файл отправлен! Выберите другой тип рака или вернитесь в меню:",
                    reply_markup=roadmaps_menu_keyboard()
                )
                return ROADMAPS_MENU
                
            except Exception as e:
                logger.error(f"Ошибка при отправке PDF: {e}")
                await update.message.reply_text(
                    "❌ Произошла ошибка при отправке файла. Пожалуйста, попробуйте позже.",
                    reply_markup=roadmaps_menu_keyboard()
                )
                return ROADMAPS_MENU
        else:
            # Если файл не найден
            logger.error(f"PDF файл не найден: {pdf_path}")
            
            # Показываем список доступных файлов для отладки
            files_dir = os.path.join(os.path.dirname(__file__), 'files')
            if os.path.exists(files_dir):
                available_files = os.listdir(files_dir)
                logger.info(f"Доступные файлы в папке files: {available_files}")
            
            await update.message.reply_text(
                "❌ Файл с дорожной картой временно недоступен.\n\n"
                "Пожалуйста, сообщите администратору о проблеме.",
                reply_markup=roadmaps_menu_keyboard()
            )
            return ROADMAPS_MENU
    
    else:
        await update.message.reply_text(
            "Пожалуйста, выберите тип рака из меню:",
            reply_markup=roadmaps_menu_keyboard()
        )
        return ROADMAPS_MENU

# Обработчик неизвестных сообщений
async def handle_unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает сообщения, которые не попали в другие обработчики"""
    await update.message.reply_text(
        "Пожалуйста, используйте кнопки меню для навигации или отправьте /start для перезапуска.",
        reply_markup=main_menu_keyboard()
    )
    return MAIN_MENU

def main():
    """Запуск бота"""
    logger.info("🚀 Запуск бота...")
    
    # Проверяем наличие папки files
    files_dir = os.path.join(os.path.dirname(__file__), 'files')
    if os.path.exists(files_dir):
        logger.info(f"✅ Папка files найдена: {files_dir}")
        available_files = os.listdir(files_dir)
        logger.info(f"📁 Доступные файлы: {available_files}")
    else:
        logger.warning(f"⚠️ Папка files не найдена: {files_dir}")
    
    # Создаем приложение
    application = Application.builder().token(TOKEN).build()
    
    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(
        filters.Regex('^(Вопросы по льготам|Вопросы по диагностике/профилактике/реабилитации|Дорожные карты)$'),
        handle_main_menu
    ))
    application.add_handler(MessageHandler(
        filters.Regex('^(К какому специалисту|Надо делать|Полипы удаляют|◀️ Назад в главное меню)$'),
        handle_test_questions
    ))
    application.add_handler(MessageHandler(
        filters.Regex('^(📄 Рак кишечника|◀️ Назад в главное меню)$'),
        handle_roadmaps
    ))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_unknown))
    
    # Запускаем бота
    logger.info("✅ Бот запущен и готов к работе!")
    application.run_polling()

if __name__ == '__main__':
    main()
