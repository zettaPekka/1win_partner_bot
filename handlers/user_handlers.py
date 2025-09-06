from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from asyncio import sleep

from middleware.db_di import DatabaseDI
from database.services.user_service import UserService
from database.services.gambling_service import GamblingService
from states.user_states import UserState
import keyboards.user_kbs as user_kbs
from config import *
from crash_signal.get_signal import get_k_signal

from random import randint


router = Router()
router.message.middleware(DatabaseDI())
router.callback_query.middleware(DatabaseDI())


@router.message(CommandStart())
async def start_handler(message: Message, user_service: UserService, gambling_service: GamblingService):
    photo = FSInputFile('images/main.jpg')
    
    tg_id = message.from_user.id
    await user_service.create_if_not_exists(tg_id)
    user = await user_service.get(tg_id)
    
    if not user.gambling_id:
        await message.answer_photo(photo, caption='<b>Привет! Этот бот выдает сигналы на AviatriX с проходимостью более 99%\n\nЧтобы получить доступ нажми кнопку ниже <blockquote>Если у вас уже есть аккаунт на платформе, то придётся создать новый так как бот выдает доступ только проверенным аккаунтам. Спасибо за понимание  🤝</blockquote></b>',
                                reply_markup=user_kbs.start_kb)
        return
    
    gambling_data = await gambling_service.get_by_tg_id(tg_id)

    if not gambling_data.balance:
        await message.answer_photo(photo, caption='<b>Ваш аккаунт уже привязан, но на нем еще не пополнен баланс. Нажмите кнопку ниже после пополнения</b>',
                                reply_markup=user_kbs.check_dep)
        return

    await message.answer_photo(photo, caption='<b>У тебя есть полный доступ к боту! Можешь пользоваться используя кнопки ниже</b>',
                            reply_markup=user_kbs.get_signal)


@router.callback_query(F.data == 'get_access')
async def get_access(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer('<b>Чтобы бот выдал доступ тебе сначала необходимо зарегистрировать новый аккаунт (даже если есть существующий) по кнопке ниже.\nПосле регистрации напиши свой ID сюда\n\n<blockquote>Регистрация аккаунта должна быть выполнена именно по кнопке ниже, иначе бот не сможет проверить валидность аккаунта </blockquote></b>',
                                    reply_markup=user_kbs.reg_kb)
    await state.set_state(UserState.gambling_id)


@router.callback_query(F.data == 'check_dep')
async def check_dep(callback: CallbackQuery, gambling_service: GamblingService):
    await callback.answer()
    
    gambling_data = await gambling_service.get_by_tg_id(callback.from_user.id)
    deposit_levels = {
        0: '1 уровня, вам доступны прогнозы до 2x',
        1: '2 уровня, вам доступны прогнозы до 4x',
        2: '3 уровня, вам доступны прогнозы до 20x',
    }
    
    if gambling_data.balance > 0:
        await callback.message.answer(f'<b>Вы успешно получили доступ {deposit_levels[min(gambling_data.balance//dep_step, 2)]}\n\nЧтобы получить сигнал нажми кнопку ниже 👇</b>',
                                        reply_markup=user_kbs.get_signal)
        return
    
    await callback.message.answer('<b>Депозит не найден</b>')


@router.message(Command('signal'))
async def get_message_signal(message: Message, gambling_service: GamblingService, user_service: UserService):
    gambling_data = await gambling_service.get_by_tg_id(message.from_user.id)
    user = await user_service.get(message.from_user.id)
    
    if gambling_data and gambling_data.balance > 0:
        
        waiting = await message.answer('<b>⏳ Сигнал генерируется...</b>')
        await sleep(2)
        await waiting.delete()
        
        k = get_k_signal(gambling_data.balance, user.next_k)
        rec_percent = randint(10, 20)
        
        if user.next_k:
            await user_service.reset_next_k(message.from_user.id)
        
        await message.answer(f'<b>Сигнал - {k}X\nРекомендумый процент на ставку - {rec_percent}%</b>',
                                reply_markup=user_kbs.get_signal)
        return
    
    photo = FSInputFile('images/forecast.jpg')
    await message.answer_photo(photo, caption=f'<b>Сигнал - {k}X\nРекомендумый процент на ставку - {rec_percent}%</b>\n<blockquote>Заходить в сделку надо, если до игры осталось не менее 5 секунд, иначе риск повышается</blockquote>',
                                        reply_markup=user_kbs.get_signal)


@router.callback_query(F.data == 'get_signal')
async def get_callback_signal(callback: CallbackQuery, gambling_service: GamblingService, user_service: UserService):
    await callback.answer()
    photo = FSInputFile('images/forecast.jpg')
    
    gambling_data = await gambling_service.get_by_tg_id(callback.from_user.id)
    user = await user_service.get(callback.from_user.id)
    
    waiting = await callback.message.answer('<b>⏳ Сигнал генерируется...</b>')
    await sleep(2)
    await waiting.delete()
    
    k = get_k_signal(gambling_data.balance, user.next_k)
    rec_percent = randint(10, 20)
    
    if user.next_k:
        await user_service.reset_next_k(callback.from_user.id)
    
    await callback.message.answer_photo(photo, caption=f'<b>Сигнал - {k}X\nРекомендумый процент на ставку - {rec_percent}%</b>\n<blockquote>Заходить в сделку надо, если до игры осталось не менее 5 секунд, иначе риск повышается</blockquote>',
                                        reply_markup=user_kbs.get_signal)


@router.message(UserState.gambling_id)
async def link_id(message: Message, user_service: UserService, gambling_service: GamblingService, state: FSMContext):
    if await gambling_service.is_free(message.text):
        await message.answer('<b>Успешно! Теперь ваш аккаунт привязан к роботу. Остался финальный шаг.\nВам необходимо пополнить баланс на любую сумму, и нажать кнопку проверить депозит. После этого вам откроется доступ к функционалу робота\n\nУровни:<blockquote>Депозит до 25$ – сигнал до 2x\nДепозит 25-49$ – сигналы до 4x\nДепозит от 50$ – сигналы до 20x\n</blockquote></b>',
                                reply_markup=user_kbs.check_dep)
        await user_service.link_gambling_user_id(message.from_user.id, message.text)
        await state.clear()
        return

    await message.answer(f'<b>Упс, кажется вы ввели неверный ID, возможно он от вашего старого аккаунта, попробуйте еще раз или напишите в @{username}</b>')


@router.callback_query(F.data == 'profile')
async def prifle(callback: CallbackQuery, gambling_service: GamblingService,):
    await callback.answer()
    photo = FSInputFile('images/profile.jpg')
    
    gambling_data = await gambling_service.get_by_tg_id(callback.from_user.id)
    
    message_text = f'<b>Профиль ID {callback.from_user.id}\n\nПополнено: {gambling_data.balance}$\nУровень: {round(min(gambling_data.balance//dep_step, 2) + 1)}</b>'
    await callback.message.answer_photo(photo, caption=message_text, reply_markup=user_kbs.get_signal)
    
    try:
        await callback.message.delete()
    except:
        pass