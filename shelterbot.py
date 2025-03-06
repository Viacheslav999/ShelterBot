import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import re
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import F


# Настройки
TOKEN = "7221043008:AAEkqiTbPjEsZir9FSBt3EdqDqsoe3Ct6O4"
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)  # ✅ Обязательно добавляем storage


CATEGORY_PHOTO_ID = 'AgACAgIAAxkBAAEWcMFnyHtuMouVWTsR7326X_dod7aDSgAC8uwxGxZvMEp7ELkhlYGidwEAAwIAA3kAAzYE'  
# Меню и корзина
menu = {
    "🍳Завтраки": [
        {'name': 'Омлет со шпинатом и курицей', 'desc':'Яицо куриное, шпинат, курица копченая, черри, сливки, сыр филадельфия, хлеб (300г)', 'price': '400р', 'photo': ''},
        {'name': 'Омлет с колбасками', 'desc':'Яицо куриное, сливки, специи, колбаски охотничьи, морковь бейби, сыр филадельфия, хлеб (250г)', 'price': '350р', 'photo': ''},
        {'name': 'Завтрак бенедикт', 'desc':'Яицо куриное, тостерный сыр, чиабатта, бекон, лист салата, огурец свежий, помидор свежий, перец болгарский, оливковое масло, горчица дижонская, лимонный фреш (450г)', 'price': '500р', 'photo': ''},
        {'name': 'Английский завтрак', 'desc':'Яицо куриное, соевый соус, сливки, чиабатта, охотничьи колбаски, лист салата, помидор свежий, огруец свежий, перец болгасркий, оливковое масло, горчица дижонская, лимонный фреш (450г)', 'price': '550р', 'photo': ''},
        {'name': 'Сэндвич с ветчиной и сыром', 'desc':'Хлеб тостерный, ветчина, сыр янтарь, сыр тостерный, помидор (310г)', 'price': '400р', 'photo': 'AgACAgIAAxkBAANNZ8WnBHpxUMtYZHce6QQ-Nb5KgqgAAoTrMRsWbzBKpYfWgJ1_WVgBAAMCAAN5AAM2BA'},
        {'name': 'Яичница с беконом', 'desc':'Яйцо куриное, бекон, черри, зелень  (270г)', 'price': '350р', 'photo': 'AgACAgIAAxkBAANLZ8WmjQd8mdHDs-HXdJrnI9jqqDUAAoDrMRsWbzBKpA1Tq24DlDEBAAMCAAN5AAM2BA'},
        {'name': 'Сырники', 'desc':'Соус, джем, сметана  (180г)', 'price': '380р', 'photo': 'AgACAgIAAxkBAANJZ8WmTwWGvn_lbk1sgThBV0qlmxMAAnzrMRsWbzBKaUpG5eVmsIIBAAMCAAN5AAM2BA'}
        ],
    "🥗Салаты": [
        {'name': 'Морской бриз', 'desc': 'Мидии, кальмары, креветки, черри, чеснок, грейпфрукт, салат, соус шафран, соус медово-горчинный (340г)', 'price': '650р', 'photo': 'AgACAgIAAxkBAANFZ8Whpco1QzGLcUbpXdN2_syTk8sAAlzrMRsWbzBKMvciAxyH8nEBAAMCAAN4AAM2BA'},
        {'name': 'Прованс', 'desc': 'Грудка куриная, огурец свежий, салат, яйцо перепелиное, чеснок, специи, кефир (410г)', 'price': '700р', 'photo': ''},
        {'name': 'Восточный с бастурмой', 'desc': 'Бастурма говяжья, салат, черри, пьяная вишня, медово-горчичный соус, дорблю, орех грецкий (220г)', 'price': '870р', 'photo': ''},
        {'name': 'Каприз', 'desc': 'Язык говяжий, черри, вешенки, лук, яйца, салат, огурец малосольный, зелень, специи, белый соус (420г)', 'price': '980р', 'photo': 'AgACAgIAAxkBAANHZ8Wiz-jprZxgRh2jYQHp7IUlhBMAAmPrMRsWbzBKS4yKjUSdC1oBAAMCAAN5AAM2BA'},
        {'name': 'Кобб', 'desc': 'Филе куриное, черри, авокадо, салат, огурец свежий, яйцо перепелиное, дорблю, соус медово-горчичный (320г)', 'price': '720р', 'photo': ''},
        {'name': 'Зеленая поляна', 'desc': 'Салат, черри,соус песто, филадельфия, авокадо, оливковое масло (400г)', 'price': '530р', 'photo': ''},
        {'name': 'Кровавая луна', 'desc': 'Микс салата, фета, мандарин, гранатовые зерна, грецкий орех, медово-горчичная заправка (240г)', 'price': '520р', 'photo': ''},
        {'name': 'Оливье с говяжьим языком', 'desc': 'Говяжий язык, яйцо, огурец маринованный, горошек, майонез, лук, картофель (340г)', 'price': '650р', 'photo': ''},
        {'name': 'Нисуаз', 'desc': 'Тунец, салат, картофель, фасоль, яйцо куриное, вяленные томаты, заправка греческая (380г)', 'price': '780р', 'photo': ''},
        {'name': 'Шафран', 'desc': 'Печень куриная, огурец маринованный, кабачки, шампиньоны, помидор, салат, соус шафран, медово-гочичный соус (390г)', 'price': '700р', 'photo': ''},
        {'name': 'Салат с гребешками и креветками', 'desc': 'Гребешки, креветки, авокадо, каперсы, греческая заправка, салат, чеснок (280г)', 'price': '1150р', 'photo': ''},
        {'name': 'Салат с запеченной форелью', 'desc': 'Форель запеченная, черри, салат, бальзамический крем, перец болгарский, специи, греческая заправка (255г)', 'price': '680р', 'photo': ''},
        {'name': 'Нежная печень с апельсином', 'desc': 'Печень куриная, помидор, апельсин, салат , соус манго-чили, соус медово-горчичный  (340г)', 'price': '750р', 'photo': ''},
        {'name': 'Теплый с телятиной', 'desc': 'Вырезка телячья. вешенки, кабачки, лук, помидор, соевый соус, соус унаги, соус терияки, салат (380г)', 'price': '850р', 'photo': ''},
        {'name': 'Салат с уткой и грушей', 'desc': 'утка жареная, груша, вино белое, фасоль, дорблю, вяленные томаты, салат, соус медово-горчичный  (380г)', 'price': '900р', 'photo': ''},
        {'name': 'Греческий', 'desc': 'Салат, помидор, огурец свежий, лук, перец болгарский, заправка греческая, фета, маслины  (380г)', 'price': '460р', 'photo': ''},
        {'name': 'Норвежский', 'desc': 'Форель запеченная, сыр надуги, салат, помидор, греческая заправка   (260г)', 'price': '570р', 'photo': ''},
        {'name': 'Испанский', 'desc': 'Куриная грудка, моцарелла бейби, салат, бальзамический крем, греческая заправка, мандарин  (330г)', 'price': '600р', 'photo': ''},
        {'name': 'Итальянский', 'desc': 'Черри, салат, моцарелла, соус песто, оливковое масло  (290г)', 'price': '580р', 'photo': ''},
        {'name': 'Цезарь с креветками', 'desc': 'Креветка, черри, пармезан, сухари, салат, соус цезарь, яйцо перепелиное  (280г)', 'price': '800р', 'photo': ''},
        {'name': 'Цезарь с курицей', 'desc': 'Куриное филе, черри, бекон, пармезан, сухари, салат, соус цезарь, яйцо перепелиное  (280г)', 'price': '680р', 'photo': ''},
        {'name': 'Цезарь с лососем', 'desc': 'Лосось, с/c черри, пармезан, сухари. салат, соус цезарь, яйцо перепелиное (280г)', 'price': '900р', 'photo': ''},
        {'name': 'Пражский', 'desc': 'Телятина. перец болгарский, шампиньоны, кабачки, соевый соус, сметана, кетчуп, салат (340г)', 'price': '600р', 'photo': ''},
        {'name': 'Каталонский', 'desc': 'Прошутто, дорблю, салат, черри, груша, белое вино, медовоя горчица, орех грецкий   (340г)', 'price': '930р', 'photo': ''},
        {'name': 'Сальмоне', 'desc': 'Черри, киноа, авокадо, лосось, яйцо, сальсо овощная  (310г)', 'price': '760р', 'photo': ''}
        
    ],
    "🍢Закуски": [
        {'name': 'Сало по домашнему', 'desc': 'Сало соленое, сало копченое, чеснок, лук зеленый, горчица (240/50г)', 'price': '520р', 'photo': ''},
        {'name': 'Греночки', 'desc': 'Хлеб черный, соус чесночный (180/40г)', 'price': '220р', 'photo': ''},
        {'name': 'Крылашки Буффало', 'desc': 'Крылышки, соус BBQ, специ,  (350/50г)', 'price': '400р', 'photo': ''},
        {'name': 'Тар тар с лососем', 'desc': 'Лосось с/c, лук, авокадо, соус устричный, черри, филадельфия, лимон, багет (215г)', 'price': '680р', 'photo': ''},
        {'name': 'Тар тар с говядиной', 'desc': 'Вырезка говяжья, помидор, горчица дижонская, лук, корнишоны, пармезан, перец чили, яйца перепелиные, багет (240г)', 'price': '750р', 'photo': ''},
        {'name': 'Паштет куриный', 'desc': 'Паштет из куриной печени, соус черная смородина,багет (200/50г)', 'price': '470р', 'photo': ''},
        {'name': 'Мидии в томатном соусе', 'desc': 'Мидии в ракушке, чеснок, вино белое, соус соевый, соус маринара (400г)', 'price': '650р', 'photo': ''},
        {'name': 'Мидии в сливочном соусе', 'desc': 'Мидии в ракушке, вино белое, чеснок, тимьян, соус соевый, сливки, дорблю, пармезан, лимон   (300г)', 'price': '700р', 'photo': ''},
        {'name': 'Карпачо из говядины', 'desc': 'Вырезка говяжья, черри, руккола. лимон, специи (200г)', 'price': '900р', 'photo': ''},
        {'name': 'Брускетта с бужениной', 'desc': 'Чиабатта, буженина, масло сливочное, зелень, огурец соленый, черри, салат (350г)', 'price': '470р', 'photo': ''},
        {'name': 'Брускетта с лососем', 'desc': 'Лосось с/c, филадельфия, оливки, огурец свежий, багет  (250г)', 'price': '600р', 'photo': ''},
        {'name': 'Рыбная нарезка', 'desc': 'Лосось с/c, салат, лимон (180г)', 'price': '1000р', 'photo': ''},
        {'name': 'Сырное плато', 'desc': 'Дорблю, гаунда, камамбер, пармезан, мед, орех грецкий, виноград (210/40г)', 'price': '900р', 'photo': ''},
        {'name': 'Мясная нарезка', 'desc': 'Буженина, бекон, колбаски охотничьи, грудка копченная, хрен, горчица  (430/60г)', 'price': '1000р', 'photo': ''},
        {'name': 'Овощная нарезка', 'desc': 'Помидор, огурец свежий, зелень, перец болгарский, лук крымский, салат (330г)', 'price': '430р', 'photo': ''},
        {'name': 'Селедочка под водочку', 'desc': 'Селедка, картофель, хлеб темный, лук (450г)', 'price': '520р', 'photo': ''},
        {'name': 'Сырные палочки', 'desc': 'Сырные палочки, соус на выбор: чесночный/сливочный/брусничный (200/50г)', 'price': '400р', 'photo': ''},
        {'name': 'Креветка в темпура', 'desc': 'Креветки, васаби, чеснок, соус соевый, лимон, соус терияки, соус свит чили (300/90г)', 'price': '780р', 'photo': ''},
        {'name': 'Креветка в кисло-сладком соусе', 'desc': 'Креветки, тимьян, чеснок, соус соевый, соус терияки, соус манго-чили, соус свит-чили, лимон (270г)', 'price': '850р', 'photo': ''},
        {'name': 'Азовская тюлька', 'desc': 'Тюлька, специи, лимон (200/30г)', 'price': '320р', 'photo': ''},
        {'name': 'Вяленные деликатесы', 'desc': 'Шея сыровяленая, бастурма говяжья, свиная вырезка сыовяленая (150г)', 'price': '680р', 'photo': ''},
        {'name': 'Пивная тарелка', 'desc': 'Крылышки, сырные палочки, луковые кольца, соус BBQ, гренки (470/50г)', 'price': '720р', 'photo': ''}
    ],
    "🍚Гарнир": [
        {'name': 'Овощи запеченные', 'desc': 'Кабачок, баклажан, перец болгарский, помидор, лук, чеснок, перец чили, специи, зелень (350г)', 'price': '430р', 'photo': ''},
        {'name': 'Картофель по-сельски', 'desc': 'Картофель, чеснок, зелень (250г)', 'price': '220р', 'photo': ''},
        {'name': 'Картофель фри', 'desc': 'Картофель фри, соус (200/50г)', 'price': '300р', 'photo': ''},
        {'name': 'Картофель отварной', 'desc': 'Картофель, зелень (150г)', 'price': '200р', 'photo': ''},
        {'name': 'Картофельное пюре', 'desc': 'Картофель, молоко (150г)', 'price': '200р', 'photo': ''},
        {'name': 'Плов с овощами', 'desc': 'Рис, лук, морковь, мексиканская смесь, фасоль, специи (250г)', 'price': '300р', 'photo': ''},
        {'name': 'Плов из говядины', 'desc': 'Телятина, рис, лук, морковь, чеснок, специи (300г)', 'price': '400р', 'photo': ''},
        {'name': 'Тяхан', 'desc': 'Рис, куриное филе, морковь, чеснок, соус соевый, лук, перец болгарский (300г)', 'price': '320р', 'photo': ''}
    ],
    "🍝Пасты": [
        {'name': 'Паста с чернилами каракатицы', 'desc': 'Паста с чернилами каракатицы, черри, чеснок, соус рыбный, морской коктейл, сливки, специи (300г)', 'price': '700р', 'photo': ''},
        {'name': 'Фетучини', 'desc': 'Паста, курица, шампиньоны, помидор, соус соевый, пармезан, сливки, специи (350г)', 'price': '580р', 'photo': ''},
        {'name': 'Паста болоньезе', 'desc': 'Паста, телятина, вино белое, соус томатный, чеснок, соус соевый, пармезан, специи  (300г)', 'price': '680р', 'photo': ''},
        {'name': 'Карбонара', 'desc': 'Патса, бекон, сливки, пармезан, желток, соус соевый (330г)', 'price': '600р', 'photo': ''},
        {'name': 'Удон с курицей и овощами', 'desc': 'Удон, курица, перец болгарский, лук, фасоль, чеснок, унаги, соус соевый, кунжут (280г)', 'price': '500р', 'photo': ''},
        {'name': 'Лазанья', 'desc': 'Паста листовая, свинина, телятина, помидоры, лук, чеснок, соус бешамель, томатный соус (400г)', 'price': '520р', 'photo': ''}
    ],
    "🔥Мангал": [
        {'name': 'Перепелка', 'desc': 'Салат, черри, укроп, красный острый перец (300г)', 'price': '650р', 'photo': ''},
        {'name': 'Каре ягненка', 'desc': 'Лаваш, черри, салат, аджика (200г)', 'price': '900р', 'photo': ''},
        {'name': 'Форель', 'desc': 'Соус дзадзики (300г)', 'price': '900р', 'photo': ''},
        {'name': 'Лосось', 'desc': 'Соус дзадзики(300г)', 'price': '900р', 'photo': ''},
        {'name': 'Сибас', 'desc': 'Соус дзадзики (300г)', 'price': '900р', 'photo': ''},
        {'name': 'Скумбрия', 'desc': 'Соус дзадзики (300г)', 'price': '850р', 'photo': ''},
        {'name': 'Дорадо', 'desc': 'Салат, лимон, красный острый перец, соус дзадзики (300г)', 'price': '1100р', 'photo': ''},
        {'name': 'Шашлык из свинины', 'desc': 'Лаваш, лук маринованный, аджика, черри, салат, соус красный (200г)', 'price': '550р', 'photo': ''},
        {'name': 'Шашлыки из баранины', 'desc': 'Шашлык баранина, лаваш, лук маринованный, аджика, черри, салат, соус красный (200г)', 'price': '850р', 'photo': ''},
        {'name': 'Шашлык из свиного антрекота', 'desc': 'Лаваш, аджика, лук маринованный, салат, черри (250г)', 'price': '600р', 'photo': ''},
        {'name': 'Овощи гриль', 'desc': 'Кабачки, баклажан, перец, помидор, кукуруза, шампиньоны (350г)', 'price': '500р', 'photo': ''},
        {'name': 'Шашлык из курциы', 'desc': 'Шашлык курица, лаваш, лук маринвоанный, салат, черри, соус белый (200г)', 'price': '450р', 'photo': ''},
        {'name': 'Колбаски свиные', 'desc': 'Лаваш, лук маринованный, соус красный, 3шт', 'price': '900р', 'photo': ''},
        {'name': 'Колбаски куриные', 'desc': 'Лаваш, лук маринованный, соус белый 3шт', 'price': '900р', 'photo': ''},
        {'name': 'Люля из курицы', 'desc': 'Лаваш, соус дзадзики, лук маринованный, салат, черри (200г)', 'price': '450р', 'photo': ''},
        {'name': 'Люля из баранины', 'desc': 'Лаваш, аджика, лук маринованный, салат, черри  (200г)', 'price': '850р', 'photo': ''},
        {'name': 'Люля из говядины', 'desc': 'Лаваш, аджика, лук маринованный, салат, черри (200г)', 'price': '650р', 'photo': ''}
    ],
    "🍕Пицца 30см": [
        {'name': 'Техас', 'desc': 'Бекон, пепперони, моцарелла, перец, халапенью, соус манго-чили, соус маринара, помидор (580г)', 'price': '650р', 'photo': ''},
        {'name': 'Барбекю', 'desc': 'Колбаски охотничьи, пармезан, моцарелла, лук маринованный, черри, соус чесночный, соус BBQ (760г)', 'price': '600р', 'photo': ''},
        {'name': 'Итальяно', 'desc': 'Хамон, моцарелла, дорблю, помидорЮ, руккола, сливки (675г)', 'price': '950р', 'photo': ''},
        {'name': 'Гавайская', 'desc': 'Грудка куриная копченая, моцарелла, кукуруза, ананс, сливки (670г)', 'price': '750р', 'photo': ''},
        {'name': 'Карбонара', 'desc': 'Бекон, моцарелла, руккола, яйцо перепелиное, помидор, шампиньоны, сливки   (710г)', 'price': '800р', 'photo': ''},
        {'name': 'Баварская', 'desc': 'Колбаски охотничьи, шампиньоны, соус маринара, моцарелла, огурцы маринованные (670г)', 'price': '680р', 'photo': ''},
        {'name': 'Соблазн', 'desc': 'Креветка, бекон, ветчина, сливки, моцарелла, соус шрирача, помидор, огурец соленый (600г)', 'price': '750р', 'photo': ''},
        {'name': 'Пепперони', 'desc': 'Пепперони, моцарелла, соус маринара (520г)', 'price': '780р', 'photo': ''},
        {'name': 'Филадельфия', 'desc': 'Лаваш, аджика, лук маринованный, салат, черри  (200г)', 'price': '850р', 'photo': ''},
        {'name': 'Груша Дорблю', 'desc': 'Лаваш, аджика, лук маринованный, салат, черри  (200г)', 'price': '850р', 'photo': ''},
        {'name': 'Лосось Терияки', 'desc': 'Лаваш, аджика, лук маринованный, салат, черри  (200г)', 'price': '850р', 'photo': ''},
        {'name': 'Капричеза', 'desc': 'Лаваш, аджика, лук маринованный, салат, черри  (200г)', 'price': '850р', 'photo': ''},
        {'name': 'Том-ям', 'desc': 'Лаваш, аджика, лук маринованный, салат, черри  (200г)', 'price': '850р', 'photo': ''},
        {'name': 'Маргарита', 'desc': 'Лаваш, аджика, лук маринованный, салат, черри  (200г)', 'price': '850р', 'photo': ''},
        {'name': 'Диабло', 'desc': 'Лаваш, аджика, лук маринованный, салат, черри  (200г)', 'price': '850р', 'photo': ''},
        {'name': 'Пицца с лососем и креветками', 'desc': 'Лаваш, аджика, лук маринованный, салат, черри  (200г)', 'price': '850р', 'photo': ''},
        {'name': 'Пицца Цезарь', 'desc': 'Лаваш, аджика, лук маринованный, салат, черри  (200г)', 'price': '850р', 'photo': ''},
        {'name': '4 сыра', 'desc': 'Лаваш, аджика, лук маринованный, салат, черри  (200г)', 'price': '850р', 'photo': ''},
        {'name': 'Хачапури по-аджарски', 'desc': 'Лаваш, аджика, лук маринованный, салат, черри  (200г)', 'price': '850р', 'photo': ''},
        {'name': 'Мясная', 'desc': 'Лаваш, аджика, лук маринованный, салат, черри  (200г)', 'price': '850р', 'photo': ''},
        {'name': 'Американо', 'desc': 'Лаваш, аджика, лук маринованный, салат, черри  (200г)', 'price': '850р', 'photo': ''},
    ],
    "🍕Пицца 45см": [],
    "🍣Суши": [],
    "🍣Роллы": [],
    "🍖Горячие блюда": [],
    "🍜Первые блюда": [],
    "🍰Десерты": []
}

