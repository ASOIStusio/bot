# -*- coding: utf-8 -*-
import time
import config
import telebot
#from telebot import types
import requests
import os.path
import random
import datetime
knownUsers=[] # будет хранится в файле
userstep={} # словарь где будет хранится id и имя состояние юзера
#global user_dict
user_dict={}
commands={'start':'команда для начала работы с ботом',
          'help':'Список доступных команд',
          'schedule':'Расписание группы',
          'latest_news':'Важные новости группы',
          'random_people':'Рандом среди списка определенных людей',
          'add_queue':'Добавление в очередь',
          'queue_see':'Просмотр очереди',
          'change_queue':'Изменения номера в очереди',
          'add_randomlist':'Добавления людей для рандома',
          'worker':'Кто сегодня дежурный?',
          'queue':'Создание очереди',
          'check_number':'Просмотр свободных номеров',
          'exit':'Обновления файлов',
          'random_see':'Просмотр списка рандома'}
#создание клавиатуры 
#bot.send_message(reply_markup=)
#class User:
    #def __init__(self,name)
        #self.name=name
        #self.
#imageSelect=types.ReplyKeyboardMarkup(one_time_keyboard=True)
#imageSelect.add('start','help','schedule','latest_news')
#hideBoard=types.ReplyKeyboardRemove()
# функция регестрации юзера
##########################

###############################################################    
def get_user_step(uid):
    if uid in userstep:
        return userstep[uid]
    else:
        knownUsers.append(uid)
        userstep[uid]=0
        print("New user detected, who hasn't used \"/start\" yet")
        return 0
# функция для проверки пользователей(только для консоли)
def listener(message):
    for m in message:
        if m.content_type=='text':
            last_text=m.text
            print(str(m.chat.first_name)+"["+str(m.chat.id)+"]:"+m.text) 
            return last_text             
bot=telebot.TeleBot(config.token)
#регестрируем пользователя
bot.set_update_listener(listener)
#обработка команды /start
@bot.message_handler(commands=['start'])
def commands_start(m):
    cid=m.chat.id
    if cid not in knownUsers:
        knownUsers.append(cid) # добавляем пользователя в список
        msg=bot.send_message(cid,"Введите свою фамилию и имя")
        bot.register_next_step_handler(msg,scan)
    else:
        bot.send_message(cid,"I already know you, no need for me to scan you again!")
def scan(message):
    name=str(message.chat.first_name)+str(message.chat.last_name)
    cid=message.chat.id
    text=message.text
    if os.path.isfile('files\crew.txt'):
        with open('files\crew.txt','a') as f:
            f.write(str(text)+':'+name +'\n')
    else:
        with open('files\crew.txt','w') as f:
            f.write(str(text) + ':'+ name +'\n')
    bot.send_message(cid,'Здравствуйте '+text+'!')
    command_help(message) # отображем новому пользователю help page
# команда help
@bot.message_handler(commands=['help'])
def command_help(m):
    cid=m.chat.id
    help_text="The following commands are available: \n"
    for key in commands:
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid,help_text)
# функция расписания группы
@bot.message_handler(commands=['schedule']) 
def command_schedule(m):
    cid=m.chat.id
    files=open('files\schedule.txt','r')
    information=files.read()
    files.close()
    bot.send_message(cid,information)
@bot.message_handler(commands=['random_see']) 
def command_random_see(m):
    cid=m.chat.id
    files=open('files\people_random.txt','r')
    information=files.read()
    files.close()
    bot.send_message(cid,information)
# команда для вывода важных новостей
@bot.message_handler(commands=['latest_news']) 
def command_latest_news(m):
    cid=m.chat.id
    files=open('files\latest_news.txt','r')
    information=files.read()
    files.close()
    bot.send_message(cid,information)
# команда создания очереди
@bot.message_handler(commands=['queue']) 
def command_queue(m):
    cid=m.chat.id
    files=open('files\queue.txt','w')
    files.close()
    bot.send_message(cid,'Очередь создана')
#команда просмотра очереди
@bot.message_handler(commands=['queue_see']) 
def command_queue_see(m):
    if os.path.isfile('files\queue.txt'):
        cid=m.chat.id
        files=open('files\queue.txt','r')
        information=files.read()
        files.close()
        bot.send_message(cid,information)
    else:
        bot.send_message(m.chat.id,'Очередь не создана. Обратитесь к администратору')  
#команда добавление в очередь    
@bot.message_handler(commands=['add_queue'])
def random_p(m):
    bot.send_message(m.chat.id,'Здравствуйте уважаемый'+'\t'+str(m.chat.first_name)+str(m.chat.last_name))
    if os.path.isfile('files\queue.txt'):
        msg=bot.send_message(m.chat.id,'Какое место вы желаете в очереди')
        bot.register_next_step_handler(msg,number)
    else:
        bot.send_message(m.chat.id,'Очередь не создана. Обратитесь к администратору')
