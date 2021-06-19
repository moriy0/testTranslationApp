import tkinter as tk

import cutOut

# メインウィンドウ作成
def createMainPage():
    app = tk.Tk()
    app.title(u'translation')
    app.attributes('-topmost', True)
    app.geometry('300x50')

    # ボタン作成
    selectButton = tk.Button(
        app,
        width=35,
        height=2,
        text='select',
        # 指定する関数には「()」をつけないようにする
        # 「()」をつけると、その場で実行されてしまう
        command=cutOut.clickButtonFunction
    )

    # ウィジェットの配置
    selectButton.pack()

    # メインループ
    app.mainloop()


if __name__ == '__main__':
    createMainPage()