cart = {}
user_data = {}

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Наше меню")],
        [KeyboardButton(text="Ваши заказы")]  # Кнопка для просмотра корзины
    ],
    resize_keyboard=True
)

# Кнопка для просмотра корзины в меню категорий
view_cart_button = InlineKeyboardButton(text="Ваши заказы", callback_data="view_cart")
keyboard = InlineKeyboardMarkup(inline_keyboard=[[view_cart_button]])

# Обработчик команды /start
@dp.message(lambda message: message.text == "/start")
async def start(message: types.Message):
    user_id = message.from_user.id
    cart[user_id] = []  # Инициализация пустой корзины для пользователя
    
    # Приветственное сообщение
    welcome_message = (
        "Добро пожаловать в ресторан Shelter! 🍽️\n\n"
        "Мы рады приветствовать вас в нашем уютном уголке, где вкусная еда и отличный сервис встречаются с комфортом и гостеприимством. 😌✨\n\n"
        "Здесь вас ждут не только изысканные блюда, но и персональный подход к каждому клиенту. Мы готовы угодить даже самым взыскательным гурманам!\n\n"
        "Как можем помочь вам сегодня? Вы можете:\n\n"
        "🍴 Ознакомиться с меню\n"
        "🚚 Заказать доставку\n"
        "📞 Получить помощь от нашего менеджера\n\n"
        "Напишите, если у вас есть вопросы или если вы хотите сделать заказ. Мы с радостью обслужим вас! 🌟"
    )
    
    # Отправка приветственного сообщения с клавиатурой
    await bot.send_message(message.chat.id, welcome_message, reply_markup=main_kb)
