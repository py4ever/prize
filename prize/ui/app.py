#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @PypiSeedTag: Main
# @Project : prize


"""
generated by PypiSeed(PPC) - Main Program
"""
import datetime
import threading
import time
import math
from random import *
from tkinter import *

from prize.ui.menu_setting import *
from prize.util.number import padding0
from prize.util.ui_placer import centralize, left, right

BG_COLOR = 'skyblue'

sample_label = "小白%s"
all_people = []
for i in range(10):
    all_people.append(sample_label % i)
PRIZE_META = {"values": all_people, "items": [], 'pickOnTime': -1, "terminated": False, "pickerWinOpen": False}

from tkinter.simpledialog import askstring


def schedule_picker(root: Tk = None):
    if PRIZE_META['pickerWinOpen']:
        mb.showwarning(POPUP_TITLE, "请勿重复操作，已打开定时窗口！")
        return
    secondary = Toplevel(master=root)
    right(secondary, root, 225, 93)
    clock_label = Label(secondary, background="tomato", relief="raised", borderwidth=3,
                        text=time.strftime('%Y-%m-%d\n%H:%M:%S', time.localtime(time.time())))
    toplevel_hook = IntVar(0)

    def update_clock():
        while toplevel_hook.get() == 0:
            if PRIZE_META['terminated']:
                return
            current_time = time.strftime('%Y-%m-%d\n%H:%M:%S', time.localtime(time.time()))
            clock_label.config(text=current_time)
            secondary.update()
            time.sleep(1)

    t = threading.Thread(target=update_clock)
    t.start()

    def on_closing():
        try:
            toplevel_hook.set(-1)
            secondary.destroy()
        finally:
            PRIZE_META['pickerWinOpen'] = False

    secondary.protocol("WM_DELETE_WINDOW", on_closing)
    hour_label = Label(secondary, background="tomato", text="时[0,23]：")
    min_label = Label(secondary, background="tomato", text="分[0,59]：")
    sec_label = Label(secondary, background="tomato", text="秒[0,59]：")
    hour_text = Text(secondary, background="skyblue", width=6, height=1)

    def handle_hour_keys(event):
        # print("event:", event)
        min_text.focus_force()

    def handle_min_keys(event):
        print("event:", event)
        sec_text.focus_force()

    def handle_sec_keys(event):
        # print("event:", event)
        hour_text.focus_force()

    hour_text.bind("<Tab>", handle_hour_keys)
    min_text = Text(secondary, background="skyblue", width=6, height=1)
    min_text.bind("<Tab>", handle_min_keys)
    sec_text = Text(secondary, background="skyblue", width=6, height=1)
    sec_text.bind("<Tab>", handle_sec_keys)
    hour_text.insert(0.0, "00")
    min_text.insert(0.0, "00")
    sec_text.insert(0.0, "00")

    def set_pick_time():
        hour = hour_text.get(1.0, END).strip()
        if not re.search("(^[0-1]{0,1}[0-9]$)|(^[2][0-3]$)", hour):
            print("Illegal input for hour：", hour)
            mb.showerror(POPUP_TITLE, "小时必须在0到23之内")
            return
        min = min_text.get(1.0, END).strip()
        if not re.search("^[0-5]{0,1}[0-9]$", min):
            print("Illegal input for min：", min)
            mb.showerror(POPUP_TITLE, "分钟必须在0到59之内")
            return
        sec = sec_text.get(1.0, END).strip()
        if not re.search("^[0-5]{0,1}[0-9]$", sec):
            print("Illegal input for second：", sec)
            mb.showerror(POPUP_TITLE, "秒数必须在0到59之内")
            return
        PRIZE_META['pickOnTime'] = padding0(hour) + ":" + padding0(min) + ":" + padding0(sec)
        print("PRIZE_META['pickOnTime']:", PRIZE_META['pickOnTime'])
        # secondary.destroy()

    confirm = Button(secondary, text="预约抽奖", fg="red", width=10,
                     command=set_pick_time)
    hour_label.grid(column=0, row=0, sticky=NSEW)
    hour_text.grid(column=1, row=0, sticky=NSEW)
    clock_label.grid(column=2, row=0, rowspan=3, sticky=NSEW)
    min_label.grid(column=0, row=1, sticky=NSEW)
    min_text.grid(column=1, row=1, sticky=NSEW)
    sec_label.grid(column=0, row=2, sticky=NSEW)
    sec_text.grid(column=1, row=2, sticky=NSEW)
    confirm.grid(column=0, row=3, columnspan=3, sticky=NSEW)
    PRIZE_META['pickerWinOpen'] = True
    secondary.rowconfigure(0, weight=1, pad=1)
    secondary.rowconfigure(1, weight=1, pad=1)
    secondary.rowconfigure(2, weight=1, pad=1)
    secondary.rowconfigure(3, weight=1, pad=1)
    secondary.columnconfigure(0, weight=1, pad=1)
    secondary.columnconfigure(1, weight=1, pad=1)
    secondary.columnconfigure(2, weight=1, pad=1)
    # secondary.mainloop()


