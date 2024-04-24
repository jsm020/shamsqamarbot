from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart

from loader import dp
from states.allstates import EshikStates
from keyboards.default.materialkeyboeard import material
from keyboards.default.xa_yoki_yuqKeyboard import xayuqkeyboard
from keyboards.default.qosh_oddiy_duty import qosh
from keyboards.default.nalichnikkeyboard import nalichnik,nalichnik2
from data.database import Qosh_narxlari,Dabor_narxlari,Nalichnik_narxlari,patshelnik_price
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,WebAppInfo

# /form komandasi uchun handler yaratamiz. Bu yerda foydalanuvchi hech qanday holatda emas, state=None
@dp.message_handler(CommandStart(),state="*")
async def material_def(message: types.Message):    # print(1)
    await message.answer("Eshik materialini tanlang?",reply_markup=material)
    await EshikStates.material.set()


@dp.message_handler(state=EshikStates.material,content_types=types.ContentTypes.TEXT)
async def answer_material(message: types.Message, state: FSMContext):
    material_eshik = message.text

    await state.update_data(
        {"material": material_eshik}
    )

    await message.answer("Quidagi tartibda eshik razmerini yozing : 0.65x2 0.75x2 \nEshik razmerini yozing:",reply_markup=ReplyKeyboardRemove())

    await EshikStates.next()

@dp.message_handler(state=EshikStates.eshik_razmer,content_types=types.ContentTypes.TEXT)
async def answer_eshik_razmer(message: types.Message, state: FSMContext):
    razmer = message.text
    razmer_list  = razmer.split(" ")
    razmer_kvadrat = 0
    tabaqalar = []
    for x in razmer_list:
        razmer_num = x.split("x")
        kvardat_razmer = float(razmer_num[0])*float(razmer_num[1])
        razmer_kvadrat+=kvardat_razmer
        if 0.6 < float(razmer_num[0]) < 1:
                tabaqalar.append("1 tabaqa")
        elif 1.07 < float(razmer_num[0]) < 1.40:
                tabaqalar.append("1.5 tabaqa")
        elif 1.40 < float(razmer_num[0]) < 1.70:
                tabaqalar.append("2 tabaqa")

        else:
            tabaqalar.append("4 tabaqa")

    await state.update_data(
        {"kvardat_razmer": razmer_kvadrat,
         "Tabaqalar":tabaqalar,
         "razmer_list":razmer_list
         }
    )

    await message.answer("Eshik kvadrati narxini yozing? :")

    await EshikStates.next()


@dp.message_handler(state=EshikStates.eshik_kvadrat_narx,content_types=types.ContentTypes.TEXT)
async def answer_kvadrat_narx(message: types.Message, state: FSMContext):
    eshik_kv_price = float(message.text)
    data = await state.get_data()
    eshik_kv = data.get("kvardat_razmer")
    eshik_kvadrat_price = eshik_kv_price * eshik_kv

    await state.update_data(
        {"eshik_kvadrat_narxi": eshik_kvadrat_price}
    )
    await message.answer("Zamok narxini yozing:")

    await EshikStates.next()


@dp.message_handler(state=EshikStates.zamok_narx,content_types=types.ContentTypes.TEXT)
async def answer_zamok_narx(message: types.Message, state: FSMContext):
    zamok_narx = float(message.text)
    data = await state.get_data()
    razmer_list = data.get("razmer_list")
    zamok_summa = zamok_narx * len(razmer_list)

    await state.update_data(
        {"zamok": zamok_summa}
    )
    await message.answer("Umumiy petle necha pachka?:")

    await EshikStates.next()
    # data = await state.get_data()
    # print(data)
@dp.message_handler(state=EshikStates.petle_soni,content_types=types.ContentTypes.TEXT)
async def answer_petle_soni(message: types.Message, state: FSMContext):
    petle_soni = float(message.text)

    await state.update_data(
        {"petle_soni": petle_soni}
    )
    await message.answer("Petle narxini yozing:")

    await EshikStates.next()

@dp.message_handler(state=EshikStates.petle_narx,content_types=types.ContentTypes.TEXT)
async def answer_petle_summa(message: types.Message, state: FSMContext):
    petle_narx = float(message.text)
    data = await state.get_data()
    petle_soni = data.get("petle_soni")
    petle_summa = petle_narx*petle_soni

    await state.update_data(
        {"petle_summa": petle_summa}
    )
    await message.answer("XA yoki Yuq: Qosh hisoblansinmi?",reply_markup=xayuqkeyboard)

    await EshikStates.next()