# Обработчик нажатия кнопки "Наше меню"
@dp.message(lambda message: message.text == "Наше меню")
async def show_categories(message: types.Message):
    if not CATEGORY_PHOTO_ID:
        await bot.send_message(message.chat.id, "Ошибка: Фото категорий не задано!")
        return
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=category, callback_data=f"cat_{category}")] for category in menu.keys()
    ])
    await bot.send_photo(message.chat.id, CATEGORY_PHOTO_ID, caption="😎 Пожалуйста, выберите категорию блюд:", reply_markup=kb)

# Обработчик нажатия на категорию меню
@dp.callback_query(lambda c: c.data.startswith('cat_'))
async def show_items(callback_query: types.CallbackQuery):
    category = callback_query.data.split('_')[1]
    
    if not menu.get(category):  
        await callback_query.answer("В этой категории пока нет блюд.")
        return

    for item in menu[category]:
        if not item.get('photo'):
            await bot.send_message(callback_query.message.chat.id, f"Ошибка: Фото для {item['name']} отсутствует!")
            continue
        
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Добавить в корзину", callback_data=f"add_{item['name']}")]
        ])
        await bot.send_photo(callback_query.message.chat.id, item['photo'],
                             caption=f"🍽 {item['name']}\n📌 {item['desc']}\n💰 Цена: {item['price']} руб.",
                             reply_markup=kb)