def figure_table(size):
    col = 5
    row = size / 5
    if size % 5 != 0 and size != 0:
        row += 1
    return row, col


def render_labels_on_panel(paned_win: PanedWindow, root: Tk):
    all_items = PRIZE_META['items']
    all_items.clear()
    children = paned_win.children
    # print("existing children:", len(children))
    for item in children:
        paned_win.remove(item)
    children = paned_win.children
    # print("cleaned children:", len(children))
    children.clear()
    # print("cleaned children:", len(children))
    paned_win = PanedWindow(orient=VERTICAL, height=50, background=BG_COLOR)
    paned_win.grid(row=4, column=0, sticky=NSEW, columnspan=2)

    people = PRIZE_META['values']
    num = len(people)
    row, col = figure_table(num)
    # print("num:", num)
    # print("row %s , col %s" % (row, col))
    row_id = 0
    col_id = 0
    counter = 0
    relief = "sunken"
    relief = "raised"
    print("root width:", root.winfo_width())
    default_label_width = 11
    default_card_width = 120
    item_per_row = 5
    if len(people) >= 100:
        default_label_width = 6
        default_card_width = 60
        item_per_row = math.floor(root.winfo_width() / (default_card_width + 10)) - 1
    elif root.winfo_width() > 620:
        item_per_row = math.floor(root.winfo_width() / default_card_width + 10) - 1
    for p in people:
        counter += 1
        item = Label(paned_win, background="skyblue", borderwidth=3, \
                     relief=relief, width=default_label_width, text=p, padx=4, pady=2)
        all_items.append(item)
        paned_win.add(item)
        item.grid(row=row_id, column=col_id, sticky=NSEW)
        col_id += 1
        if counter % item_per_row == 0:
            row_id += 1
            col_id = 0
    root.update()


def focus_item(rand: int, total: int, trigger_button: Button, other_button: Button = None):
    all_items = PRIZE_META['items']

    def flash_red():
        # print("start flashing")
        data_list = [x for x in range(total)]
        shuffle(data_list)
        for x in data_list:
            item = all_items[x]
            item.configure(background='red')
            time.sleep(0.1)
            item.configure(background='skyblue')

    def handle_item(item: Label):
        item.focus()
        item.configure(background='red')
        item.update()
        try:
            winner = item.cget('text')
            print("winner is:", winner)
            # winner = "杜甫"
            mb.showinfo(POPUP_TITLE, "恭喜幸运个体【" + winner + "】！")
        except Exception as err:
            print("Fail to popup the winner info：%s" % str(err))

    try:
        each = all_items[rand]
        # print("each : ", each)
        flash_red()
        handle_item(each)
    finally:
        trigger_button.configure(state=NORMAL)
        if other_button:
            other_button.configure(state=NORMAL)
        print("end of processing")


"""
prize  ui
"""


