import threading as th
import time
import schedule
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from package.vk_token import token
from package.get_msgs import msgs
from package.change_users_info import change_user_info
from package.read_excel import schedule_time, groups_info
authorize = vk_api.VkApi(token = token)
longpoll = VkLongPoll(authorize)

def write_msg(sender, msg, keyboard):
    authorize.method('messages.send', {'user_id': sender, 'message': msg, 'random_id': get_random_id(), 'keyboard': keyboard.get_keyboard()})

def generate_keyboard(keyboard, buttons, next_lines):
    i = 0
    for command, color in buttons.items():
        i += 1
        keyboard.add_button(command, color=color)
        if (i % next_lines == 0 and i != len(buttons)):
            keyboard.add_line()
    return keyboard

def maling(): #add users n msgs n keyboard
    print('started')
    while True:
        schedule.run_pending()
        time.sleep(60)
schedule.every().day.at("19:00", "Europe/Moscow").do(lambda: write_msg(sender='376386974', msg='231231', keyboard=generate_keyboard(VkKeyboard(one_time=True), {'11': VkKeyboardColor.PRIMARY}, 1)))

malingTh = th.Thread(target=maling)
malingTh.start()
PRIMARY = VkKeyboardColor.PRIMARY
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        reseived_msg = event.text.lower()
        sender = event.user_id
        msg = 'Неизвестная команда'
        main_vk_keyboard = VkKeyboard(one_time=True)
        buttons = {}
        next_lines = 2

        if reseived_msg == 'начать':
            msg = '\n'.join(msgs['start'])
        if reseived_msg == 'команды':
            msg = '\n'.join(msgs['commands'])
        if reseived_msg == 'расписание':
            msg = '\n'.join(msgs['schedule'])
            buttons['По группе'] = PRIMARY
            buttons['По преподователю'] = PRIMARY
            buttons['Рассылка расписания'] = PRIMARY
            buttons['Вернуться в меню'] = PRIMARY
        if reseived_msg == 'по группе':
            for key in groups_info.keys():
                buttons[key] = PRIMARY
        if reseived_msg == 'по преподователю':
            teachers = []
            for value in groups_info.values():
                for value2 in value:
                    for value3 in value2:
                        if value3 is not None:
                            teachers.append(value3[1])
                            if len(value3) == 4:
                                teachers.append(value3[3])
            teachers = set(teachers)
            for teacher in teachers:
                buttons[teacher] = PRIMARY
        if reseived_msg == 'рассылка расписания':
            msg = '\n'.join(msgs['maling'])
            buttons['Выбрать класс рассылки'] = PRIMARY
            buttons['Отключить рассылку'] = PRIMARY
        if reseived_msg == 'выбрать класс рассылки':
            msg = '\n'.join(msgs['choose_class'])
            for key in groups_info.keys():
                buttons[key] = PRIMARY
        if reseived_msg == 'отключить рассылку':
            change_user_info(uid=sender, new_status='none')
            msg = '\n'.join(msgs['deactivate_maling'])
        if reseived_msg == 'вернуться в меню':
            msg = '\n'.join(msgs['return'])
            
        if len(buttons) == 0:
            buttons['расписание'] = PRIMARY
            buttons['команды'] = PRIMARY
            next_lines = 1

        main_vk_keyboard = generate_keyboard(main_vk_keyboard, buttons, next_lines)
        write_msg(sender=sender, msg=msg, keyboard=main_vk_keyboard)