# Обработчик нажатия на кнопку добавления в корзину
@dp.callback_query(lambda c: c.data.startswith('add_'))
async def add_to_cart(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    item_name = callback_query.data.split('_')[1]
    
    # Ищем товар в меню
    for category in menu.values():
        for item in category:
            if item['name'] == item_name:
                # Добавляем товар в корзину
                cart.setdefault(user_id, []).append(item)
                
                # Отправляем уведомление пользователю
                await callback_query.answer(f"{item_name} добавлено в корзину! ✅")
                return

# Обработчик для кнопки "Ваши заказы"
@dp.message(lambda message: message.text == "Ваши заказы")
async def view_cart(message: types.Message):
    user_id = message.from_user.id
    if user_id not in cart or not cart[user_id]:
        await message.answer("Ваша корзина пуста. Добавьте товары в корзину!")
        return

    # Составляем список товаров из корзины
    cart_items = cart[user_id]
    cart_summary = ""
    total_price = 0

    for item in cart_items:
        # Используем регулярное выражение для извлечения числовой части цены
        price_str = item['price']
        price_match = re.search(r'\d+', price_str)  # Ищем числовую часть
        if price_match:
            item_price = float(price_match.group())  # Преобразуем в число
        else:
            item_price = 0  # Если не нашли цену, считаем как 0
        
        cart_summary += f"• {item['name']} - {item_price}₽\n"
        total_price += item_price  # Складываем цену с общей суммой

    cart_summary += f"\n**Общая сумма**: {total_price}₽"

    # Отправляем пользователю сообщение с содержимым корзины
    await message.answer(f"Ваша корзина:\n\n{cart_summary}")

    # Переходим к запросу ФИО и телефона
    await message.answer("Пожалуйста, введите ваше ФИО и телефон через пробел (например: Иванов Иван 123-456-7890):")

# ID сотрудника, которому будет отправляться уведомление о новом заказе
employee_id = '5301735162'
# Создаем клавиатуру для выбора способа доставки
def delivery_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[  # Указываем список кнопок
        [InlineKeyboardButton(text="Самовывоз", callback_data="delivery_pickup")],
        [InlineKeyboardButton(text="Доставка", callback_data="delivery_home")]
    ])
    return kb

