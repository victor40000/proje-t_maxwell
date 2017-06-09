from matplotlib import pyplot
import numpy as np
from tkinter import *
import math
import sys
import telebot
import time

access_token = "375480588:AAHh6kF7AoRpMgpcqykEzzwrmUEGWxl0EnE"
bot = telebot.TeleBot(access_token)
pi = math.pi
k = 1.3807 #-23
e = 2.7182818284
n = 6.022140 #23
v_kv = 0
v_ver = 0 
v_srar = 0
m = -1
t = -1
R = 8.3144598 
rt = 0
lt = 0
ver_m = 0
ver_m1 = 0
mid = 0
flag = False
root = Tk()
root.geometry('450x300+0+0')
root.title('Распределение Максвелла')
but = Button(root, font=(170))
ent_m = Entry(root, bd=3, font=(170))
ent_t = Entry(root, width=20, bd=3, font=(50))
ent_lt = Entry(root, bd=3, font=(170))
ent_rt = Entry(root, width=20, bd=3, font=(50))

lbl_m = Label(root, width=20, font=(270))
lbl_t = Label(root, width=20, font=(50))
lbl_kv = Label(root, width=20, font=(50), fg="red")
lbl_ver = Label(root, width=20, font=(50), fg="blue")
lbl_srar = Label(root, width=20, font=(50), fg="green")
lbl_ver_m = Label(root, width=20, font=(50), fg="dark orange")
lbl_ver_m1 = Label(root, width=20, font=(50), fg="dark orange")
lbl_lt = Label(root, width=20, font=(50))
lbl_rt = Label(root, width=20, font=(50))


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hello, here you can calculate important values of Maxwell distribution and create plots. Type /help for more details")


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "/get_mp_speed mass temperature - calculates the most probable speed of molecules")
    bot.send_message(message.chat.id, "/get_av_speed mass temperature - calculates the average speed of molecules")
    bot.send_message(message.chat.id, "/get_sq_speed mass temperature - calculates the root-mean-square speed of molecules")
    bot.send_message(message.chat.id, "/get_chance mass temperature speed_1 speed_2 - calculates the chance, that speed of molecule is between speed_1 and speed_2")
    bot.send_message(message.chat.id, "/get_plots mass temperature speed_1 speed_2 - creates plots of maxwell function (2 views)")
    bot.send_message(message.chat.id, "measure units: mass[g/mole], temperature[K], speed[m/s]")


@bot.message_handler(commands=['get_mp_speed'])
def get_mp(message):
    if len(message.text.split()) != 3:
        bot.send_message(message.chat.id, 'Wrong number of arguments. Use /help to see details')
        return
    m = int(message.text.split()[1])
    t = int(message.text.split()[2])
    if m <= 0 or t <= 0:
        bot.send_message(message.chat.id, 'Wrong arguments. Use /help to see details')
        return
    v_ver = get_ver(m, t)
    bot.send_message(message.chat.id, str(v_ver))


@bot.message_handler(commands=['get_av_speed'])
def get_av(message):
    if len(message.text.split()) != 3:
        bot.send_message(message.chat.id, 'Wrong number of arguments. Use /help to see details')
        return
    m = int(message.text.split()[1])
    t = int(message.text.split()[2])
    if m <= 0 or t <= 0:
        bot.send_message(message.chat.id, 'Wrong arguments. Use /help to see details')
        return
    v_srar = get_srar(m, t)
    bot.send_message(message.chat.id, str(v_srar))


@bot.message_handler(commands=['get_sq_speed'])
def get_sq(message):
    if len(message.text.split()) != 3:
        bot.send_message(message.chat.id, 'Wrong number of arguments. Use /help to see details')
        return
    m = int(message.text.split()[1])
    t = int(message.text.split()[2])
    if m <= 0 or t <= 0:
        bot.send_message(message.chat.id, 'Wrong arguments. Use /help to see details')
        return
    v_kv = get_kv(m, t)
    bot.send_message(message.chat.id, str(v_kv))


@bot.message_handler(commands=['get_chance'])
def get_chace(message):
    if len(message.text.split()) != 5:
        bot.send_message(message.chat.id, 'Wrong number of arguments. Use /help to see details')
        return
    m = int(message.text.split()[1])
    t = int(message.text.split()[2])
    lt = int(message.text.split()[3])
    rt = int(message.text.split()[4])
    if lt > rt or m <= 0 or t <= 0:
        bot.send_message(message.chat.id, 'Wrong arguments. Use /help to see details')
        return
    ver_m = ( (f_integral(m, t, rt) - f_integral(m, t, lt)) / f_integral(m, t, 10000000000000000) )
    ver_m1 = maksvell_mod(lt + (rt - lt)/2) * (rt - lt)
    bot.send_message(message.chat.id, "analyt: {}".format(str(ver_m)))
    bot.send_message(message.chat.id, "av: {}".format(str(ver_m1)))
    