@dp.message_handler(state=EshikStates.qosh_bor_yuq,content_types=types.ContentTypes.TEXT)
async def answer_petle_summa(message: types.Message, state: FSMContext):
    xa_yuq = message.text
    if xa_yuq.lower() == "xa":
        await message.answer("Qosh oddiy yoki duty?",reply_markup=qosh)
        await EshikStates.next()
    else:
         await message.answer("Umumiy qo'g'irchoqlar necha par?:",reply_markup=ReplyKeyboardRemove())

         await state.update_data(
              {"qosh_narxi":0}
         )
         await EshikStates.qugirchoq_par.set()
@dp.message_handler(state=EshikStates.qosh_oddiy_duty,content_types=types.ContentTypes.TEXT)
async def answer_petle_summa(message: types.Message, state: FSMContext):
    qosh = message.text
    await state.update_data(
        {"qosh_oddiy_yoki_duty": qosh}
    )

    await message.answer("Qoshlar soni har bir eshik uchun(1 1):",reply_markup=ReplyKeyboardRemove())

    await EshikStates.next()


@dp.message_handler(state=EshikStates.qosh_soni)
async def answer_petle_summa(message: types.Message, state: FSMContext):
    qosh_soni = message.text
    qosh_split = qosh_soni.split(' ')
    data = await state.get_data()
    maretial = data.get("material")
    tabaqalar = data.get("Tabaqalar")
    qosh_oddiy_yoki_duti = data.get("qosh_oddiy_yoki_duty")
    new_material = Qosh_narxlari[maretial]
    qosh_narxi_all = 0
    for x, y in zip(tabaqalar, qosh_split):
        for key, value in new_material.items():
            # print(value)
            if value["tabaqa"] == x and value["qosh_turi"] == qosh_oddiy_yoki_duti:
                qosh_narxi = value["narxi"] * float(y)
                # print(qosh_narxi)
        qosh_narxi_all +=qosh_narxi


    await state.update_data(
        {"qosh_narxi": qosh_narxi_all}
    )
    data = await state.get_data()

    await message.answer("Umumiy qo'g'irchoqlar necha par?:")

    await EshikStates.next()

@dp.message_handler(state=EshikStates.qugirchoq_par)
async def answer_petle_summa(message: types.Message, state: FSMContext):
    qugirchoq = float(message.text)
    kukla_narx = qugirchoq * 40
    await state.update_data(
        {"kukla_narx": kukla_narx}
    )
    await message.answer("Dabor hisoblansinmi?",reply_markup=xayuqkeyboard)

    await EshikStates.next()

@dp.message_handler(state=EshikStates.dabor_bor_yoki_yuq)
async def answer_petle_summa(message: types.Message, state: FSMContext):
    dabor = message.text
    if dabor.lower() == "xa":
        await message.answer("Dabor razmerini kiriting(0.40 0.30 0.20)?:",reply_markup=ReplyKeyboardRemove())
        await EshikStates.next()
    else:
        await state.update_data({"dabor_narx": 0})
        await message.answer("Padshelnik hisoblansinmi? ",reply_markup=xayuqkeyboard)
        await EshikStates.padshelnik_xa_yuq.set()
@dp.message_handler(state=EshikStates.dabor_razmer)
async def answer_petle_summa(message: types.Message, state: FSMContext):
    dabor = message.text
    dabor_narx = 0
    dabor_split = dabor.split(' ')
    data = await state.get_data()
    razmer_list = data.get('razmer_list')
    maretial = data.get('material')
    for x,y in zip(razmer_list,dabor_split):
        razmer_num = x.split("x")


        dabor_m2_1 = float(razmer_num[1])*2
        dabor_m2_2 = dabor_m2_1 + float(razmer_num[0])
        dabor_m2 = dabor_m2_2*float(y)

        dabor_summa = dabor_m2*Dabor_narxlari[maretial]
        dabor_narx +=dabor_summa
    await state.update_data({"dabor_narx": dabor_narx})
    await message.answer("Padshelnik hisoblansinmi? ",reply_markup=xayuqkeyboard)
    await EshikStates.next()



@dp.message_handler(state=EshikStates.padshelnik_xa_yuq)
async def answer_petle_summa(message: types.Message, state: FSMContext):
    padshelnik = message.text
    if padshelnik.lower() == "xa":
        await message.answer("podshelnik necha metr(umumiy)?",reply_markup=ReplyKeyboardRemove())
        await EshikStates.next()
    else:
        await state.update_data({"patshelnik_narx": 0})
        data = await state.get_data()
        maretial = data.get('material')
        if maretial=="Krashni":
            await message.answer("8smlik nalichnik yoki 10smllik yoki 16mmlik?",reply_markup=nalichnik)
        else:
            await message.answer("8smlik nalichnik yoki 10smllik?",reply_markup=nalichnik2)

        await EshikStates.nalichnik_8sm_10_16.set()