# Создаем клавиатуру для выбора времени или связи с сотрудником
def time_or_contact_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[  # Указываем список кнопок
        [InlineKeyboardButton(text="Ближайшее время", callback_data="nearest_time")],
        [InlineKeyboardButton(text="Связаться с сотрудником", callback_data="contact_employee")]
    ])
    return kb

# Создаем клавиатуру для подтверждения заказа
def confirm_order_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[  # Указываем список кнопок
        [InlineKeyboardButton(text="Подтвердить заказ", callback_data="confirm_order")],
        [InlineKeyboardButton(text="Связаться с сотрудником", callback_data="contact_employee")]
    ])
    return kb

# Обработчик получения ФИО и номера телефона
@dp.message(lambda message: True)  # Принимаем любой текст
async def get_fio_and_phone(message: types.Message):
    user_id = message.from_user.id

    # Проверяем, если данные уже сохранены
    if user_id in user_data and "fio" in user_data[user_id] and "phone" in user_data[user_id]:
        return  # Если данные уже есть, пропускаем дальнейшие действия

    input_data = message.text.split()

    # Проверяем, что введены минимум два значения (ФИО и номер телефона)
    if len(input_data) < 2:
        await message.answer("Пожалуйста, введите ваше ФИО и телефон в формате: ФИО Номер телефона.")
        return

    # Все элементы кроме последнего считаем ФИО
    fio = ' '.join(input_data[:-1])
    phone = input_data[-1]  # Последний элемент — это номер телефона

    # Преобразуем ФИО в заглавные буквы, чтобы было унифицировано
    fio = fio.strip().title()  # Преобразуем ФИО, чтобы каждое слово начиналось с заглавной буквы

    # Проверяем номер телефона
    # Убираем все символы кроме цифр и символа "+"
    phone_clean = re.sub(r'[^0-9+]', '', phone)

    # Проверка на валидный номер телефона (с 10 до 15 цифр, может быть с + или без)
    if not re.match(r'^\+?\d{10,15}$', phone_clean):
        await message.answer("Некорректный номер телефона. Пожалуйста, введите номер телефона в правильном формате.")
        return

    # Если номер с +, удаляем его для унификации
    if phone_clean.startswith('+'):
        phone_clean = phone_clean[1:]

    # Сохраняем ФИО и телефон пользователя
    user_data[user_id] = {"fio": fio, "phone": phone_clean}

    # Запрашиваем способ доставки
    await message.answer("Выберите способ доставки:", reply_markup=delivery_kb())

