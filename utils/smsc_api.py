# -*- coding: utf-8 -*-
# SMSC.RU API (smsc.ru) версия 1.7 (08.06.2012)
# Отрефакторено. Краснов Дмитрий 16.10.2014

from datetime import datetime
from time import sleep
import smtplib

try:
    from urllib import urlopen, quote
except ImportError:
    from urllib.request import urlopen
    from urllib.parse import quote


def ifs(cond, val1, val2):
    """Вспомогательная функция, эмуляция тернарной операции ?:"""

    if cond:
        return val1
    return val2


class SMSC(object):
    """Класс для взаимодействия с сервером smsc.ru"""

    def __init__(self, login='login', password='password', post=False, https=False,
                 charset='utf-8', debug=False, smtp_from='api@smsc.ru', smtp_server='send.smsc.ru',
                 smtp_login='', smtp_password=''):

        # Константы для настройки библиотеки
        self.smsc_login = login  # логин клиента
        self.smsc_password = password   # пароль или MD5-хеш пароля в нижнем регистре
        self.smsc_post = post  # использовать метод POST
        self.smsc_https = https  # использовать HTTPS протокол
        self.smsc_charset = charset  # кодировка сообщения (windows-1251 или koi8-r), по умолчанию используется utf-8
        self.smsc_debug = debug   # флаг отладки

        # Константы для отправки SMS по SMTP
        self.smtp_from = smtp_from  # e-mail адрес отправителя
        self.smtp_server = smtp_server  # адрес smtp сервера
        self.smtp_login = smtp_login  # логин для smtp сервера
        self.smtp_password = smtp_password  # пароль для smtp сервера

    def send_sms(self, phones, message, translit=0, time="", id=0, format=0, sender=False, query=""):
        """Метод отправки SMS
        обязательные параметры:
        phones - список телефонов через запятую или точку с запятой
        message - отправляемое сообщение

        необязательные параметры:
        translit - переводить или нет в транслит (1,2 или 0)
        time - необходимое время доставки в виде строки (DDMMYYhhmm, h1-h2, 0ts, +m)
        id - идентификатор сообщения. Представляет собой 32-битное число в диапазоне от 1 до 2147483647.
        format - формат сообщения (0 - обычное sms, 1 - flash-sms, 2 - wap-push, 3 - hlr, 4 - bin, 5 - bin-hex, 6 - ping-sms)
        sender - имя отправителя (Sender ID). Для отключения Sender ID по умолчанию необходимо в качестве имени
        передать пустую строку или точку.
        query - строка дополнительных параметров, добавляемая в URL-запрос ("valid=01:00&maxsms=3")

        возвращает массив (<id>, <количество sms>, <стоимость>, <баланс>) в случае успешной отправки
        либо массив (<id>, -<код ошибки>) в случае ошибки"""

        formats = ["flash=1", "push=1", "hlr=1", "bin=1", "bin=2", "ping=1"]
        m = self._smsc_send_cmd("send", "cost=3&phones=" + quote(phones) + "&mes=" + quote(message) + \
                                "&translit=" + str(translit) + "&id=" + str(id) + ifs(format > 0,
                                                                                      "&" + formats[format - 1], "") + \
                                ifs(sender == False, "", "&sender=" + quote(str(sender))) + \
                                ifs(time, "&time=" + quote(time), "") + ifs(query, "&" + query, ""))

        # (id, cnt, cost, balance) или (id, -error)

        if self.smsc_debug:
            if m[1] > "0":
                print("Сообщение отправлено успешно. ID: " + m[0] + ", всего SMS: " + m[1] + ", стоимость: " + m[
                    2] + ", баланс: " + m[3])
            else:
                print("Ошибка №" + m[1][1:] + ifs(m[0] > "0", ", ID: " + m[0], ""))

        return m

    def send_sms_mail(self, phones, message, translit=0, time="", id=0, format=0, sender=""):
        """SMTP версия метода отправки SMS"""

        server = smtplib.SMTP(self.smtp_server)

        if self.smsc_debug:
            server.set_debuglevel(1)

        if self.smtp_login:
            server.login(self.smtp_login, self.smtp_password)

        server.sendmail(self.smtp_from, "send@send.smsc.ru", "Content-Type: text/plain; charset=" + self.smsc_charset + "\n\n" + \
                        self.smsc_login + ":" + self.smsc_password + ":" + str(id) + ":" + time + ":" + str(translit) + "," + \
                        str(format) + "," + sender + ":" + phones + ":" + message)
        server.quit()

    def get_sms_cost(self, phones, message, translit=0, format=0, sender=False, query=""):
        """Метод получения стоимости SMS
        обязательные параметры:
        phones - список телефонов через запятую или точку с запятой
        message - отправляемое сообщение

        необязательные параметры:
        translit - переводить или нет в транслит (1,2 или 0)
        format - формат сообщения (0 - обычное sms, 1 - flash-sms, 2 - wap-push, 3 - hlr, 4 - bin, 5 - bin-hex, 6 - ping-sms)
        sender - имя отправителя (Sender ID)
        query - строка дополнительных параметров, добавляемая в URL-запрос ("list=79999999999:Ваш пароль: 123\n78888888888:Ваш пароль: 456")

        возвращает массив (<стоимость>, <количество sms>) либо массив (0, -<код ошибки>) в случае ошибки"""

        formats = ["flash=1", "push=1", "hlr=1", "bin=1", "bin=2", "ping=1"]
        m = self._smsc_send_cmd("send", "cost=1&phones=" + quote(phones) + "&mes=" + quote(message) + \
                                ifs(sender == False, "", "&sender=" + quote(str(sender))) + \
                                "&translit=" + str(translit) + ifs(format > 0, "&" + formats[format - 1], "") + ifs(
            query, "&" + query, ""))

        # (cost, cnt) или (0, -error)

        if self.smsc_debug:
            if m[1] > "0":
                print("Стоимость рассылки: " + m[0] + ". Всего SMS: " + m[1])
            else:
                print("Ошибка №" + m[1][1:])

        return m

    def get_status(self, id, phone, all=0):
        """Метод проверки статуса отправленного SMS или HLR-запроса
        id - ID cообщения
        phone - номер телефона

        возвращает массив:
        для отправленного SMS (<статус>, <время изменения>, <код ошибки sms>)
        для HLR-запроса (<статус>, <время изменения>, <код ошибки sms>, <код IMSI SIM-карты>, <номер сервис-центра>, <код страны регистрации>,
        <код оператора абонента>, <название страны регистрации>, <название оператора абонента>, <название роуминговой страны>,
        <название роумингового оператора>)

        При all = 1 дополнительно возвращаются элементы в конце массива:
        (<время отправки>, <номер телефона>, <стоимость>, <sender id>, <название статуса>, <текст сообщения>)

        либо массив (0, -<код ошибки>) в случае ошибки"""

        m = self._smsc_send_cmd("status", "phone=" + quote(phone) + "&id=" + str(id) + "&all=" + str(all))

        # (status, time, err, ...) или (0, -error)

        if self.smsc_debug:
            if m[1] >= "0":
                tm = ""
                if m[1] > "0":
                    tm = str(datetime.fromtimestamp(int(m[1])))
                print("Статус SMS = " + m[0] + ifs(m[1] > "0", ", время изменения статуса - " + tm, ""))
            else:
                print("Ошибка №" + m[1][1:])

        if all and len(m) > 9 and (len(m) < 14 or m[14] != "HLR"):
            m = (",".join(m)).split(",", 8)

        return m

    def get_balance(self):
        """Метод получения баланса
        без параметров

        возвращает баланс в виде строки или False в случае ошибки"""

        m = self._smsc_send_cmd("balance")  # (balance) или (0, -error)

        if self.smsc_debug:
            if len(m) < 2:
                print("Сумма на счете: " + m[0])
            else:
                print("Ошибка №" + m[1][1:])

        return ifs(len(m) > 1, False, m[0])

    def _smsc_send_cmd(self, cmd, arg=""):
        """Метод вызова запроса. Формирует URL и делает 3 попытки чтения"""

        url = ifs(self.smsc_https, "https", "http") + "://smsc.ru/sys/" + cmd + ".php"
        arg = "login=" + quote(self.smsc_login) + "&psw=" + quote(
            self.smsc_password) + "&fmt=1&charset=" + self.smsc_charset + "&" + arg

        i = 0
        ret = ""

        while ret == "" and i < 3:
            if i > 0:
                sleep(2)

            if i == 2:
                url = url.replace("://smsc.ru/", "://www2.smsc.ru/")

            try:
                if self.smsc_post or len(arg) > 2000:
                    data = urlopen(url, arg.encode(self.smsc_charset))
                else:
                    data = urlopen(url + "?" + arg)

                ret = str(data.read())
            except:
                ret = ""

            i += 1

        if ret == "":
            if self.smsc_debug:
                print("Ошибка чтения адреса: " + url)
            ret = ","  # фиктивный ответ

        return ret.split(",")


# Examples:
if __name__ == '__min__':
    smsc = SMSC(login='solarispromo', password='40cbe6860ee7014fdc2d9f5800c6dc70')
    # smsc.send_sms("79999999999", "test", sender="sms")
    # smsc.send_sms("79999999999", "http://smsc.ru\nSMSC.RU", query="maxsms=3")
    # smsc.send_sms("79999999999", "0605040B8423F0DC0601AE02056A0045C60C036D79736974652E72750001036D7973697465000101", format=5)
    # smsc.send_sms("79999999999", "", format=3)
    # r = smsc.get_sms_cost("79999999999", "Вы успешно зарегистрированы!")
    # smsc.send_sms_mail("79999999999", "test2", format=1)
    # r = smsc.get_status(12345, "79999999999")
    print(smsc.get_balance())