@bot.message_handler(commands=['get_plots'])
def get_plots(message):
    if len(message.text.split()) != 5:
        bot.send_message(message.chat.id, 'Wrong number of arguments. Use /help to see details')
        return
    global m, t, lt, rt, v_ver, v_kv, v_srar, flag
    m = int(message.text.split()[1])
    t = int(message.text.split()[2])
    lt = int(message.text.split()[3])
    rt = int(message.text.split()[4])
    if lt > rt or m <= 0 or t <= 0:
        bot.send_message(message.chat.id, 'Wrong arguments. Use /help to see details')
        return
    v_ver = get_ver(m, t)
    v_kv = get_kv(m, t)
    v_srar = get_srar(m, t)
    global mid
    mid = message.chat.id
    flag = True
    bot.stop_polling()
    
    







def create_figure(show, m, t, lt, rt, v_ver, v_kv, v_srar): 
        val = []
        vel = []
        ver = []
        srar = []
        kv = []
        pyplot.figure('f1')
        pyplot.ylabel('f(v)')
        pyplot.xlabel('v')
        pyplot.title('Функция распределения Максвелла по модулям скоростей')
        count = []
        step = maksvell_mod(v_ver) / 1000
        for i in range(1000):
            v = i * step
            ver.append(v) 
            count.append(v_ver)
        pyplot.plot(count, ver, 'b--')

        count = []
        step = maksvell_mod(v_kv) / 1000
        for i in range(1000):
            v = i * step
            kv.append(v) 
            count.append(v_kv)
        pyplot.plot(count, kv, 'r--')

        count = []
        step = maksvell_mod(v_srar) / 1000
        for i in range(1000):
            v = i * step
            srar.append(v) 
            count.append(v_srar)
        pyplot.plot(count, srar, 'g--')



        step = v_ver / 10000
        for i in range(60000):
            v = i * step
            val.append(maksvell_mod(v)) 
            vel.append(v)
        pyplot.plot(vel, val, 'black', markersize=20)


        count = []
        count1 = []
        step = v_ver / 10000
        for i in range(60000):
            v = i * step
            count1.append(0) 
            count.append(v)
        pyplot.plot(count, count1, 'black')


        count = []
        count1 = []
        step = maksvell_mod(v_ver) / 1000
        for i in range(1000):
            v = i * step
            count1.append(v) 
            count.append(0)
        pyplot.plot(count, count1, 'black')



        count = []
        count1 = []
        step = maksvell_mod(rt) / 1000
        for i in range(1000):
            v = i * step
            count1.append(v) 
            count.append(rt)
        pyplot.plot(count, count1, 'orange')

        count = []
        count1 = []
        step = maksvell_mod(lt) / 1000
        for i in range(1000):
            v = i * step
            count1.append(v) 
            count.append(lt)
        pyplot.plot(count, count1, 'orange')

        count = []
        count1 = []
        step = (rt - lt) / 1000
        for i in range(1000):
            v = lt + i * step
            count1.append(v) 
            count.append(0)
        pyplot.plot(count1, count, 'orange')

        count = []
        count1 = []
        step = (rt - lt) / 1000
        for i in range(1000):
            v = lt + i * step
            count1.append(v) 
            count.append(maksvell_mod(lt + i * step))
        pyplot.plot(count1, count, 'orange')
        pyplot.savefig('f1.png')
       

        pyplot.figure('f2')
        pyplot.ylabel('f(v)')
        pyplot.xlabel('v')
        pyplot.title('Функция распределения Максвелла в неприведенном виде')

        val = []
        vel = []
        step = v_ver / 10000
        for i in range(-30000, 30000, 1):
            v = i * step
            val.append(maksvell_komp(v)) 
            vel.append(v)
        pyplot.plot(vel, val, 'black', markersize=20)

        count = []
        count1 = []
        step = maksvell_komp(0) / 1000
        for i in range(1030):
            v = i * step
            count1.append(v) 
            count.append(0)
        pyplot.plot(count, count1, 'black')

        val = []
        vel = []
        step = v_ver / 10000
        for i in range(-30000, 30000, 1):
            v = i * step
            val.append(0) 
            vel.append(v)
        pyplot.plot(vel, val, 'black', markersize=20)

        pyplot.savefig('f2.png')
        if show != True:
            pyplot.clf()
            pyplot.figure('f1')
            pyplot.clf()
        if show == True:
            pyplot.show()
            



