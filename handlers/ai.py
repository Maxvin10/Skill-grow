from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from llama import ask_llama

ai_router = Router()

class AskAIState(StatesGroup):
    waiting_for_prompt = State()

@ai_router.message(Command("ask"))
async def cmd_ask(message: Message, state: FSMContext):
    await message.answer("Savolingizni yozing, Velmaro AI sizga yordam beradi 🧠")
    await state.set_state(AskAIState.waiting_for_prompt)

@ai_router.message(AskAIState.waiting_for_prompt)
async def handle_ai_prompt(message: Message, state: FSMContext):
    prompt = message.text
    await message.answer("""🧠 "Deap searching" yoqildi biroz kuting javob yozilmoqda...""")
    answer = ask_llama(prompt)
    await message.answer(f"{answer}")
    await state.clear()