@dp.message_handler(state=EshikStates.padshelmik_metr)
async def answer_petle_summa(message: types.Message, state: FSMContext):
    patshelnik = float(message.text)
    data = await state.get_data()
    maretial = data.get('material')
    narxi = patshelnik_price[maretial]*patshelnik
    await state.update_data({"patshelnik_narx": narxi})
    if maretial=="Krashni":
            await message.answer("8smlik nalichnik yoki 10smllik yoki 16mmlik?",reply_markup=nalichnik)
    else:
        await message.answer("8smlik nalichnik yoki 10smllik?",reply_markup=nalichnik2)
    await EshikStates.next()

@dp.message_handler(state=EshikStates.nalichnik_8sm_10_16)
async def answer_petle_summa(message: types.Message, state: FSMContext):
    nalichnik_8_10 = message.text
    await state.update_data({"nalichnik_8_10": nalichnik_8_10})
    await message.answer("nalichnik razmeri necha metr(umumiy)?",reply_markup=ReplyKeyboardRemove())
    await EshikStates.next()

@dp.message_handler(state=EshikStates.nalichnik_razmer)
async def answer_petle_summa(message: types.Message, state: FSMContext):
    nalichnik_8_10 = float(message.text)
    data = await state.get_data()
    maretial = data.get('material')
    nalichnik_8_yoki_10 = data.get("nalichnik_8_10")
    nalichnik_narxi=Nalichnik_narxlari[maretial][nalichnik_8_yoki_10]
    nalichni_summa = nalichnik_narxi * nalichnik_8_10
    await state.update_data({"nalichnik_narx": nalichni_summa})
    await message.answer("Oyna hisoblansinmi?",reply_markup=xayuqkeyboard)
    await EshikStates.next()
    
@dp.message_handler(state=EshikStates.oyna_bor_yuq)
async def answer_petle_summa(message: types.Message, state: FSMContext):
    oyna_bor_yoki_yuq=message.text
    if oyna_bor_yoki_yuq.lower() == "xa":
        await message.answer("Oynani soni(umumiy):",reply_markup=ReplyKeyboardRemove())
        await EshikStates.next()
    else:
        await state.update_data({"oyna_summa": 0})
        await message.answer("Ustanovka hisoblansinmi?", reply_markup=xayuqkeyboard)
        await EshikStates.ustanovka_bor_yuq.set()
@dp.message_handler(state=EshikStates.oyna_soni)
async def answer_petle_summa(message: types.Message, state: FSMContext):     
    oyna_soni = float(message.text)
    oyna_narxi = 150
    oyna_summa = oyna_narxi * oyna_soni
    await state.update_data({"oyna_summa": oyna_summa})
    await message.answer("Ustanovka hisoblansinmi?", reply_markup=xayuqkeyboard)
    await EshikStates.next()

@dp.message_handler(state=EshikStates.ustanovka_bor_yuq)
async def answer_petle_summa(message: types.Message, state: FSMContext):
    ustanovka_bor_yoki_yuq = message.text
    if ustanovka_bor_yoki_yuq.lower() == "xa":
        await message.answer("Ustanovka narxini kiriting?(umumiy):",reply_markup=ReplyKeyboardRemove())
        await EshikStates.next()
    else:
        await state.update_data({"ustanovka_narx": 0})
        await message.answer("Dastavka hisoblansinmi?",reply_markup=xayuqkeyboard)

        await EshikStates.dastavka.set()

@dp.message_handler(state=EshikStates.ustanovka)
async def handle_ustanovka(message: types.Message, state: FSMContext):
    ustanovka_narxi = float(message.text)
    await state.update_data({"ustanovka_narx": ustanovka_narxi})
    await message.answer("Dastavka hisoblansinmi?", reply_markup=xayuqkeyboard)
    await EshikStates.dastavka.set()