# Обработчик выбора способа доставки
@dp.callback_query(lambda c: c.data.startswith("delivery_"))
async def choose_delivery(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    delivery_method = callback_query.data.split('_')[1]

    # Сохраняем способ доставки
    user_data[user_id]["delivery_method"] = delivery_method

    if delivery_method == "home":
        await bot.send_message(callback_query.message.chat.id, "🏠 Выберите предпочтение: Ближайшее время или Связаться с сотрудником.",
                               reply_markup=time_or_contact_kb())
    else:
        await bot.send_message(callback_query.message.chat.id, "✅ Спасибо за заказ! Мы готовы к отправке.")

# Обработка кнопки "Подтвердить заказ"
@dp.callback_query(lambda c: c.data == "confirm_order")
async def confirm_order(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    
    # Проверяем, что все данные введены
    if user_id not in user_data or "fio" not in user_data[user_id] or "phone" not in user_data[user_id]:
        await callback_query.answer("Пожалуйста, введите ваши данные (ФИО и телефон).")
        return
    
    # Получаем данные заказа
    fio = user_data[user_id]["fio"]
    phone = user_data[user_id]["phone"]
    delivery_method = user_data[user_id]["delivery_method"]

    # Создаем сообщение с деталями заказа
    order_details = f"**Заказ от:** {fio}\n**Телефон:** {phone}\n**Способ доставки:** {delivery_method}"

    # Отправляем подтверждение пользователю
    await callback_query.message.answer(f"✅ Ваш заказ подтвержден! Спасибо за заказ!\n\n{order_details}")

    # Отправляем уведомление сотруднику о новом заказе
    await bot.send_message(employee_id, f"🚨 Новый заказ!\n\n{order_details}")

    # Очищаем данные пользователя
    user_data[user_id] = {}

# Обработка кнопки "Ближайшее время"
@dp.callback_query(lambda c: c.data == "nearest_time")
async def nearest_time(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    await callback_query.message.answer("✅ Ваш заказ будет обработан в ближайшее время. Мы свяжемся с вами для уточнения деталей.")

    # Подтверждаем заказ
    await callback_query.message.answer("✅ Ваш заказ подтвержден! Спасибо за заказ!")
    
    # Очищаем данные пользователя
    user_data[user_id] = {}

# Обработка кнопки "Связаться с сотрудником"
@dp.callback_query(lambda c: c.data == "contact_employee")
async def contact_employee(callback_query: types.CallbackQuery):
    await callback_query.message.answer("📞 Мы свяжемся с вами для уточнения деталей.")

# 📌 Логирование ошибок
@dp.errors()
async def error_handler(update: types.Update, exception: Exception):
    logging.error(f"Ошибка: {exception}")
    return True

# 📌 Запуск бота
async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())