def number(message):
    name=str(message.chat.first_name)+str(message.chat.last_name)
    text=message.text
    if not text.isdigit():
        msg=bot.reply_to(message,'Место в очереди должно быть только числом. Какое место вы желаете в очереди')  
        bot.register_next_step_handler(msg,number) 
    with open('files\crew.txt') as f:
        content=f.readlines()
    content=[x.strip() for x in content]
    for x in content:
        if name in x:
            s=x.split(':')
            print(s)
            s.remove(name)
    with open('files\mumber.txt') as f:
        info=f.readlines()
    info=[x.strip() for x in info]
    if text in info:
        files=open('files\queue.txt','a')  
        files.write(str(*s) + '-'+text + '\n')
        files.close()
        bot.send_message(message.chat.id,'Вы успешно были добавлены в очередь с номером'+'\t'+text)
        bot.send_message(message.chat.id,'Для того чтобы посмотреть всю очередь воспользуйтесь командой /queue_see')
        with open("files\mumber.txt", "w") as f:
            for line in info:
                if text != line.strip('\n'):
                    f.write(line+'\n')
    else:
        msg=bot.reply_to(message,'Место занято. Введите другое число')  
        bot.register_next_step_handler(msg,number) 
#команда смены номера в очереди
@bot.message_handler(commands=['change_queue'])
def change_queue_command(message):
    name=str(message.chat.first_name)+str(message.chat.last_name)
    if os.path.isfile('files\queue.txt'):
        bot.send_message(message.chat.id,'Здравствуйте уважаемый'+'\t'+str(message.chat.first_name)+str(message.chat.last_name))
        with open('files\crew.txt') as f:
            content=f.readlines()
        content=[x.strip() for x in content]
        for x in content:
            if name in x:
                s=x.split(':')
                print(s)
                s.remove(name)
        with open('files\queue.txt') as f:
            content=f.readlines()
        content=[x.strip() for x in content]
        for x in content:
            if str(*s) in x:
                bot.send_message(message.chat.id,'Ваше место в очереди : '+x)
        msg=bot.send_message(message.chat.id,'На какое место осуществить замену')
        bot.register_next_step_handler(msg,change)
    else:
        bot.send_message(m.chat.id,'Очередь не создана. Обратитесь к администратору')  
def change(message):
    name=str(message.chat.first_name)+str(message.chat.last_name)
    text=message.text
    if not text.isdigit():
        msg=bot.reply_to(message,'Место в очереди должно быть только числом. Какое место вы желаете в очереди')  
        bot.register_next_step_handler(msg,change) 
    with open('files\crew.txt') as f:
        content=f.readlines()
    content=[x.strip() for x in content]
    for x in content:
        if name in x:
            s=x.split(':')
            print(s)
            s.remove(name)
    with open('files\mumber.txt') as f:
        info=f.readlines()
    info=[x.strip() for x in info]
    if text in info:
        with open("files\queue.txt", "r") as f:
            lines = f.readlines()
        with open("files\queue.txt", "w") as f:
            for line in lines:
                if str(*s) not in line.strip('\n'):
                    f.write(line+'\n')
        files=open('files\queue.txt','a')  
        files.write(str(*s) + '-'+text + '\n')
        files.close()
        with open("files\mumber.txt", "w") as f:
            for line in info:
                if text != line.strip('\n'):
                    f.write(line+'\n')
        bot.send_message(message.chat.id,'Ваше место обновлено. Для того чтобы посмотреть очередь используете команду /queue_see')
    else:
        msg=bot.reply_to(message,'Место занято. Введите другое число')  
        bot.register_next_step_handler(msg,change)
################################################
# команда добавления людей в список для рандома
@bot.message_handler(commands=['add_randomlist'])
def add_people_command(message):
    name=str(message.chat.first_name)+str(message.chat.last_name)
    with open('files\crew.txt') as f:
        content=f.readlines()
    content=[x.strip() for x in content]
    for x in content:
        if name in x:
            s=x.split(':')
            print(s)
            s.remove(name)
    with open('files\people_random.txt','a') as f:
        f.write(str(*s)+'\n')
    bot.send_message(message.chat.id,'Вы успешно были добавлены в список')    
# команда выбора определенных из списка
@bot.message_handler(commands=['random_people'])
def randem(message):
    bot.send_message(message.chat.id,'Список человек участвующих в рандоме : ')
    files=open('files\people_random.txt','r')
    information=files.read()
    files.close()
    bot.send_message(message.chat.id,information)
    with open("files\people_random.txt", "r") as f:
        lines = f.readlines()
    lines=[x.strip() for x in lines]
    ran=random.choice(lines)
    bot.send_message(message.chat.id,'Победитель : '+ran)
    if os.path.getsize("files\people_random.txt")>0:
        with open("files\people_random.txt", "r") as f:
            lines = f.readlines()
        with open("files\people_random.txt", "w") as f:
            for line in lines:
                if ran != line.strip('\n'):
                    f.write(line+'\n')
    else:
        bot.send_message(message.chat.id,'Файл пуст')
# команда выявления дежурного
@bot.message_handler(commands=['worker'])
def work(message):
    with open('files\schook.txt') as f:
        content=f.readlines()
    content=[x.strip() for x in content]
    print(content)
    now=datetime.datetime.now()
    bot.send_message(message.chat.id,'Дежурный под номером : '+str(content[now.day-1]))
@bot.message_handler(commands=['check_number'])
def check(message):
    cid=message.chat.id
    files=open('files\mumber.txt','r')
    information=files.readlines()
    files.close()
    information=[x.strip() for x in information]
    bot.send_message(cid,'Свободные номера :'+'\t'+str(information))
@bot.message_handler(commands=['exit'])
def stop(message):
    files=open('files\people_random.txt','w').close()
    os.remove('files\queue.txt')
    with open('files\mumber.txt','w') as f:
        for x in range(1,31):
            f.write(str(x) +'\n')
    bot.send_message(message.chat.id,'Работа завершена. Файлы обновлены')
bot.polling(none_stop=True)