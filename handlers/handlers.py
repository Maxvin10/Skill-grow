from aiogram import Bot, types, Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from states import sign
from keyboards.nomer import nomer
from keyboards.web import web
from keyboards.lang import inline_lang
from keyboards.uzbreply import uzbreply
from keyboards.rusreply import rusreply
from keyboards.engreply import engreply
from aiogram.utils.keyboard import InlineKeyboardBuilder
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
    await message.answer("Ma'lumotlaringiz qabul qilindi✅\nBotdan foydalanish uchun /menu kamandasini bosing!")
    await state.clear()

@router.message(Command("menu"))
async def start_menu(message: Message):
    await message.answer("Maroqli o'rganing😉", reply_markup = web)

@router.message(F.text == "✍️Qo'llanma")
async def use(message: Message):
    await message.answer("""👋 Xush kelibsiz!
Siz o‘z ustida ishlaydigan, ko‘nikmalarini oshirishni istaydigan, va kelajagiga sarmoya qiladigan inson bo‘lsangiz — SkillGrow siz uchun!

🚀 Nimalar qilishingiz mumkin?
🔧 Ko‘nikmalarni rivojlantiring:

Backend asoslari

Frontend boshlang‘ich tushunchalari

Kichik darslar, topshiriqlar, yo‘naltirishlar

Agar o'rganishga qiynalsangiz 🤖 Velmaro AI yordamchingiz sizga yordam beradi 😊

🧠 Savollar bering – Velmaro AI yordam beradi:

Har qanday mavzuda savol

Ingliz tilini o‘rganishda yordam

Shaxsiy reja tuzib berish

Tarjima yoki tushunarsiz matnlar izohi

🤖 Velmaro AI dan ingliz tilida foydalanishingiz mumkin ingliz tilda rivojlanish hamda o'sish sari

🇬🇧 Ingliz tilini o‘rganish uchun foydali
🧠 Siz Velmaro AI yordamida quyidagilarni qilishingiz mumkin:

Matn tarjimasi

So‘z va iboralarni tushuntirish

Inglizcha gap tuzish mashqlari

Speaking va writing odatlarini shakllantirish

✅ Siz so‘ragan mavzuni tushunarli va oddiy izohlab beradi

🤖 Velmaro AI dan /ask buyrug'ini bosib foydalanishingiz mumkin har safar 1 martalik savol bilan 


""")

@router.message(F.text == "Backend")
async def backen(message: Message):
    await message.answer("Kerakli tilni tanlang: ", reply_markup = inline_lang())

@router.callback_query(F.data.startswith("lang_"))
async def tilni_qabul_qil(callback: CallbackQuery):
    code = callback.data.split("_")[1]  # "uz", "ru", "en", "back"

    if code == "uzb":
        await callback.message.answer("Siz o'zbek tilini tanladingiz", reply_markup = uzbreply)
    elif code == "ru":
        await callback.message.answer("Вы выбрали русский язык", reply_markup = rusreply)
    elif code == "eng":
        await callback.message.answer("You chose English", reply_markup = engreply)
    elif code == "back":
        await callback.message.answer("Ortga", reply_markup = web)
    
    await callback.message.edit_reply_markup() 

    await callback.answer()

@router.message(F.text == "🔙 Ortga")
async def ortg(message: Message):
    await message.answer("Ortga", reply_markup = web)