@dp.message_handler(state=EshikStates.dastavka)
async def handle_dastavka(message: types.Message, state: FSMContext):
    dastavka_bor_yoki_yuq = message.text
    if dastavka_bor_yoki_yuq.lower() == "xa":
        await message.answer("Dastavka narxini kiriting? (umumiy):", reply_markup=ReplyKeyboardRemove())
        await EshikStates.dastavka_narx.set()
    else:
        await state.update_data({"dastavka_narx": 0})
        dastavka_narxi = float(message.text)
        await state.update_data({"dastavka_narx": dastavka_narxi})
        data = await state.get_data()
        kvardat_razmer = data.get("kvardat_razmer")
        eshik_kvadrat_narxi = data.get("eshik_kvadrat_narxi")
        petle_summa = data.get("petle_summa")
        nalichnik_narx = data.get("nalichnik_narx")
        zamok = data.get("zamok")
        kukla_narx = data.get("kukla_narx")
        qosh_narxi = data.get("qosh_narxi")
        dabor_narx = data.get("dabor_narx")
        patshelnik_narx = data.get("patshelnik_narx")
        oyna_summa = data.get("oyna_summa")
        dastavka_narx = data.get("dastavka_narx")
        ustanovka_narx = data.get("ustanovka_narx")
        tabaqalar = data.get("Tabaqalar")
        maretial = data.get('material')

        
        summa = 0

        summa +=eshik_kvadrat_narxi
        print(summa)
        summa = round(summa)
        summa += zamok+petle_summa+nalichnik_narx+kukla_narx
        print(summa)
        if qosh_narxi:
            summa += qosh_narxi
        if dabor_narx:
            summa += dabor_narx
        if patshelnik_narx:
            summa += patshelnik_narx
        if oyna_summa:
            summa +=oyna_summa
        if dastavka_narx:
            summa +=dastavka_narx
        if ustanovka_narx:
            summa +=ustanovka_narx



        msg = "Quyidai ma`lumotlar qabul qilindi:\n"
        msg += f"Material - {maretial}\n"
        msg += f"Kvadrat razmer - {kvardat_razmer}\n"
        msg += f"Tabaqalar: - {tabaqalar}\n"
        msg += f"Eshik kvadrati narxi:- {eshik_kvadrat_narxi}\n"
        msg += f"Petle_summa - {petle_summa}\n"
        msg += f"Qo'g'irchoq summa - {kukla_narx}\n"
        msg += f"Tabaqalar: - {tabaqalar}\n"
        msg += f"Qosh narxi - {qosh_narxi}\n"
        msg += f"Dabor_narx - {dabor_narx}\n"
        msg += f"Patshelnik_narx: - {patshelnik_narx}\n"
        msg += f"Nalichnik_narx: - {nalichnik_narx}\n"
        msg += f"Oyna_summa - {oyna_summa}\n"
        msg += f"Ustanovka narx - {ustanovka_narx}\n"
        msg += f"Dastavka_narx: - {dastavka_narx}\n"
        msg += f"Jamu summa: - {summa}\n"

        # await message.answer(msg)
        await message.answer(msg, reply_markup=ReplyKeyboardRemove())
        await state.finish()




@dp.message_handler(state=EshikStates.dastavka_narx)
async def handle_dastavka_narx(message: types.Message, state: FSMContext):
    dastavka_narxi = float(message.text)
    await state.update_data({"dastavka_narx": dastavka_narxi})
    data = await state.get_data()
    kvardat_razmer = data.get("kvardat_razmer")
    eshik_kvadrat_narxi = data.get("eshik_kvadrat_narxi")
    petle_summa = data.get("petle_summa")
    nalichnik_narx = data.get("nalichnik_narx")
    zamok = data.get("zamok")
    kukla_narx = data.get("kukla_narx")
    qosh_narxi = data.get("qosh_narxi")
    dabor_narx = data.get("dabor_narx")
    patshelnik_narx = data.get("patshelnik_narx")
    oyna_summa = data.get("oyna_summa")
    dastavka_narx = data.get("dastavka_narx")
    ustanovka_narx = data.get("ustanovka_narx")
    tabaqalar = data.get("Tabaqalar")
    maretial = data.get('material')

    
    summa = 0

    summa +=eshik_kvadrat_narxi
    print(summa)
    summa = round(summa)
    summa += zamok+petle_summa+nalichnik_narx+kukla_narx
    print(summa)
    if qosh_narxi:
        summa += qosh_narxi
    if dabor_narx:
        summa += dabor_narx
    if patshelnik_narx:
        summa += patshelnik_narx
    if oyna_summa:
        summa +=oyna_summa
    if dastavka_narx:
        summa +=dastavka_narx
    if ustanovka_narx:
        summa +=ustanovka_narx



    msg = "Quyidai ma`lumotlar qabul qilindi:\n"
    msg += f"Material - {maretial}\n"
    msg += f"Kvadrat razmer - {kvardat_razmer}\n"
    msg += f"Tabaqalar: - {tabaqalar}\n"
    msg += f"Eshik kvadrati narxi:- {eshik_kvadrat_narxi}\n"
    msg += f"Petle_summa - {petle_summa}\n"
    msg += f"Qo'g'irchoq summa - {kukla_narx}\n"
    msg += f"Tabaqalar: - {tabaqalar}\n"
    msg += f"Qosh narxi - {qosh_narxi}\n"
    msg += f"Dabor_narx - {dabor_narx}\n"
    msg += f"Patshelnik_narx: - {patshelnik_narx}\n"
    msg += f"Nalichnik_narx: - {nalichnik_narx}\n"
    msg += f"Oyna_summa - {oyna_summa}\n"
    msg += f"Ustanovka narx - {ustanovka_narx}\n"
    msg += f"Dastavka_narx: - {dastavka_narx}\n"
    msg += f"Jamu summa: - {summa}\n"

    # await message.answer(msg)
    await message.answer(msg, reply_markup=ReplyKeyboardRemove())
    await state.finish()

