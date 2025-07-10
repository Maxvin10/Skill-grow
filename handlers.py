from aiogram import Bot, types, Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from states import sign
from keyboards.nomer import nomer
router = Router()

@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.set_state(sign.firstname)
    await message.answer("Assalomu alaykum botdan foydalanish uchun ma'lumotlarni to'ldiring!\nIsmingizni kiritng: ")

@router.message(sign.firstname)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(firstname = message.text)
    await message.answer("Familiyangizni kiritng")
    await state.set_state(sign.lastname)

@router.message(sign.lastname)
async def get_lastname(message: Message, state: FSMContext):
    await state.update_data(lastname = message.text)
    await message.answer("Yoshingizni kiriting: ")
    await state.set_state(sign.age)

@router.message(sign.age)
async def get_age(message: Message, state: FSMContext):
    await state.update_data(age = message.text)
    await message.answer("Iltimos, nomeringizni ulashing 👇", reply_markup=nomer)
    await state.set_state(sign.nomer)

@router.message(sign.nomer)
async def get_nomer(message: Message, state: FSMContext):
    phone_num = message.contact.phone_number
    await state.update_data(nomer = phone_num)
    data = await state.get_data()
    await message.answer(f"Ma'lumotlaringiz:\nIsm:{data.get('firstname')},\nFamiliyangiz:{data.get('lastname')},\nYoshingiz:{data.get('age')},\nNomeringiz:{data.get('nomer')}")
    await state.clear()