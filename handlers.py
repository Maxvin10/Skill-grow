from aiogram import Bot, types, Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from states import sign
from keyboards.nomer import nomer
import re
router = Router()
def is_valid_email(email: str) -> bool:
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None
@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.set_state(sign.firstname)
    await message.answer("Assalomu alaykum botdan foydalanish uchun ma'lumotlarni to'ldiring!\nIsmingizni kiriting: ")

@router.message(sign.firstname)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(firstname = message.text)
    await message.answer("Familiyangizni kiriting: ")
    await state.set_state(sign.lastname)

@router.message(sign.lastname)
async def get_lastname(message: Message, state: FSMContext):
    await state.update_data(lastname = message.text)
    await message.answer("Yoshingizni kiriting: ")
    await state.set_state(sign.age)

@router.message(sign.age)
async def get_age(message: Message, state: FSMContext):
    await state.update_data(age = message.text)
    await message.answer("Emailingizni kiriting: ")
    await state.set_state(sign.email)

@router.message(sign.email)
async def get_email(message: Message, state: FSMContext):
   email = message.text
   if not is_valid_email(email):
        await message.answer("❌ Noto'g'ri email format! Iltimos, qayta kiriting. Masalan: example@gmail.com")
        return
   await state.update_data(email=email)
   await message.answer("✅ Email qabul qilindi. Endi parolingizni kiriting:")
   await state.set_state(sign.parol)

@router.message(sign.parol)
async def get_parol(message: Message, state: FSMContext):
    await state.update_data(parol = message.text)
    await message.answer("Iltimos, nomeringizni ulashing 👇", reply_markup=nomer)
    await state.set_state(sign.nomer)

@router.message(sign.nomer)
async def get_nomer(message: Message, state: FSMContext):
    phone_num = message.contact.phone_number
    await state.update_data(nomer = phone_num)
    data = await state.get_data()
    await message.answer(f"Ma'lumotlaringiz:\nIsm:{data.get('firstname')}\nFamiliyangiz:{data.get('lastname')}\nYoshingiz:{data.get('age')}\nEmailingiz: {data.get('email')}\nParolingiz: {data.get('parol')}\nNomeringiz:{data.get('nomer')}")
    await state.clear()