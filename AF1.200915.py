import tkinter
import tkinter.filedialog
import os
from PIL import ImageGrab
from time import sleep
import time
from Tools import autoFocus
# from screenShot import window_capture

from pynput.mouse import Controller,Button

root = tkinter.Tk()
root.geometry('500x120+400+300')
root.resizable(False, False)
mouse = Controller()

class MyCapture:

    def __init__(self, png):
        # 变量X和Y用来记录鼠标左键按下的位置
        self.X = tkinter.IntVar(value=0)
        self.Y = tkinter.IntVar(value=0)
        # 屏幕尺寸
        screenWidth = root.winfo_screenwidth()
        screenHeight = root.winfo_screenheight()
        # 创建顶级组件容器
        self.top = tkinter.Toplevel(root, width=screenWidth, height=screenHeight)
        # 不显示最大化、最小化按钮
        self.top.overrideredirect(True)
        self.top.attributes('-alpha', 0.5)
        self.canvas = tkinter.Canvas(self.top, bg='white', width=screenWidth, height=screenHeight)
        self.canvas.bind('<Button-1>', self.onLeftButtonDown)
        self.canvas.bind('<B1-Motion>', self.onLeftButtonMove)
        self.canvas.bind('<ButtonRelease-1>', self.onLeftButtonUp)

        self.canvas.pack()
        self.position = []
        # 显示全屏截图，在全屏截图上进行区域截图
        # self.image = tkinter.PhotoImage(file=png)
        # self.canvas.create_image(screenWidth // 2, screenHeight // 2, image=self.image)
        # 鼠标左键按下的位置

    def onLeftButtonDown(self, event):

        self.X.set(event.x)
        self.Y.set(event.y)
        # 开始截图
        self.sel = True

    # 鼠标左键移动，显示选取的区域
    def onLeftButtonMove(self, event):

        if not self.sel:
            return
        global lastDraw
        try:
            # 删除刚画完的图形，要不然鼠标移动的时候是黑乎乎的一片矩形
            self.canvas.delete(lastDraw)
        except Exception as e:
            print(e)
        lastDraw = self.canvas.create_rectangle(self.X.get(), self.Y.get(), event.x, event.y, outline='black')

    # 获取鼠标左键抬起的位置，保存区域截图
    def onLeftButtonUp(self, event):
        global lastDraw
        self.sel = False

        try:
            self.canvas.delete(lastDraw)
        except Exception as e:
            pass
        sleep(0.1)
        # 考虑鼠标左键从右下方按下而从左上方抬起的截图
        left, right = sorted([self.X.get(), event.x])
        top, bottom = sorted([self.Y.get(), event.y])
        # beg = time.time()

        pic = ImageGrab.grab((left + 1, top + 1, right, bottom))
        # print(left + 1, top + 1, right, bottom)
        self.position = [left + 1, top + 1, right, bottom]
        # end = time.time()
        # print(end - beg)


        # beg = time.time()
        # window_capture('laji.png', position)
        # end = time.time()
        # print(end - beg)
        # 弹出保存截图对话框
        # fileName = tkinter.filedialog.asksaveasfilename(title='保存截图', filetypes=[('image', '*.jpg *.png')])
        # print(fileName)
        # if fileName:
        pic.save('./img/screenShot.png')
        sleep(0.1)

        # 关闭当前窗口
        self.canvas.pack(fill=tkinter.BOTH, expand=tkinter.YES)
        self.top.destroy()


    # 开始截图
def buttonCaptureClick():
    # 最小化主窗口
    root.state('icon')
    sleep(0.2)
    filename = 'temp.png'
    im = ImageGrab.grab()
    im.save(filename)
    im.close()
    # 显示全屏幕截图
    w = MyCapture(filename)
    buttonCapturePosition.wait_window(w.top)
    # 截图结束，恢复主窗口，并删除临时的全屏幕截图文件
    ssPos["text"] = w.position
    root.state('normal')
    os.remove(filename)

# 获取目标区域坐标进行截图后获取清晰度值
def buttonGetPosition():
    settingPos = ssPos["text"] # str
    settingPosL = settingPos.split(' ')
    for i in range(len(settingPosL)):
        settingPosL[i] = int(settingPosL[i])
    settingPic = ImageGrab.grab((settingPosL[0],settingPosL[1],settingPosL[2],settingPosL[3]))
    settingPic.save('./img/screenShot.png')
    score['text'] = autoFocus('./img/screenShot.png').getImgVarTenengrad()

# 设置目标值
def targetScoreSetting():
    ts['text'] = score['text']

# 3秒后获取鼠标位置，用于定位鼠标操作的位置
def mousePos():
    # Read pointer position
    sleep(3)
    print('The current pointer position is {0}'.format(mouse.position))
    cpLabel['text'] = mouse.position

# 到指定屏幕位置进行操作
def mouseRolling(dir:int, num:int):
    if cpLabel['text'] != 'Null':
        pos = getData(cpLabel['text'])
        mouse.position = (pos[0], pos[1])
        mouse.press(Button.left)
        mouse.release(Button.left)
        mouse.scroll(dir, num)

# 对比目标值和实际值后进行鼠标操作
def start():
    try:
        rollNum = list(dirText.get())
        print(rollNum)
        if abs(float(score['text']) - float(ts['text'])) > 5:
            print((float(score['text']) - float(ts['text'])))
            mouseRolling(rollNum[0], rollNum[1])
    except Exception as e:
        print(e)

# 从Label中获取数值转列表
def getData(data):
    if data is not 'Null':
        list = []
        list = data.split(' ')
    return list

buttonCapturePosition = tkinter.Button(root, text='选取目标区域', command=buttonCaptureClick)
buttonCapturePosition.grid(row=0, column=0, padx=5, pady=5)

btnSetting = tkinter.Button(root, text='设置目标清晰度', command=targetScoreSetting)
btnSetting.grid(row=1, column=0, padx=5, pady=5)
buttonCaptureAnalysis = tkinter.Button(root, text='获取', command=buttonGetPosition)
buttonCaptureAnalysis.grid(row=2, column=0, padx=5, pady=5)

ssLabel = tkinter.Label(root, text='截图区域： ')
ssLabel.grid(row=0, column=1, padx=5, pady=5)
ssPos = tkinter.Label(root, text='0 0 0 0')
ssPos.grid(row=0, column=2, padx=5, pady=5)

# Target score
tsLabel = tkinter.Label(root, text='Target score: ')
tsLabel.grid(row=1, column=1, padx=5, pady=5)
ts = tkinter.Label(root, text='Null')
ts.grid(row=1, column=2, padx=5, pady=5)

scoreLabel = tkinter.Label(root, text='Score: ')
scoreLabel.grid(row=2, column=1, padx=5, pady=5)
score = tkinter.Label(root, text='Null')
score.grid(row=2, column=2, padx=5, pady=5)


curPosition = tkinter.Button(root, text='获取控制坐标', command=mousePos)
curPosition.grid(row=0, column=5, padx=5, pady=5)
cpLabel = tkinter.Label(root, text='Null')
cpLabel.grid(row=0, column=6, padx=5, pady=5)

btnRolling = tkinter.Button(root, text='开始', command=start)
btnRolling.grid(row=1, column=5, padx=5, pady=5)

dirText = tkinter.Entry(root, text='12')
dirText.grid(row=2, column=5, padx=5, pady=5)


# 启动消息主循环
root.mainloop()