class ChouJiang(object):
    def __init__(self, root):
        self.root = root

    def setup_root_win(self):
        self.root.title(POPUP_TITLE)
        # self.root.geometry('604x600')
        centralize(self.root, 604, 600)
        self.root.configure(bg=BG_COLOR)
        # self.root.resizable(0, 0)  # 阻止Python GUI的大小调整
        # 组件标签
        self.data_label = Label(self.root, background="tomato", text="参与抽奖全部个体")
        # 处理数据按钮
        self.generator_btn = Button(self.root, text="生成卡片", fg="red", width=10,
                                    command=self.render_text_into_cards)
        self.process_btn = Button(self.root, text="重新抽奖", fg="red", width=10,
                                  command=self.start_prize_picker)
        self.log_label = Label(self.root, background="tomato", borderwidth=1, text="黏贴抽奖人员名单")
        paned_win = PanedWindow(orient=VERTICAL)
        paned_win.configure(bg=BG_COLOR)
        self.paned_win = paned_win
        render_labels_on_panel(paned_win, self.root)
        # below resize event trigger will hang up the app
        # self.root.bind("<Configure>",lambda e: self.render_text_into_cards())
        # 文本展示框
        self.log_text = Text(self.root)

        def load_data_per_opt():
            opt = self.user_opt.get()
            # print("opt is ", opt)

        self.group = LabelFrame(self.root, text='提取ID卡片方式？', padx=1, pady=1)
        OPTS = [
            ("按行取ID", 0),
            ("按'ID:评论'提取ID", 1),
            ("按'ID：评论'提取ID", 2)]
        self.user_opt = IntVar()
        index = 0
        for opt, num in OPTS:
            b = Radiobutton(self.group, text=opt, variable=self.user_opt, value=num, command=load_data_per_opt)
            b.grid(row=0, column=index)
            index += 1
        self.log_text.insert(0.0, "<这里黏贴参与活动人员>")
        # 布局
        self.log_label.grid(row=0, column=0, columnspan=2, sticky=NSEW)
        # clock_label.grid(row=0, column=1, sticky=W + E)
        self.group.grid(row=1, column=0, columnspan=2, sticky=NSEW)
        self.log_text.grid(row=2, column=0, columnspan=2, sticky=NSEW)
        self.generator_btn.grid(row=3, column=0, sticky=NSEW)
        self.process_btn.grid(row=3, column=1, sticky=NSEW)
        self.data_label.grid(row=4, column=0, sticky=NSEW, columnspan=2)
        self.paned_win.grid(row=5, column=0, sticky=NSEW, columnspan=2)
        # self.root.rowconfigure(0, weight=1, pad=1)
        # self.root.rowconfigure(1, weight=1, pad=1)
        # self.root.rowconfigure(2, weight=1, pad=1)
        # self.root.rowconfigure(3, weight=1, pad=1)
        self.root.rowconfigure(4, weight=1, pad=1)
        self.root.columnconfigure(0, weight=1, pad=1)
        self.root.columnconfigure(1, weight=1, pad=1)
        t = threading.Thread(target=self.monitor_clock)
        t.start()

    def monitor_clock(self):
        while not PRIZE_META['terminated']:
            try:
                schedule_time = PRIZE_META['pickOnTime']
                min = 70
                hour = 26
                if re.search("^[0-9]{2}:[0-9]{2}:[0-9]{2}$", str(schedule_time)):
                    min = int(schedule_time.split(':')[1])
                    hour = int(schedule_time.split(':')[0])
                current = datetime.datetime.now()
                if abs(min - current.minute) > 2 or abs(hour - current.hour) > 2:
                    # print("Wait more time as clock is not closer")
                    time.sleep(2)
                # print("PRIZE_META['pickOnTime']:", PRIZE_META['pickOnTime'])
                time_str = padding0(current.hour) + ":" + padding0(current.minute) + ":" + padding0(current.second)
                # print("time_str :", time_str)
                if time_str == PRIZE_META['pickOnTime']:
                    print("on time")
                    PRIZE_META['pickOnTime'] = -1
                    self.start_prize_picker()
            finally:
                time.sleep(0.5)

    def start_prize_picker(self):
        self.process_btn.configure(state=DISABLED)
        self.generator_btn.configure(state=DISABLED)
        print("start prize picker")
        try:
            # Column integer to match the column which was clicked in the table
            # Create list of 'id's
            all_people = PRIZE_META['values']
            people_num = len(all_people)
            # print("people_num:", people_num)
            rand = choice(range(people_num))
            # print("随机数：", rand)
            all_items = PRIZE_META['items']
            for item in all_items:
                item.configure(background='skyblue')
            time.sleep(0.5)

            def my_focus_item():
                return focus_item(rand, people_num, self.process_btn, self.generator_btn)

            t = threading.Thread(target=my_focus_item)
            t.start()
        except Exception as err:
            self.process_btn.configure(state=NORMAL)
            if self.generator_btn:
                self.generator_btn.configure(state=NORMAL)

    def render_text_into_cards(self):
        self.generator_btn.configure(state=DISABLED)
        try:
            comment = self.log_text.get(1.0, END).strip()
            if comment is None or comment == '' or not comment or comment == "<这里黏贴参与活动人员>":
                print("请输入有效的名单")
                return
            # print("comment:", comment)
            lines = comment.split("\n")
            # print("number of lines:", len(lines))
            dataset = set(lines)
            # print("number of unique lines:", len(dataset))
            colspacings = []
            id_opt = self.user_opt.get()
            if id_opt == 0:
                for line in dataset:
                    colspacings.append(line.strip())
            elif id_opt == 1:
                for line in dataset:
                    if ':' in line:
                        id = line[:line.index(':')]
                        colspacings.append(id)
            elif id_opt == 2:
                for line in dataset:
                    if '：' in line:
                        id = line[:line.index('：')]
                        colspacings.append(id)
            # print("colspacings:", colspacings)
            PRIZE_META['values'] = colspacings
            render_labels_on_panel(self.paned_win, self.root)
        finally:
            self.generator_btn.configure(state=NORMAL)

    def clear_data(self):
        pass


def construct_menu(root):
    menubar = Menu(root)
    about_menu = Menu(menubar)
    setting_menu = Menu(menubar)
    about_menu.add_command(label='版权信息', command=show_copyright)
    about_menu.add_command(label='操作说明', command=show_about)
    about_menu.add_command(label='升级', command=trigger_upgrade)
    setting_menu.add_command(label='创建桌面快捷方式', command=make_shortcut)
    setting_menu.add_command(label='定时抽奖', command=lambda: schedule_picker(root))
    menubar.add_cascade(label="使用介绍", menu=about_menu)
    menubar.add_cascade(label="更多配置", menu=setting_menu)
    return menubar


def app_start():
    try:
        # init_metadata()
        root = Tk()
        menubar = construct_menu(root)
        root.config(menu=menubar)
        prize_ui = ChouJiang(root)
        prize_ui.setup_root_win()
        # 进入事件循环，保持窗口运行
        root.mainloop()
    finally:
        PRIZE_META['terminated'] = True
        print("program terminated, bye")
        sys.exit(0)


def main():
    hello = "hello prize"
    print(hello)
    return hello


if __name__ == '__main__':
    main()
    app_start()
