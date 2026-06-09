import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder

# === НАСТРОЙКИ БОТА ===
# Сюда вставь токен, который ты получил у @BotFather
BOT_TOKEN = "8393848735:AAG_-YHygzhl-800epmqvbyELkmKvzS-YVc"
MY_TG_ID = 1019227039  # Твой ID, бот будет писать тебе в личку

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Шаги квеста (состояния)
class QuestStates(StatesGroup):
    q1 = State() # Фильм (Кнопки)
    q2 = State() # Как искупил вину (Текст)
    q3 = State() # Что осталось (Текст)
    q4 = State() # Первый поцелуй (Кнопки)
    q5 = State() # Вопрос "6" (Кнопки)

# Функция для создания кнопок
def make_keyboard(options: list):
    builder = InlineKeyboardBuilder()
    for option in options:
        builder.button(text=option, callback_data=option)
    builder.adjust(1)
    return builder.as_markup()

# === СТАРТ ===
@dp.message(CommandStart())
async def start_cmd(message: types.Message, state: FSMContext):
    await state.clear()
    try:
        await bot.send_message(MY_TG_ID, "🔔 Квест начался! Она запустила бота.")
    except Exception:
        pass
        
    welcome = (
        "deux mois de bonheur. ❤️\n\n"
        "Сможешь ответить на всё?) Лови первый вопрос! 👇"
    )
    await message.answer(welcome)
    await asyncio.sleep(1)
    
    text = "🍿 **Вопрос 1:** На какой мы фильм пошли, когда гуляли в первый раз?"
    options = ["Человек диван", "Крутой парень на мотоцикле", "Девка теракт", "Ждун"]
    await message.answer(text, reply_markup=make_keyboard(options), parse_mode="Markdown")
    await state.set_state(QuestStates.q1)

# === ОБРАБОТКА ВОПРОСА 1 ===
@dp.callback_query(QuestStates.q1)
async def process_q1(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == "Человек диван":
        await callback.answer("Правильно! 😂")
        await bot.send_message(MY_TG_ID, "✅ Прошла 1-й вопрос (Человек диван)")
        
        text = "💬 **Вопрос 2:** Как я искупил вину за то, что врал (про пепу и т.д)?"
        await callback.message.answer(text, parse_mode="Markdown")
        await state.set_state(QuestStates.q2)
    else:
        await callback.answer("Не-а, не угадала! ❌", show_alert=True)
        await bot.send_message(MY_TG_ID, f"❌ Ошиблась на 1-м вопросе, выбрав: {callback.data}")

# === ОБРАБОТКА ВОПРОСА 2 (ТЕКСТ) ===
@dp.message(QuestStates.q2)
async def process_q2(message: types.Message, state: FSMContext):
    answer = message.text.strip().lower()
    if "подстриг" in answer:
        await message.answer("Даа, это было мощно! Двигаемся дальше. 🔥")
        await bot.send_message(MY_TG_ID, "✅ Прошла 2-й вопрос (Подстригся)")
        await asyncio.sleep(1)
        
        text = "👀 **Вопрос 3:** Что мне осталось от тебя с первой прогулки?"
        await message.answer(text, parse_mode="Markdown")
        await state.set_state(QuestStates.q3)
    else:
        await message.answer("Хмм, нет, вспоминай лучше!")
        await bot.send_message(MY_TG_ID, f"❌ Ошиблась на 2-м вопросе, написав: {message.text}")

# === ОБРАБОТКА ВОПРОСА 3 (ТЕКСТ) ===
@dp.message(QuestStates.q3)
async def process_q3(message: types.Message, state: FSMContext):
    answer = message.text.strip().lower()
    if "заколк" in answer: 
        await message.answer("Точно! Она всё еще у меня. 🥰")
        await bot.send_message(MY_TG_ID, "✅ Прошла 3-й вопрос (Заколка)")
        await asyncio.sleep(1)
        
        text = "💋 **Вопрос 4:** Когда мы впервые поцеловались?"
        options = ["12 апреля", "11 апреля", "13 апреля", "Никогда 🥺"]
        await message.answer(text, reply_markup=make_keyboard(options), parse_mode="Markdown")
        await state.set_state(QuestStates.q4)
    else:
        await message.answer("Неправильно. Вспоминай лучше! 😉")
        await bot.send_message(MY_TG_ID, f"❌ Ошиблась на 3-м вопросе, написав: {message.text}")

# === ОБРАБОТКА ВОПРОСА 4 ===
@dp.callback_query(QuestStates.q4)
async def process_q4(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == "13 апреля":
        await callback.answer("Помнишь! ❤️")
        await bot.send_message(MY_TG_ID, "✅ Прошла 4-й вопрос (13 апреля)")
        
        text = "🔢 **Вопрос 5:**\n\n6"
        options = ["7", "8", "0", "2"]
        await callback.message.answer(text, reply_markup=make_keyboard(options), parse_mode="Markdown")
        await state.set_state(QuestStates.q5)
    else:
        await callback.answer("Подумай еще раз! 🧐", show_alert=True)
        await bot.send_message(MY_TG_ID, f"❌ Ошиблась на 4-м вопросе, выбрав: {callback.data}")

# === ФИНАЛ (ОБРАБОТКА ВОПРОСА 5) ===
@dp.callback_query(QuestStates.q5)
async def process_q5(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == "7":
        await callback.answer("Квест пройден! 🏆")
        await state.clear()
        await bot.send_message(MY_TG_ID, "🥳 ФИНИШ! Она прошла весь квест!")
        
        final_text = (
            "🏆 **ПОЗДРАВЛЯЮ! Ты прошла квест на 10/10!** 🏆\n\n"
            "Твой подарок ждет тебя у меня. Напиши мне в личку секретный код: "
            "**DEUX MOIS**, и я скажу, где мы сегодня увидимся! 😉✨"
        )
        await callback.message.answer(final_text, parse_mode="Markdown")
    else:
        await callback.answer("Неверная цифра! 😜", show_alert=True)
        await bot.send_message(MY_TG_ID, f"❌ Ошиблась на финальном вопросе, выбрав: {callback.data}")

# === ЗАПУСК ===
async def main():
    print("Бот 'deux mois de bonheur' успешно запущен!")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
