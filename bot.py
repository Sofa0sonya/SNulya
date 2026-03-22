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

# Создаем папку files если её нет
files_dir = os.path.join(os.path.dirname(__file__), 'files')
if not os.path.exists(files_dir):
    os.makedirs(files_dir)
    logger.info(f"Создана папка: {files_dir}")

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
        [KeyboardButton("◀️ Назад")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Меню дорожных карт
def roadmaps_menu_keyboard():
    keyboard = [
        [KeyboardButton("📄 Рак кишечника")],
        [KeyboardButton("◀️ Назад")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Состояния пользователей
user_states = {}

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправляет приветствие и показывает меню"""
    user = update.effective_user
    user_id = user.id
    
    logger.info(f"Пользователь {user_id} ({user.first_name}) запустил бота")
    
    # Сбрасываем состояние пользователя
    user_states[user_id] = "main"
    
    welcome_text = f"""Привет, {user.first_name}!

Добро пожаловать в ОнкоКонсультант! Я помогу вам с вопросами по онкологическим заболеваниям.

Выберите интересующую вас опцию:"""
    
    await update.message.reply_text(welcome_text, reply_markup=main_menu_keyboard())

# Обработка всех текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает все текстовые сообщения"""
    text = update.message.text
    user = update.effective_user
    user_id = user.id
    
    logger.info(f"Сообщение от {user_id}: {text}")
    
    # Получаем текущее состояние пользователя
    state = user_states.get(user_id, "main")
    
    # Обработка команды "◀️ Назад"
    if text == "◀️ Назад":
        await update.message.reply_text(
            "Возвращаемся в главное меню:",
            reply_markup=main_menu_keyboard()
        )
        user_states[user_id] = "main"
        return
    
    # Если пользователь в главном меню
    if state == "main":
        if text == "Вопросы по льготам":
            await update.message.reply_text(
                "Бот в разработке, скоро подключим!",
                reply_markup=main_menu_keyboard()
            )
        
        elif text == "Вопросы по диагностике/профилактике/реабилитации":
            await update.message.reply_text(
                "Выберите интересующий вас вопрос:",
                reply_markup=test_questions_keyboard()
            )
            user_states[user_id] = "questions"
        
        elif text == "Дорожные карты":
            await update.message.reply_text(
                "Выберите тип рака для получения дорожной карты:",
                reply_markup=roadmaps_menu_keyboard()
            )
            user_states[user_id] = "roadmaps"
        
        else:
            await update.message.reply_text(
                "Пожалуйста, используйте кнопки меню.",
                reply_markup=main_menu_keyboard()
            )
    
    # Если пользователь в меню вопросов
    elif state == "questions":
        if text in TEST_QUESTIONS_DATA:
            await update.message.reply_text(
                TEST_QUESTIONS_DATA[text],
                reply_markup=test_questions_keyboard()
            )
        else:
            await update.message.reply_text(
                "Пожалуйста, выберите вопрос из списка:",
                reply_markup=test_questions_keyboard()
            )
    
    # Если пользователь в меню дорожных карт
    elif state == "roadmaps":
        if text == "📄 Рак кишечника":
            # Путь к PDF файлу
            pdf_path = os.path.join(files_dir, 'colorectal_cancer_roadmap')
            
            logger.info(f"Ищем PDF файл: {pdf_path}")
            
            if os.path.exists(pdf_path):
                try:
                    with open(pdf_path, 'rb') as pdf_file:
                        await update.message.reply_document(
                            document=pdf_file,
                            filename="dorozhnaya_karta_rak_kishechnika.pdf",
                            caption="📄 Дорожная карта по раку кишечника"
                        )
                    logger.info(f"PDF отправлен пользователю {user_id}")
                    
                    await update.message.reply_text(
                        "✅ Файл отправлен! Выберите другой тип рака:",
                        reply_markup=roadmaps_menu_keyboard()
                    )
                except Exception as e:
                    logger.error(f"Ошибка отправки PDF: {e}")
                    await update.message.reply_text(
                        "❌ Ошибка при отправке файла. Попробуйте позже.",
                        reply_markup=roadmaps_menu_keyboard()
                    )
            else:
                logger.error(f"PDF не найден: {pdf_path}")
                await update.message.reply_text(
                    "❌ Файл с дорожной картой временно недоступен.",
                    reply_markup=roadmaps_menu_keyboard()
                )
        else:
            await update.message.reply_text(
                "Пожалуйста, выберите тип рака из меню:",
                reply_markup=roadmaps_menu_keyboard()
            )

def main():
    """Запуск бота"""
    logger.info("🚀 Запуск бота...")
    
    # Проверяем наличие папки files
    if os.path.exists(files_dir):
        logger.info(f"✅ Папка files: {files_dir}")
        files = os.listdir(files_dir)
        logger.info(f"📁 Файлы: {files}")
    else:
        logger.warning(f"⚠️ Папка files не создана")
    
    # Создаем приложение
    application = Application.builder().token(TOKEN).build()
    
    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Запускаем бота
    logger.info("✅ Бот запущен и готов к работе!")
    application.run_polling()

if __name__ == '__main__':
    main()
