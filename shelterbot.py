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
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command


# Настройки
TOKEN = "7221043008:AAEkqiTbPjEsZir9FSBt3EdqDqsoe3Ct6O4"
CHANNEL_ID = '-1002160470436'
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)  # ✅ Обязательно добавляем storage


CATEGORY_PHOTO_ID = 'AgACAgIAAxkBAAEWcMFnyHtuMouVWTsR7326X_dod7aDSgAC8uwxGxZvMEp7ELkhlYGidwEAAwIAA3kAAzYE'  
# Меню и корзина
menu = {
    "🍳Завтраки": [
        {'name': 'Омлет со шпинатом и курицей', 'desc':'Яицо куриное, шпинат, курица копченая, черри, сливки, сыр филадельфия, хлеб (300г)', 'price': '400р', 'photo': 'AgACAgIAAxkBAAIILGfROVDuaTAeo-LTKYd9Bp1_80pqAALwKDIbYVSJSiz92BddRKLcAQADAgADeAADNgQ'},
        {'name': 'Омлет с колбасками', 'desc':'Яицо куриное, сливки, специи, колбаски охотничьи, морковь бейби, сыр филадельфия, хлеб (250г)', 'price': '350р', 'photo': 'AgACAgIAAxkBAAIILGfROVDuaTAeo-LTKYd9Bp1_80pqAALwKDIbYVSJSiz92BddRKLcAQADAgADeAADNgQ'},
        {'name': 'Завтрак бенедикт', 'desc':'Яицо куриное, тостерный сыр, чиабатта, бекон, лист салата, огурец свежий, помидор свежий, перец болгарский, оливковое масло, горчица дижонская, лимонный фреш (450г)', 'price': '500р', 'photo': 'AgACAgIAAxkBAAIGKWfQgZiKzqZB2cwvIKaOdrsW33N4AAKI6jEb6KqJSkTBio7B5cc4AQADAgADeQADNgQ'},
        {'name': 'Английский завтрак', 'desc':'Яицо куриное, соевый соус, сливки, чиабатта, охотничьи колбаски, лист салата, помидор свежий, огруец свежий, перец болгасркий, оливковое масло, горчица дижонская, лимонный фреш (450г)', 'price': '550р', 'photo': 'AgACAgIAAxkBAAIGimfQipuJXhoDkmkAATaZSTTGieMp0AACjeoxG-iqiUqmO3f3CfDGYwEAAwIAA3kAAzYE'},
        {'name': 'Сэндвич с ветчиной и сыром', 'desc':'Хлеб тостерный, ветчина, сыр янтарь, сыр тостерный, помидор (310г)', 'price': '400р', 'photo': 'AgACAgIAAxkBAANNZ8WnBHpxUMtYZHce6QQ-Nb5KgqgAAoTrMRsWbzBKpYfWgJ1_WVgBAAMCAAN5AAM2BA'},
        {'name': 'Яичница с беконом', 'desc':'Яйцо куриное, бекон, черри, зелень  (270г)', 'price': '350р', 'photo': 'AgACAgIAAxkBAANLZ8WmjQd8mdHDs-HXdJrnI9jqqDUAAoDrMRsWbzBKpA1Tq24DlDEBAAMCAAN5AAM2BA'},
        {'name': 'Сырники', 'desc':'Соус, джем, сметана  (180г)', 'price': '380р', 'photo': 'AgACAgIAAxkBAANJZ8WmTwWGvn_lbk1sgThBV0qlmxMAAnzrMRsWbzBKaUpG5eVmsIIBAAMCAAN5AAM2BA'}
        ],
    "🥗Салаты": [
        {'name': 'Морской бриз', 'desc': 'Мидии, кальмары, креветки, черри, чеснок, грейпфрукт, салат, соус шафран, соус медово-горчинный (340г)', 'price': '650р', 'photo': 'AgACAgIAAxkBAANFZ8Whpco1QzGLcUbpXdN2_syTk8sAAlzrMRsWbzBKMvciAxyH8nEBAAMCAAN4AAM2BA'},
        {'name': 'Прованс', 'desc': 'Грудка куриная, огурец свежий, салат, яйцо перепелиное, чеснок, специи, кефир (410г)', 'price': '700р', 'photo': 'AgACAgIAAxkBAAIILGfROVDuaTAeo-LTKYd9Bp1_80pqAALwKDIbYVSJSiz92BddRKLcAQADAgADeAADNgQ'},
        {'name': 'Восточный с бастурмой', 'desc': 'Бастурма говяжья, салат, черри, пьяная вишня, медово-горчичный соус, дорблю, орех грецкий (220г)', 'price': '870р', 'photo': 'AgACAgIAAxkBAAIGWGfQhprBwtuPuBn_3GJzAfxDaPukAALS6jEb6KqJSkdiQl4oFSl5AQADAgADeAADNgQ'},
        {'name': 'Каприз', 'desc': 'Язык говяжий, черри, вешенки, лук, яйца, салат, огурец малосольный, зелень, специи, белый соус (420г)', 'price': '980р', 'photo': 'AgACAgIAAxkBAANHZ8Wiz-jprZxgRh2jYQHp7IUlhBMAAmPrMRsWbzBKS4yKjUSdC1oBAAMCAAN5AAM2BA'},
        {'name': 'Кобб', 'desc': 'Филе куриное, черри, авокадо, салат, огурец свежий, яйцо перепелиное, дорблю, соус медово-горчичный (320г)', 'price': '720р', 'photo': 'AgACAgIAAxkBAAIGMmfQgmvycPyNHGW0pe_YISVHWh6ZAAKZ6jEb6KqJStAN6LePjeKgAQADAgADeQADNgQ'},
        {'name': 'Зеленая поляна', 'desc': 'Салат, черри,соус песто, филадельфия, авокадо, оливковое масло (400г)', 'price': '530р', 'photo': 'AgACAgIAAxkBAAIGdmfQiSW09Bd9bPw30B6k2lf0m6frAAIV6zEb6KqJSls5FHvlSwABXwEAAwIAA3kAAzYE'},
        {'name': 'Кровавая луна', 'desc': 'Микс салата, фета, мандарин, гранатовые зерна, грецкий орех, медово-горчичная заправка (240г)', 'price': '520р', 'photo': 'AgACAgIAAxkBAAIILGfROVDuaTAeo-LTKYd9Bp1_80pqAALwKDIbYVSJSiz92BddRKLcAQADAgADeAADNgQ'},
        {'name': 'Оливье с говяжьим языком', 'desc': 'Говяжий язык, яйцо, огурец маринованный, горошек, майонез, лук, картофель (340г)', 'price': '650р', 'photo': 'AgACAgIAAxkBAAIILGfROVDuaTAeo-LTKYd9Bp1_80pqAALwKDIbYVSJSiz92BddRKLcAQADAgADeAADNgQ'},
        {'name': 'Нисуаз', 'desc': 'Тунец, салат, картофель, фасоль, яйцо куриное, вяленные томаты, заправка греческая (380г)', 'price': '780р', 'photo': 'AgACAgIAAxkBAAIGXGfQhwd6osHiRvoyXSAzTT-Rzcf3AALa6jEb6KqJSl3HmTk-A8pfAQADAgADeQADNgQ'},
        {'name': 'Шафран', 'desc': 'Печень куриная, огурец маринованный, кабачки, шампиньоны, помидор, салат, соус шафран, медово-гочичный соус (390г)', 'price': '700р', 'photo': 'AgACAgIAAxkBAAIGXmfQhzGBGTs4a_JDaSCldn80xRmAAALc6jEb6KqJShvGNuPiJnGKAQADAgADeQADNgQ'},
        {'name': 'Салат с гребешками и креветками', 'desc': 'Гребешки, креветки, авокадо, каперсы, греческая заправка, салат, чеснок (280г)', 'price': '1150р', 'photo': 'AgACAgIAAxkBAAIGBWfQfbknoRFWf1xgGT-XDuwdtAa9AAKzBzIb6KqBSj_qv-KRZpbfAQADAgADeQADNgQ'},
        {'name': 'Салат с запеченной форелью', 'desc': 'Форель запеченная, черри, салат, бальзамический крем, перец болгарский, специи, греческая заправка (255г)', 'price': '680р', 'photo': 'AgACAgIAAxkBAAIGMGfQgkXT_Nhg8S6PW6L28xXl6HuOAAKS6jEb6KqJSiCG9WzvmgawAQADAgADeQADNgQ'},
        {'name': 'Нежная печень с апельсином', 'desc': 'Печень куриная, помидор, апельсин, салат , соус манго-чили, соус медово-горчичный  (340г)', 'price': '750р', 'photo': 'AgACAgIAAxkBAAIILGfROVDuaTAeo-LTKYd9Bp1_80pqAALwKDIbYVSJSiz92BddRKLcAQADAgADeAADNgQ'},
        {'name': 'Теплый с телятиной', 'desc': 'Вырезка телячья. вешенки, кабачки, лук, помидор, соевый соус, соус унаги, соус терияки, салат (380г)', 'price': '850р', 'photo': 'AgACAgIAAxkBAAIF8WfQe9Kmr_jHJnj7Hwiu8jPNRIuxAAKKBzIb6KqBSoE2x1glu5gGAQADAgADeQADNgQ'},
        {'name': 'Салат с уткой и грушей', 'desc': 'утка жареная, груша, вино белое, фасоль, дорблю, вяленные томаты, салат, соус медово-горчичный  (380г)', 'price': '900р', 'photo': 'AgACAgIAAxkBAAIG02fQjlHwPw8lW6Sx3llpWgfZETEFAAKj6jEb6KqJSl6FILWCk5f3AQADAgADeQADNgQ'},
        {'name': 'Греческий', 'desc': 'Салат, помидор, огурец свежий, лук, перец болгарский, заправка греческая, фета, маслины  (380г)', 'price': '460р', 'photo': 'AgACAgIAAxkBAAIGB2fQfdmsL2Aw0N0l6G0zxHzmObdaAAK6BzIb6KqBShNBbR3Xlo7zAQADAgADeAADNgQ'},
        {'name': 'Норвежский', 'desc': 'Форель запеченная, сыр надуги, салат, помидор, греческая заправка   (260г)', 'price': '570р', 'photo': 'AgACAgIAAxkBAAIILGfROVDuaTAeo-LTKYd9Bp1_80pqAALwKDIbYVSJSiz92BddRKLcAQADAgADeAADNgQ'},
        {'name': 'Испанский', 'desc': 'Куриная грудка, моцарелла бейби, салат, бальзамический крем, греческая заправка, мандарин  (330г)', 'price': '600р', 'photo': 'AgACAgIAAxkBAAIGDWfQfk-82D7QVihCNklUbwzi3oC2AALBBzIb6KqBShE8qG-NWwuAAQADAgADeQADNgQ'},
        {'name': 'Итальянский', 'desc': 'Черри, салат, моцарелла, соус песто, оливковое масло  (290г)', 'price': '580р', 'photo': 'AgACAgIAAxkBAAIGD2fQfpgDK73tJMkFS2-34UsfF0AhAALCBzIb6KqBSpBynVIDuJPWAQADAgADeQADNgQ'},
        {'name': 'Цезарь с креветками', 'desc': 'Креветка, черри, пармезан, сухари, салат, соус цезарь, яйцо перепелиное  (280г)', 'price': '800р', 'photo': 'AgACAgIAAxkBAAIGYGfQh2QoTyPEinqNKZA0JnxU6KZ6AALg6jEb6KqJSgPZuwf0D9jKAQADAgADeQADNgQ'},
        {'name': 'Цезарь с курицей', 'desc': 'Куриное филе, черри, бекон, пармезан, сухари, салат, соус цезарь, яйцо перепелиное  (280г)', 'price': '680р', 'photo': 'AgACAgIAAxkBAAIF5WfQesxLYIROKl94c91n5ejSchiFAAJ6BzIb6KqBSnKLBdQGT4bLAQADAgADeQADNgQ'},
        {'name': 'Цезарь с лососем', 'desc': 'Лосось, с/c черри, пармезан, сухари. салат, соус цезарь, яйцо перепелиное (280г)', 'price': '900р', 'photo': 'AgACAgIAAxkBAAIGJWfQgFwx6XDJd4Q4-4H-aWbrNssaAAKg6TEb6KqJSjpN_LWADeJpAQADAgADeQADNgQ'},
        {'name': 'Пражский', 'desc': 'Телятина. перец болгарский, шампиньоны, кабачки, соевый соус, сметана, кетчуп, салат (340г)', 'price': '600р', 'photo': 'AgACAgIAAxkBAAIF42fQeqZC8zwGmSchtzokIM5mDAqyAAJ2BzIb6KqBSmG8dD0YfIrjAQADAgADeQADNgQ'},
        {'name': 'Каталонский', 'desc': 'Прошутто, дорблю, салат, черри, груша, белое вино, медовоя горчица, орех грецкий   (340г)', 'price': '930р', 'photo': 'AgACAgIAAxkBAAIILGfROVDuaTAeo-LTKYd9Bp1_80pqAALwKDIbYVSJSiz92BddRKLcAQADAgADeAADNgQ'},
        {'name': 'Сальмоне', 'desc': 'Черри, киноа, авокадо, лосось, яйцо, сальсо овощная  (310г)', 'price': '760р', 'photo': 'AgACAgIAAxkBAAIGE2fQftj_IX-mi-IRoO6pYKOiKig9AALHBzIb6KqBShhtIQvQSKPwAQADAgADeQADNgQ'}
        
    ],
    "🍢Закуски": [
        {'name': 'Сало по домашнему', 'desc': 'Сало соленое, сало копченое, чеснок, лук зеленый, горчица (240/50г)', 'price': '520р', 'photo': 'AgACAgIAAxkBAAIILGfROVDuaTAeo-LTKYd9Bp1_80pqAALwKDIbYVSJSiz92BddRKLcAQADAgADeAADNgQ'},
        {'name': 'Греночки', 'desc': 'Хлеб черный, соус чесночный (180/40г)', 'price': '220р', 'photo': 'AgACAgIAAxkBAAIGF2fQfyVvGx1BPz6Ugs0hm9w2mQcWAALSBzIb6KqBSpXwHS9VzYt3AQADAgADeQADNgQ'},
        {'name': 'Крылашки Буффало', 'desc': 'Крылышки, соус BBQ, специ,  (350/50г)', 'price': '400р', 'photo': 'AgACAgIAAxkBAAIGAWfQfXgAAYc7gWViKQTX4KvKojZOxQACqgcyG-iqgUpdHiLznvCpJgEAAwIAA3kAAzYE'},
        {'name': 'Тар тар с лососем', 'desc': 'Лосось с/c, лук, авокадо, соус устричный, черри, филадельфия, лимон, багет (215г)', 'price': '680р', 'photo': 'AgACAgIAAxkBAAIF3WfQeit0JlK1oEKfQ65632jnfU_MAAJmBzIb6KqBSlnh0eGm9IVxAQADAgADeQADNgQ'},
        {'name': 'Тар тар с говядиной', 'desc': 'Вырезка говяжья, помидор, горчица дижонская, лук, корнишоны, пармезан, перец чили, яйца перепелиные, багет (240г)', 'price': '750р', 'photo': 'AgACAgIAAxkBAAIGYmfQh4jELICv1rPfhby8mvnv3Bo-AALk6jEb6KqJSgrpJU31Fv1bAQADAgADeQADNgQ'},
        {'name': 'Паштет куриный', 'desc': 'Паштет из куриной печени, соус черная смородина,багет (200/50г)', 'price': '470р', 'photo': 'AgACAgIAAxkBAAIGNmfQgtcDceXnCVLU1EWCHMrL8ledAAKd6jEb6KqJStOPTusmnySrAQADAgADeQADNgQ'},
        {'name': 'Мидии в томатном соусе', 'desc': 'Мидии в ракушке, чеснок, вино белое, соус соевый, соус маринара (400г)', 'price': '650р', 'photo': 'AgACAgIAAxkBAAIGFWfQfwgEKiUHx2l8O_ruyKbITcRBAALLBzIb6KqBSgrvZ0NKx9jAAQADAgADeQADNgQ'},
        {'name': 'Мидии в сливочном соусе', 'desc': 'Мидии в ракушке, вино белое, чеснок, тимьян, соус соевый, сливки, дорблю, пармезан, лимон   (300г)', 'price': '700р', 'photo': 'AgACAgIAAxkBAAIGH2fQf7vdNgcwUgABIvqg9mVF-jIfhQAC5QcyG-iqgUq30Ez3zgZV3QEAAwIAA3gAAzYE'},
        {'name': 'Карпаччо из говядины', 'desc': 'Вырезка говяжья, черри, руккола. лимон, специи (200г)', 'price': '900р', 'photo': 'AgACAgIAAxkBAAIF-WfQfLGFotc5IFU5eT-6yGayhyvxAAKVBzIb6KqBSsIN7IwNJaQcAQADAgADeQADNgQ'},
        {'name': 'Брускетта с бужениной', 'desc': 'Чиабатта, буженина, масло сливочное, зелень, огурец соленый, черри, салат (350г)', 'price': '470р', 'photo': 'AgACAgIAAxkBAAIILGfROVDuaTAeo-LTKYd9Bp1_80pqAALwKDIbYVSJSiz92BddRKLcAQADAgADeAADNgQ'},
        {'name': 'Брускетта с лососем', 'desc': 'Лосось с/c, филадельфия, оливки, огурец свежий, багет  (250г)', 'price': '600р', 'photo': 'AgACAgIAAxkBAAIILGfROVDuaTAeo-LTKYd9Bp1_80pqAALwKDIbYVSJSiz92BddRKLcAQADAgADeAADNgQ'},
        {'name': 'Рыбная нарезка', 'desc': 'Лосось с/c, салат, лимон (180г)', 'price': '1000р', 'photo': 'AgACAgIAAxkBAAIILGfROVDuaTAeo-LTKYd9Bp1_80pqAALwKDIbYVSJSiz92BddRKLcAQADAgADeAADNgQ'},
        {'name': 'Сырное плато', 'desc': 'Дорблю, гаунда, камамбер, пармезан, мед, орех грецкий, виноград (210/40г)', 'price': '900р', 'photo': 'AgACAgIAAxkBAAIF72fQe7C0ONay-bE6eV7GkSh-FwdoAAKIBzIb6KqBSpQ-ERw1uA0TAQADAgADeQADNgQ'},
        {'name': 'Мясная нарезка', 'desc': 'Буженина, бекон, колбаски охотничьи, грудка копченная, хрен, горчица  (430/60г)', 'price': '1000р', 'photo': 'AgACAgIAAxkBAAEWfWhn0C1dqEyFNuaXxLnyFtYQ0eHVYQACyukxG-iqiUq4IYw4JX4qsgEAAwIAA3kAAzYE'},
        {'name': 'Овощная нарезка', 'desc': 'Помидор, огурец свежий, зелень, перец болгарский, лук крымский, салат (330г)', 'price': '430р', 'photo': 'AgACAgIAAxkBAAIGCWfQffhgIkxPM4VnGfnCXiIrhn4DAAK7BzIb6KqBSmLZv7Q--PanAQADAgADeQADNgQ'},
        {'name': 'Селедочка под водочку', 'desc': 'Селедка, картофель, хлеб темный, лук (450г)', 'price': '520р', 'photo': 'AgACAgIAAxkBAAIGWmfQhsy3M-XoLfn6z8BELrJ-Kwc-AALW6jEb6KqJSqL5-3MSgau6AQADAgADeQADNgQ'},
        {'name': 'Сырные палочки', 'desc': 'Сырные палочки, соус на выбор: чесночный/сливочный/брусничный (200/50г)', 'price': '400р', 'photo': 'AgACAgIAAxkBAAIF4WfQeoJUr5qow6F3LFGEwRupKzczAAJ1BzIb6KqBSiXrmJZGdz9UAQADAgADeQADNgQ'},
        {'name': 'Креветка в темпура', 'desc': 'Креветки, васаби, чеснок, соус соевый, лимон, соус терияки, соус свит чили (300/90г)', 'price': '780р', 'photo': 'AgACAgIAAxkBAAIGOGfQgxs9L4i5Sd3KBU42UirTaN5MAAKh6jEb6KqJSge4o7k2prldAQADAgADeQADNgQ'},
        {'name': 'Креветка в кисло-сладком соусе', 'desc': 'Креветки, тимьян, чеснок, соус соевый, соус терияки, соус манго-чили, соус свит-чили, лимон (270г)', 'price': '850р', 'photo': 'AgACAgIAAxkBAAIF_2fQfTn0DqUYvSyOSGKHQ_KuZAT4AAKdBzIb6KqBSqUt47-T0FvIAQADAgADeQADNgQ'},
        {'name': 'Азовская тюлька', 'desc': 'Тюлька, специи, лимон (200/30г)', 'price': '320р', 'photo': 'AgACAgIAAxkBAAIGcmfQiLRrjHZayEXBf-dkOOaYUMF3AAL86jEb6KqJSh2juMFd7J32AQADAgADeQADNgQ'},
        {'name': 'Вяленные деликатесы', 'desc': 'Шея сыровяленая, бастурма говяжья, свиная вырезка сыовяленая (150г)', 'price': '680р', 'photo': 'AgACAgIAAxkBAAIGdGfQiPXv5By1sW3h6GwJxINlyKSmAAIC6zEb6KqJSmZ5bauNORBqAQADAgADeQADNgQ'},
        {'name': 'Пивная тарелка', 'desc': 'Крылышки, сырные палочки, луковые кольца, соус BBQ, гренки (470/50г)', 'price': '720р', 'photo': 'AgACAgIAAxkBAAIF52fQevSeg_lzeAu8nx7_vL-RJpNFAAJ-BzIb6KqBSj_DKEicnh31AQADAgADeQADNgQ'},
        {'name': 'Фруктовая нарезка', 'desc': ' (150г)', 'price': '680р', 'photo': 'AgACAgIAAxkBAAIHlWfQkK4dtzJC6NL7hyGUUVsHEXBpAALS6TEb6KqJStKmYJiluRZqAQADAgADeQADNgQ'},
        {'name': 'Мясная нарезка', 'desc': 'Шея сыровяленая, бастурма говяжья, свиная вырезка сыовяленая (150г)', 'price': '680р', 'photo': 'AgACAgIAAxkBAAIF2WfQedbre4DoZoMS_VlyZ9nBQSCCAALK6TEb6KqJSombxCMf5Iz4AQADAgADeQADNgQ'}
    ],
    "🍚Гарнир": [
        {'name': 'Овощи запеченные', 'desc': 'Кабачок, баклажан, перец болгарский, помидор, лук, чеснок, перец чили, специи, зелень (350г)', 'price': '430р', 'photo': 'AgACAgIAAxkBAAIGcGfQiIkZ50aZ8XfxGPLezR2HQ3FKAAL66jEb6KqJSp3Y8olQ0bUAAQEAAwIAA3kAAzYE'},
        {'name': 'Картофель по-сельски', 'desc': 'Картофель, чеснок, зелень (250г)', 'price': '220р', 'photo': 'AgACAgIAAxkBAAIGemfQiXRrN8rk-50NuQQTRzEJCoLLAAI06zEb6KqJSgXJIqVK3cPzAQADAgADeAADNgQ'},
        {'name': 'Картофель фри', 'desc': 'Картофель фри, соус (200/50г)', 'price': '300р', 'photo': 'AgACAgIAAxkBAAIILGfROVDuaTAeo-LTKYd9Bp1_80pqAALwKDIbYVSJSiz92BddRKLcAQADAgADeAADNgQ'},
        {'name': 'Картофель отварной', 'desc': 'Картофель, зелень (150г)', 'price': '200р', 'photo': 'AgACAgIAAxkBAAIILGfROVDuaTAeo-LTKYd9Bp1_80pqAALwKDIbYVSJSiz92BddRKLcAQADAgADeAADNgQ'},
        {'name': 'Картофельное пюре', 'desc': 'Картофель, молоко (150г)', 'price': '200р', 'photo': 'AgACAgIAAxkBAAIILGfROVDuaTAeo-LTKYd9Bp1_80pqAALwKDIbYVSJSiz92BddRKLcAQADAgADeAADNgQ'},
        {'name': 'Плов с овощами', 'desc': 'Рис, лук, морковь, мексиканская смесь, фасоль, специи (250г)', 'price': '300р', 'photo': 'AgACAgIAAxkBAAIGJ2fQgIeDODZHQHGa7ssQAAG1CX47CwACoekxG-iqiUpoXZLRoG_zygEAAwIAA3kAAzYE'},
        {'name': 'Плов из говядины', 'desc': 'Телятина, рис, лук, морковь, чеснок, специи (300г)', 'price': '400р', 'photo': 'AgACAgIAAxkBAAIGC2fQfiXdp3Qz7IVJYvmOFJkoQgABhQACvwcyG-iqgUrp9a4iQCxalQEAAwIAA3gAAzYE'},
        {'name': 'Тяхан', 'desc': 'Рис, куриное филе, морковь, чеснок, соус соевый, лук, перец болгарский (300г)', 'price': '320р', 'photo': 'AgACAgIAAxkBAAIGbmfQiGTCsgTdKzkb6lLyEZHXoqNcAAL26jEb6KqJSidyys15Kz-8AQADAgADeQADNgQ'}
    ],
    "🍝Пасты": [
        {'name': 'Паста с чернилами каракатицы', 'desc': 'Паста с чернилами каракатицы, черри, чеснок, соус рыбный, морской коктейл, сливки, специи (300г)', 'price': '700р', 'photo': 'AgACAgIAAxkBAAIGOmfQg0v0D_eRmX7bDjSZIBQuqnAhAAKm6jEb6KqJSnwLX9Ims2V0AQADAgADeAADNgQ'},
        {'name': 'Фетучини', 'desc': 'Паста, курица, шампиньоны, помидор, соус соевый, пармезан, сливки, специи (350г)', 'price': '580р', 'photo': 'AgACAgIAAxkBAAIGbGfQiEZ1uUhVGZKTuQvNUr0z5s1JAALy6jEb6KqJSrdbC4-takROAQADAgADeQADNgQ'},
        {'name': 'Паста болоньезе', 'desc': 'Паста, телятина, вино белое, соус томатный, чеснок, соус соевый, пармезан, специи  (300г)', 'price': '680р', 'photo': 'AgACAgIAAxkBAAIGPGfQg36fYfPjaVoi1nQqMyv3P3OEAAKn6jEb6KqJSo8ai0PXkPTuAQADAgADeQADNgQ'},
        {'name': 'Карбонара', 'desc': 'Патса, бекон, сливки, пармезан, желток, соус соевый (330г)', 'price': '600р', 'photo': 'AgACAgIAAxkBAAEWfc5n0D9nRUZzfSbSztn-QagQ2l7tewACvOoxG-iqiUpRAAHRu03rftgBAAMCAAN5AAM2BA'},
        {'name': 'Удон с курицей и овощами', 'desc': 'Удон, курица, перец болгарский, лук, фасоль, чеснок, унаги, соус соевый, кунжут (280г)', 'price': '500р', 'photo': 'AgACAgIAAxkBAAIF-2fQfN7lAjdc-YcekphYn0L8CSUsAAKXBzIb6KqBSnvsBrBiopaUAQADAgADeQADNgQ'},
        {'name': 'Лазанья', 'desc': 'Паста листовая, свинина, телятина, помидоры, лук, чеснок, соус бешамель, томатный соус (400г)', 'price': '520р', 'photo': 'AgACAgIAAxkBAAIGA2fQfZnpAcn_PIxb0zduKuwdtSafAAKxBzIb6KqBSqrpmsw8F7UeAQADAgADeQADNgQ'}
    ],
    "🔥Мангал": [
        {'name': 'Перепелка', 'desc': 'Салат, черри, укроп, красный острый перец (300г)', 'price': '650р', 'photo': 'AgACAgIAAxkBAAIGamfQiBtIntNEzTCVaX_m5DDXbW2tAALt6jEb6KqJSiQDipZ0vjVHAQADAgADeQADNgQ'},
        {'name': 'Каре ягненка', 'desc': 'Лаваш, черри, салат, аджика (200г)', 'price': '900р', 'photo': 'AgACAgIAAxkBAAIGG2fQf2PZ5tUr-hSZt1WH4H__lRIeAALeBzIb6KqBSn06ziIL6OIGAQADAgADeQADNgQ'},
        {'name': 'Форель', 'desc': 'Соус дзадзики (300г)', 'price': '900р', 'photo': 'AgACAgIAAxkBAAIILGfROVDuaTAeo-LTKYd9Bp1_80pqAALwKDIbYVSJSiz92BddRKLcAQADAgADeAADNgQ'},
        {'name': 'Лосось', 'desc': 'Соус дзадзики(300г)', 'price': '900р', 'photo': 'AgACAgIAAxkBAAIILGfROVDuaTAeo-LTKYd9Bp1_80pqAALwKDIbYVSJSiz92BddRKLcAQADAgADeAADNgQ'},
        {'name': 'Сибас', 'desc': 'Соус дзадзики (300г)', 'price': '900р', 'photo': 'AgACAgIAAxkBAAIGPmfQg6y7X14DWsxyxMzcTXOlCHVfAAKp6jEb6KqJSjM4v07Mg8AzAQADAgADeQADNgQ'},
        {'name': 'Скумбрия', 'desc': 'Соус дзадзики (300г)', 'price': '850р', 'photo': 'AgACAgIAAxkBAAIILGfROVDuaTAeo-LTKYd9Bp1_80pqAALwKDIbYVSJSiz92BddRKLcAQADAgADeAADNgQ'},
        {'name': 'Дорадо', 'desc': 'Салат, лимон, красный острый перец, соус дзадзики (300г)', 'price': '1100р', 'photo': 'AgACAgIAAxkBAAIGZmfQh9epPU27ofJ5RdTWiqJezGywAALo6jEb6KqJSmc6EHz82Uq2AQADAgADeQADNgQ'},
        {'name': 'Шашлык из свинины', 'desc': 'Лаваш, лук маринованный, аджика, черри, салат, соус красный (200г)', 'price': '550р', 'photo': 'AgACAgIAAxkBAAIGHWfQf4ZPEMCdcVo2H05sUdci79EFAALfBzIb6KqBSvc_nbN-JtvFAQADAgADeQADNgQ'},
        {'name': 'Шашлыки из баранины', 'desc': 'Шашлык баранина, лаваш, лук маринованный, аджика, черри, салат, соус красный (200г)', 'price': '850р', 'photo': 'AgACAgIAAxkBAAIILGfROVDuaTAeo-LTKYd9Bp1_80pqAALwKDIbYVSJSiz92BddRKLcAQADAgADeAADNgQ'},
        {'name': 'Шашлык из свиного антрекота', 'desc': 'Лаваш, аджика, лук маринованный, салат, черри (250г)', 'price': '600р', 'photo': 'AgACAgIAAxkBAAIILGfROVDuaTAeo-LTKYd9Bp1_80pqAALwKDIbYVSJSiz92BddRKLcAQADAgADeAADNgQ'},
        {'name': 'Овощи гриль', 'desc': 'Кабачки, баклажан, перец, помидор, кукуруза, шампиньоны (350г)', 'price': '500р', 'photo': 'AgACAgIAAxkBAAIF32fQelAmZIi_qYytt5duRv04l3s5AAJsBzIb6KqBSiOFWAoqaCnFAQADAgADeQADNgQ'},
        {'name': 'Шашлык из курциы', 'desc': 'Шашлык курица, лаваш, лук маринвоанный, салат, черри, соус белый (200г)', 'price': '450р', 'photo': 'AgACAgIAAxkBAAIILGfROVDuaTAeo-LTKYd9Bp1_80pqAALwKDIbYVSJSiz92BddRKLcAQADAgADeAADNgQ'},
        {'name': 'Колбаски свиные', 'desc': 'Лаваш, лук маринованный, соус красный, 3шт', 'price': '900р', 'photo': 'AgACAgIAAxkBAAIILGfROVDuaTAeo-LTKYd9Bp1_80pqAALwKDIbYVSJSiz92BddRKLcAQADAgADeAADNgQ'},
        {'name': 'Колбаски куриные', 'desc': 'Лаваш, лук маринованный, соус белый 3шт', 'price': '900р', 'photo': 'AgACAgIAAxkBAAIILGfROVDuaTAeo-LTKYd9Bp1_80pqAALwKDIbYVSJSiz92BddRKLcAQADAgADeAADNgQ'},
        {'name': 'Люля из курицы', 'desc': 'Лаваш, соус дзадзики, лук маринованный, салат, черри (200г)', 'price': '450р', 'photo': 'AgACAgIAAxkBAAIGQmfQhA0cTkzDz9D0GJn_v1POCU8uAAKs6jEb6KqJSjdeBRxPKAZxAQADAgADeQADNgQ'},
        {'name': 'Люля из баранины', 'desc': 'Лаваш, аджика, лук маринованный, салат, черри  (200г)', 'price': '850р', 'photo': 'AgACAgIAAxkBAAIGQGfQg-K1prTb_7bXf1CimrFsTfTnAAKr6jEb6KqJSgABfSMdvkeQ0gEAAwIAA3kAAzYE'},
        {'name': 'Люля из говядины', 'desc': 'Лаваш, аджика, лук маринованный, салат, черри (200г)', 'price': '650р', 'photo': 'AgACAgIAAxkBAAIGIWfQf-z4Lg9RGhgQUmLY3bMhzH7KAAInMDIbYVSBStdL6PUQrewhAQADAgADeAADNgQ'}
    ],
    "🍕Пицца 30см": [
        {'name': 'Техас', 'desc': 'Бекон, пепперони, моцарелла, перец, халапенью, соус манго-чили, соус маринара, помидор (580г)', 'price': '650р', 'photo': 'AgACAgIAAxkBAAIILGfROVDuaTAeo-LTKYd9Bp1_80pqAALwKDIbYVSJSiz92BddRKLcAQADAgADeAADNgQ'},
        {'name': 'Барбекю', 'desc': 'Колбаски охотничьи, пармезан, моцарелла, лук маринованный, черри, соус чесночный, соус BBQ (760г)', 'price': '600р', 'photo': 'AgACAgIAAxkBAAIF6WfQexUVCPw5sKNXKk9ijur19HA9AAKABzIb6KqBSkqVo9TSp8nMAQADAgADeQADNgQ'},
        {'name': 'Итальяно', 'desc': 'Хамон, моцарелла, дорблю, помидорЮ, руккола, сливки (675г)', 'price': '950р', 'photo': 'AgACAgIAAxkBAAIGRGfQhDlr9SJ_nKD51BbuRC2UQFQeAAKu6jEb6KqJSrhqdMVp9H_WAQADAgADeQADNgQ'},
        {'name': 'Гавайская', 'desc': 'Грудка куриная копченая, моцарелла, кукуруза, ананс, сливки (670г)', 'price': '750р', 'photo': 'AgACAgIAAxkBAAIGRmfQhG0jy7nWW5abRLO49XAljMFDAAKy6jEb6KqJSk6CJXfmwxSJAQADAgADeAADNgQ'},
        {'name': 'Карбонара', 'desc': 'Бекон, моцарелла, руккола, яйцо перепелиное, помидор, шампиньоны, сливки   (710г)', 'price': '800р', 'photo': 'AgACAgIAAxkBAAIGSGfQhJGfs_6w1R9QesA2Bxe4iwABgQACtOoxG-iqiUqoFOv5A9j0nQEAAwIAA3kAAzYE'},
        {'name': 'Баварская', 'desc': 'Колбаски охотничьи, шампиньоны, соус маринара, моцарелла, огурцы маринованные (670г)', 'price': '680р', 'photo': 'AgACAgIAAxkBAAIGSmfQhLnsoXAewBS93GiHD3CdMph6AAK56jEb6KqJSiOsGbw4o-KhAQADAgADeQADNgQ'},
        {'name': 'Соблазн', 'desc': 'Креветка, бекон, ветчина, сливки, моцарелла, соус шрирача, помидор, огурец соленый (600г)', 'price': '750р', 'photo': 'AgACAgIAAxkBAAIF_WfQfQQEpYf-IpMNK4mLBlfbpZ44AAKYBzIb6KqBSrwxrysWuBpNAQADAgADeQADNgQ'},
        {'name': 'Пепперони', 'desc': 'Пепперони, моцарелла, соус маринара (520г)', 'price': '780р', 'photo': 'AgACAgIAAxkBAAIGTmfQhX45TPWHBaT9ZZ2Lh6mgOlNXAALA6jEb6KqJSpCbuvXcryTKAQADAgADeQADNgQ'},
        {'name': 'Филадельфия', 'desc': 'Лаваш, аджика, лук маринованный, салат, черри  (200г)', 'price': '850р', 'photo': 'AgACAgIAAxkBAAIGUGfQhbgAAboksb_TAAFbcf_TKFL6FwMAAsfqMRvoqolKu9eWabWDKV0BAAMCAAN5AAM2BA'},
        {'name': 'Груша Дорблю', 'desc': 'Лаваш, аджика, лук маринованный, салат, черри  (200г)', 'price': '850р', 'photo': 'AgACAgIAAxkBAAIF92fQfIvVfzds2lIOPgQnTpSAxm8XAAKOBzIb6KqBSnDezJc6wLtEAQADAgADeQADNgQ'},
        {'name': 'Лосось Терияки', 'desc': 'Лаваш, аджика, лук маринованный, салат, черри  (200г)', 'price': '850р', 'photo': 'AgACAgIAAxkBAAIILGfROVDuaTAeo-LTKYd9Bp1_80pqAALwKDIbYVSJSiz92BddRKLcAQADAgADeAADNgQ'},
        {'name': 'Капричеза', 'desc': 'Лаваш, аджика, лук маринованный, салат, черри  (200г)', 'price': '850р', 'photo': 'AgACAgIAAxkBAAIGUmfQheAUbKSgIo3flVr1VGHUx2n1AALI6jEb6KqJShU-A8FtYIb2AQADAgADeQADNgQ'},
        {'name': 'Том-ям', 'desc': 'Лаваш, аджика, лук маринованный, салат, черри  (200г)', 'price': '850р', 'photo': 'AgACAgIAAxkBAAIILGfROVDuaTAeo-LTKYd9Bp1_80pqAALwKDIbYVSJSiz92BddRKLcAQADAgADeAADNgQ'},
        {'name': 'Маргарита', 'desc': 'Лаваш, аджика, лук маринованный, салат, черри  (200г)', 'price': '850р', 'photo': 'AgACAgIAAxkBAAIILGfROVDuaTAeo-LTKYd9Bp1_80pqAALwKDIbYVSJSiz92BddRKLcAQADAgADeAADNgQ'},
        {'name': 'Диабло', 'desc': 'Лаваш, аджика, лук маринованный, салат, черри  (200г)', 'price': '850р', 'photo': 'AgACAgIAAxkBAAIILGfROVDuaTAeo-LTKYd9Bp1_80pqAALwKDIbYVSJSiz92BddRKLcAQADAgADeAADNgQ'},
        {'name': 'Пицца с лососем и креветками', 'desc': 'Лаваш, аджика, лук маринованный, салат, черри  (200г)', 'price': '850р', 'photo': 'AgACAgIAAxkBAAIILGfROVDuaTAeo-LTKYd9Bp1_80pqAALwKDIbYVSJSiz92BddRKLcAQADAgADeAADNgQ'},
        {'name': 'Пицца Цезарь', 'desc': 'Лаваш, аджика, лук маринованный, салат, черри  (200г)', 'price': '850р', 'photo': 'AgACAgIAAxkBAAIGI2fQgCLfVMF6e8HbxZI8ju4XY-JlAAIsMDIbYVSBShnkn99I5fq8AQADAgADeAADNgQ'},
        {'name': '4 сыра', 'desc': 'Лаваш, аджика, лук маринованный, салат, черри  (200г)', 'price': '850р', 'photo': 'AgACAgIAAxkBAAIEVmfQUsknVCHx7_KJQkxhhz3sm7jjAALN6jEb6KqJSrzgyNWSwxj7AQADAgADeQADNgQ'},
        {'name': 'Хачапури по-аджарски', 'desc': 'Лаваш, аджика, лук маринованный, салат, черри  (200г)', 'price': '850р', 'photo': 'AgACAgIAAxkBAAIGEWfQfrKCQQhtCEF3WfIX0P_oLLhvAALGBzIb6KqBSibc_ues_wAB8wEAAwIAA3kAAzYE'},
        {'name': 'Мясная', 'desc': 'Лаваш, аджика, лук маринованный, салат, черри  (200г)', 'price': '850р', 'photo': 'AgACAgIAAxkBAAIF9WfQfBmy2tDoVYH9EEpp_CgtlnV3AAKNBzIb6KqBSkb5bc8uRcKgAQADAgADeQADNgQ'},
        {'name': 'Американо', 'desc': 'Лаваш, аджика, лук маринованный, салат, черри  (200г)', 'price': '850р', 'photo': 'AgACAgIAAxkBAAIILGfROVDuaTAeo-LTKYd9Bp1_80pqAALwKDIbYVSJSiz92BddRKLcAQADAgADeAADNgQ'}
    ],
    "🍕Пицца 45см": [
        {'name': 'Том-ям', 'desc': 'Креветка, кальмар, сливки, том-ям паста, моцарелла, шампиньоны, черри  (1180г)', 'price': '1350р', 'photo': 'AgACAgIAAxkBAAIILGfROVDuaTAeo-LTKYd9Bp1_80pqAALwKDIbYVSJSiz92BddRKLcAQADAgADeAADNgQ'},
        {'name': '4 Сыра', 'desc': 'Пармезан, дорблю, гауда, моцарелла, орехи грецкий, груша, сливки  (1170г)', 'price': '1500р', 'photo': 'AgACAgIAAxkBAAIEVmfQUsknVCHx7_KJQkxhhz3sm7jjAALN6jEb6KqJSrzgyNWSwxj7AQADAgADeQADNgQ'},
        {'name': 'Диабло', 'desc': 'Колбаски охотничьи, соус шрирача, моцарелла, пеперони, халапенью, соус BBQ, огурцы маринованные  (1200г)', 'price': '1200р', 'photo': 'AgACAgIAAxkBAAIILGfROVDuaTAeo-LTKYd9Bp1_80pqAALwKDIbYVSJSiz92BddRKLcAQADAgADeAADNgQ'},
        {'name': 'Американо', 'desc': 'Колбаски охотничьи, пепперони, перец болгарский, кукуруза, унаги, моцарелла, соус маринара, BBQ (1200г)', 'price': '1200р', 'photo': 'AgACAgIAAxkBAAIILGfROVDuaTAeo-LTKYd9Bp1_80pqAALwKDIbYVSJSiz92BddRKLcAQADAgADeAADNgQ'},
        {'name': 'Соблазн', 'desc': 'Креветка, бекон, ветчина, сливки, моцарелла, соус шрирача, помидор, огурец маринованный (1220г)', 'price': '1250р', 'photo': 'AgACAgIAAxkBAAIF_WfQfQQEpYf-IpMNK4mLBlfbpZ44AAKYBzIb6KqBSrwxrysWuBpNAQADAgADeQADNgQ'},
        {'name': 'Карбонара', 'desc': 'Бекон, моцарелла, руккола, яйцо перепелиное, помидор, шампиньоны, сливки   (1320г)', 'price': '1300р', 'photo': ' AgACAgIAAxkBAAIGSGfQhJGfs_6w1R9QesA2Bxe4iwABgQACtOoxG-iqiUqoFOv5A9j0nQEAAwIAA3kAAzYE'},
        {'name': 'Итальяно', 'desc': 'Прошутто, моцарелла, дорблю, помидор, руккола, сливки  (1220г)', 'price': '1500р', 'photo': 'AgACAgIAAxkBAAIGRGfQhDlr9SJ_nKD51BbuRC2UQFQeAAKu6jEb6KqJSrhqdMVp9H_WAQADAgADeQADNgQ'},
        {'name': 'Мясная', 'desc': 'Соус BBQ, охотничьи колбаски, грудка копченая, ветчина, моцарелла, пепперони, черри, маринара, маслины/сливки (1340г)', 'price': '1250р', 'photo': 'AgACAgIAAxkBAAIF9WfQfBmy2tDoVYH9EEpp_CgtlnV3AAKNBzIb6KqBSkb5bc8uRcKgAQADAgADeQADNgQ'}
    ],
    "🍣Суши": [],
    "🍣Роллы": [],
    "🍖Горячие блюда": [
        {'name': 'Бефстроганов из говядины с картофельным пюре', 'desc': 'Мякоть говяжья, лук, чеснок, шампиньоны, сливки, специи6 картофельное пюре  (250/150г)', 'price': '680р', 'photo': 'AgACAgIAAxkBAAIGeGfQiU8_dltKmcF-5yZZrk7SeClwAAIi6zEb6KqJSgLWUjm_eYo2AQADAgADeAADNgQ'},
        {'name': 'Бифштекс с яйцом и пюре', 'desc': 'Говядина, лук, яйцо, картофельное пюре, специи  (400г)', 'price': '580р', 'photo': 'AgACAgIAAxkBAAIILGfROVDuaTAeo-LTKYd9Bp1_80pqAALwKDIbYVSJSiz92BddRKLcAQADAgADeAADNgQ'},
        {'name': 'Рибай с запеченным перцем', 'desc': 'Рибай, перец болгарский, специи (340/40г)', 'price': '1600р', 'photo': 'AgACAgIAAxkBAAIF7WfQe5P8nVhcK4HKrEuzqCV758XwAAKEBzIb6KqBSsRf6jMY5BheAQADAgADeQADNgQ'},
        {'name': 'Медальоны свиные с жареной картошкой', 'desc': 'Свиная вырезка, бекон, жареный картофель, черри, зелень, специи, сливочно-сырный соус  (450г)', 'price': '780р', 'photo': 'AgACAgIAAxkBAAIF22fQefyj-5elho8Ph1UydJF9m_uRAAJiBzIb6KqBSoh6cdREW1ljAQADAgADeQADNgQ'},
        {'name': 'Сковорода по-русски', 'desc': 'Свинина, телятина, курица, картофель, специи, чеснок, зелень (370г)', 'price': '650р', 'photo': 'AgACAgIAAxkBAAIF82fQe_ak6FDFEWWf9i6zKyLUPEQGAAKLBzIb6KqBSmwP86qFVlZ7AQADAgADeQADNgQ'},
        {'name': 'Сковорода по-фермерски', 'desc': 'Свинина, телятина, курица, шампиньоны, фасоль, сельдерей, сметана, соус соевый, зелень  (460г)', 'price': '700р', 'photo': 'AgACAgIAAxkBAAIGGWfQf0f0yju7Civj-pUWgkaqITWvAALdBzIb6KqBSkitdEeY-iPbAQADAgADeQADNgQ'},
        {'name': 'Курица в кисло-сладком соусе', 'desc': 'Куриное филе, перец болгарский, чеснок, соус свит-чили, специи, кунжут (320г)', 'price': '900р', 'photo': 'AgACAgIAAxkBAAIILGfROVDuaTAeo-LTKYd9Bp1_80pqAALwKDIbYVSJSiz92BddRKLcAQADAgADeAADNgQ'},
        {'name': 'Утиная грудка с грибной подушкой и картофельным пюре', 'desc': 'Утина грудка, шампиньоны, сливки, картофельное пюре, специи  (450г)', 'price': '900р', 'photo': 'AgACAgIAAxkBAAIILGfROVDuaTAeo-LTKYd9Bp1_80pqAALwKDIbYVSJSiz92BddRKLcAQADAgADeAADNgQ'},
        {'name': 'Куриная панчетта', 'desc': 'Куриное филе, фасоль, специи, шампиньоны, соус белый, соус соевый  (330г)', 'price': '750р', 'photo': 'AgACAgIAAxkBAAIGaGfQh_hg5UI4zskWl4E086peFkuhAALr6jEb6KqJStbBlE-RZon6AQADAgADeQADNgQ'},
        {'name': 'Сковородка с грибами и луком', 'desc': 'Шампиньоны, картофель, лук, специи, зелень  (400г)', 'price': '580р', 'photo': 'AgACAgIAAxkBAAIGfGfQiZywJ1exWZEX19vEFpBOtQmwAAI_6zEb6KqJSjQwQ6ZUSFVSAQADAgADeQADNgQ'},
        {'name': 'Хинкали со свининой', 'desc': 'Свиной фарш, тесто, сметана  (215/50г)', 'price': '300р', 'photo': 'AgACAgIAAxkBAAIILGfROVDuaTAeo-LTKYd9Bp1_80pqAALwKDIbYVSJSiz92BddRKLcAQADAgADeAADNgQ'},
        {'name': 'Хинкали с говядиной', 'desc': 'Говяжий фарш, тесто, сметана  (215/50г)', 'price': '300р', 'photo': 'AgACAgIAAxkBAAIILGfROVDuaTAeo-LTKYd9Bp1_80pqAALwKDIbYVSJSiz92BddRKLcAQADAgADeAADNgQ'}
    ],
    "🍜Первые блюда": [
        {'name': 'Борщ красный с салом', 'desc': 'Говяжий бульон, говядина, картофель, морковь, лук, капуста, томатная паста, специи, свекла, сметана, сало соленое (300/40/40г)', 'price': '480р', 'photo': 'AgACAgIAAxkBAAIGZGfQh7ZXbVJQde74UZ3O-ILCJhxQAALn6jEb6KqJStxZHbNWOZefAQADAgADeQADNgQ'},
        {'name': 'Шурпа из баранины', 'desc': 'Прошутто, моцарелла, дорблю, помидор, руккола, сливки  (1220г)', 'price': '1500р', 'photo': 'AgACAgIAAxkBAAIILGfROVDuaTAeo-LTKYd9Bp1_80pqAALwKDIbYVSJSiz92BddRKLcAQADAgADeAADNgQ'},
        {'name': 'Солянка', 'desc': 'Прошутто, моцарелла, дорблю, помидор, руккола, сливки  (1220г)', 'price': '1500р', 'photo': 'AgACAgIAAxkBAAIGVmfQhjA4Y2W55uTFp_Y6jy96vulGAALP6jEb6KqJSn_sTmG39I2jAQADAgADeQADNgQ'},
        {'name': 'Бульон куриный', 'desc': 'Прошутто, моцарелла, дорблю, помидор, руккола, сливки  (1220г)', 'price': '1500р', 'photo': 'AgACAgIAAxkBAAIILGfROVDuaTAeo-LTKYd9Bp1_80pqAALwKDIbYVSJSiz92BddRKLcAQADAgADeAADNgQ'},
        {'name': 'Грибной крем-суп', 'desc': 'Прошутто, моцарелла, дорблю, помидор, руккола, сливки  (1220г)', 'price': '1500р', 'photo': 'AgACAgIAAxkBAAIILGfROVDuaTAeo-LTKYd9Bp1_80pqAALwKDIbYVSJSiz92BddRKLcAQADAgADeAADNgQ'},
        {'name': '', 'desc': 'Прошутто, моцарелла, дорблю, помидор, руккола, сливки  (1220г)', 'price': '1500р', 'photo': ''},
        {'name': '', 'desc': 'Прошутто, моцарелла, дорблю, помидор, руккола, сливки  (1220г)', 'price': '1500р', 'photo': ''},
        {'name': '', 'desc': 'Прошутто, моцарелла, дорблю, помидор, руккола, сливки  (1220г)', 'price': '1500р', 'photo': ''},
        {'name': '', 'desc': 'Прошутто, моцарелла, дорблю, помидор, руккола, сливки  (1220г)', 'price': '1500р', 'photo': ''},
        {'name': '', 'desc': 'Прошутто, моцарелла, дорблю, помидор, руккола, сливки  (1220г)', 'price': '1500р', 'photo': ''}

    ],
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
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Добавить в корзину", callback_data=f"add_{item['name']}")]
        ])

        try:
            # Попытка отправить фото, если оно есть
            if item.get('photo'):
                await bot.send_photo(callback_query.message.chat.id, item['photo'],
                                     caption=f"🍽 {item['name']}\n📌 {item['desc']}\n💰 Цена: {item['price']} руб.",
                                     reply_markup=kb)
            else:
                # Если нет фото, просто отправляем сообщение
                await bot.send_message(callback_query.message.chat.id,
                                       f"🍽 {item['name']}\n📌 {item['desc']}\n💰 Цена: {item['price']} руб.",
                                       reply_markup=kb)
        except TelegramBadRequest as e:
            # В случае ошибки с ID фото, выводим только описание блюда
            if "wrong remote file identifier" in str(e):
                await bot.send_message(callback_query.message.chat.id,
                                       f"🍽 {item['name']}\n📌 {item['desc']}\n💰 Цена: {item['price']} руб.",
                                       reply_markup=kb)
            else:
                # Логируем ошибку или делаем другую обработку, если нужно
                print(f"Ошибка при отправке фото: {e}")
                await bot.send_message(callback_query.message.chat.id,
                                       f"🍽 {item['name']}\n📌 {item['desc']}\n💰 Цена: {item['price']} руб.",
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
@dp.message(lambda message: message.text is not None)  # Принимаем только текстовые сообщения
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
    print("Функция сработала!")
    user_id = callback_query.from_user.id

    # Проверяем, что пользователь существует в user_data
    if user_id not in user_data:
        print(f"Ошибка: user_id {user_id} не найден в user_data")
        await callback_query.answer("Ошибка: данные пользователя отсутствуют. Пожалуйста, начните заново.")
        return

    # Проверяем, что все необходимые данные есть
    if "fio" not in user_data[user_id] or "phone" not in user_data[user_id] or "delivery_method" not in user_data[user_id]:
        print(f"Ошибка: данные не полные для user_id {user_id}")
        await callback_query.answer("Пожалуйста, введите все данные (ФИО, телефон и способ доставки).")
        return

    # Получаем данные заказа
    fio = user_data[user_id]["fio"]
    phone = user_data[user_id]["phone"]
    delivery_method = user_data[user_id]["delivery_method"]

    # Логируем данные заказа
    print(f"Полученные данные: ФИО: {fio}, Телефон: {phone}, Способ доставки: {delivery_method}")

    # Создаем сообщение с деталями заказа
    order_details = f"**Заказ от:** {fio}\n**Телефон:** {phone}\n**Способ доставки:** {delivery_method}"

    try:
        # Попытка отправить уведомление в канал с публичным именем
        print("Попытка отправить сообщение в канал...")
        await bot.send_message('-1002160470436', f"🚨 Новый заказ!\n\n{order_details}")
        print("Сообщение успешно отправлено в канал!")
    except Exception as e:
        # Логируем ошибку
        print(f"Ошибка при отправке уведомления в канал: {e}")
        await callback_query.answer("Ошибка при отправке уведомления в канал. Попробуйте позже.")
        return  # Завершаем функцию, если произошла ошибка

    # После отправки уведомления, уведомляем клиента
    await callback_query.message.answer(f"✅ Ваш заказ подтвержден! Спасибо за заказ!\n\n{order_details}")

    # Логируем успешную отправку уведомления клиенту
    print(f"Сообщение отправлено клиенту: {fio}, {phone}, {delivery_method}")

    # Очищаем данные пользователя
    user_data[user_id] = {}
    print(f"Данные пользователя {user_id} очищены")

    # Закрытие диалога с подтверждением
    await callback_query.answer("Заказ подтвержден!")

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


# Функция для обработки фотографий
async def handle_photo(message: types.Message):
    if message.photo:
        file_id = message.photo[-1].file_id
        await message.answer(f"Ваш file_id: {file_id}")
    else:
        await message.answer("Пожалуйста, отправьте фотографию.")

# Обработчик для сообщений с фотографиями
@dp.message(F.photo)
async def photo_handler(message: types.Message):
    await handle_photo(message)
    

# 📌 Логирование ошибок
async def error_handler(update: types.Update, exception: Exception):
    logging.error(f"Ошибка в обновлении {update}: {exception}")


    return True  # Чтобы бот продолжил работу

def register_handlers(dp: Dispatcher):
    dp.errors.register(error_handler)


# 📌 Запуск бота
async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())