def on_button1(event):
    if ent_m.get() != '' and ent_t.get() != '' and ent_rt.get() != '' and ent_lt.get() != '':
        global v_ver, v_kv, v_srar, m, t, lt, rt, ver_m, ver_m1
        if int(ent_m.get()) > 0:
            m = int(ent_m.get())*10/n
        else:
            return
        if int(ent_t.get()) >= 0:
            t = int(ent_t.get())
        else:
            return
        if int(ent_rt.get()) > int(ent_lt.get()) and int(ent_lt.get()) >= 0 :
            lt = int(ent_lt.get())
            rt = int(ent_rt.get())
        v_ver = get_ver(m, t)
        v_kv = get_kv(m, t)
        v_srar = get_srar(m, t)
        ver_m = ( (f_integral(m, t, rt)-f_integral(m, t, lt))/f_integral(m, t, 10000000000000000) )
        ver_m1 = maksvell_mod(lt + (rt - lt)/2) * (rt - lt)

        lbl_kv["text"] = "v(ср.кв) = {v}".format(v = round(v_kv, 3))
        lbl_ver["text"] = "v(вер) = {v}".format(v = round(v_ver, 3))
        lbl_srar["text"] = "v(ср.ар) = {v}".format(v = round(v_srar, 3))
        lbl_ver_m["text"] = "Вероятность(аналит.) = {v}".format(v = round(ver_m, 3))
        lbl_ver_m1["text"] = "Вероятность(средн.) = {v}".format(v = round(ver_m1, 3))
        create_figure(True, m, t, lt, rt, v_ver, v_kv, v_srar)
        


def maksvell_mod(v):
    res = (4*pi) * ((math.sqrt(m/(2*k*t*pi*10000)))**3) * (v**2) * (e**(-(m*v**2)/(2*k*t*10000)))
    return res


def maksvell_komp(v):
    res = ((math.sqrt(m/(2*k*t*pi*10000)))**3) * (e**(-(m*v**2)/(2*k*t*10000)))
    return res



def f_integral(mass, temp, v): 
    k = 1.38 * 10 ** -23 
    mass = mass / 10**27
    term1 = (math.pi / 2) ** (1/2) * (k * temp / mass) ** (3/2) * math.erf(mass ** (1/2) * v / (2 * k * temp) ** (1/2)) 
    term2 = k * temp * v * math.e ** (-mass * v ** 2 / (2 * k * temp)) / mass 
    f = 2 ** (1/2) * math.pi * (mass / (math.pi * k * temp)) ** (3 / 2) * (term1 - term2) 
    return f


def get_ver(m, t): 
    x = 20000 * k * t / m
    return math.sqrt(x)


def get_srar(m, t):
    x = 22500 * k * t / m
    return math.sqrt(x)

def get_kv(m, t):
    x = 30000 * k * t / m
    return math.sqrt(x)


def create_ui():



    but["text"] = "Построить график"

    lbl_m["text"] = "Масса молекулы(г/моль)"
    lbl_t["text"] = "Температура (К)"
    lbl_lt["text"] = "v1(м/с)"
    lbl_rt["text"] = "v2(м/с)"
    lbl_kv["text"] = "v(ср.кв) = {v}".format(v = v_kv)
    lbl_ver["text"] = "v(вер) = {v}".format(v = v_ver)
    lbl_srar["text"] = "v(ср.ар) = {v}".format(v = v_srar)
    lbl_ver_m["text"] = "Вероятность(аналит.) = {v}".format(v = round(ver_m, 3))
    lbl_ver_m1["text"] = "Вероятность(средн.) = {v}".format(v = round(ver_m1, 3))

    but.bind("<Button-1>", on_button1)

    but.place(x = 45, y = 255, width = 150)

    ent_m.place(x = 45, y = 35, width = 120)
    ent_t.place(x = 45, y = 95, width = 120)
    ent_lt.place(x = 45, y = 155, width = 120)
    ent_rt.place(x = 45, y = 215, width = 120)

    lbl_m.place(x = 25, y = 5, width = 250)
    lbl_t.place(x = 5, y = 65, width = 200)
    lbl_lt.place(x = 5, y = 125, width = 200)
    lbl_rt.place(x = 5, y = 185, width = 200)
    lbl_kv.place(x = 210, y = 70, width = 180)
    lbl_ver.place(x = 210, y = 100, width = 180)
    lbl_srar.place(x = 210, y = 130, width = 180)
    lbl_ver_m.place(x = 160, y = 160, width = 290)
    lbl_ver_m1.place(x = 160, y = 190, width = 310)
    root.mainloop() 




if len(sys.argv) == 1:
    create_ui()
if len(sys.argv) == 2:
    if sys.argv[1] == 'run':

        while True:
            bot.polling(none_stop=True, timeout = 0)
            time.sleep(1)
            if flag == True:
                create_figure(False, m, t, lt, rt, v_ver, v_kv, v_srar)
                bot.send_photo(mid, photo=open('f2.png', 'rb'))
                bot.send_photo(mid, photo=open('f1.png', 'rb'))
                flag = False
                time.sleep(5)





