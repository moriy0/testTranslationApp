import pyautogui as pg
import tkinter as tk
from PIL import Image, ImageTk

import ocr


def clickButtonFunction():

        RESIZE_RETIO = 1.1 # 縮小倍率の規定

        # ドラッグ開始時のイベント
        def startPointGet(event):
            global startX, startY # グローバル変数に書き込みを行う

            canvas1.delete('rect1') # すでに'rect1'タグの図形があれば削除

            # canvas1上に四角形を描画
            canvas1.create_rectangle(
                event.x,
                event.y,
                event.x + 1,
                event.y + 1,
                outline = 'red',
                tag = 'rect1'
            )
            # グローバル変数に座標を格納
            startX, startY = event.x, event.y


        # ドラッグ中のイベント
        def rectDrawing(event):
            # ドラッグ中のマウスポインタが領域外に出た時の処理
            if event.x < 0:
                endX = 0
            else:
                endX = min(resizedImg.width, event.x)
            if event.y < 0:
                endY = 0
            else:
                endY = min(resizedImg.height, event.y)

            # 'rect1'タグの画像を再描画
            canvas1.coords('rect1', startX, startY, endX, endY)


        # ドラッグを離したときのイベント
        def releaseAction(event):
            # 'rect1'タグの画像の座標を元の縮尺に戻して取得
            startX, startY, endX, endY = [round(n * RESIZE_RETIO) for n in canvas1.coords('rect1')]

            # .destroy()でTKinterのウィンドウを閉じる
            root.destroy()

            cutOutImage(startX, startY, endX, endY)


        # 画像切り抜き後、翻訳結果を表示する
        def cutOutImage(startX, startY, endX, endY):

            def clickCloseButton():
                # 翻訳結果を閉じる
                root_tran.destroy()


            root_tran = tk.Tk()

            # 取得した座標でスクリーンショットを切り抜く
            img_cutout = img.crop((startX, startY, endX, endY))
            # img_cutout_tk = ImageTk.PhotoImage(img_cutout, master=root_cutout)

            translatedTxt = ocr.imageToString(img_cutout)

            # 翻訳結果を表示するためのウィジェットの作成
            label = tk.Label(root_tran, text=translatedTxt)

            # 翻訳結果を閉じるボタンを作成
            closeButton = tk.Button(
                root_tran,
                width=10,
                height=1,
                text='Close',
                command=clickCloseButton
            )

            # pack()でウィジェットを配置
            label.pack()
            closeButton.pack()

            root_tran.mainloop()


        # 表示する画像の取得
        img = pg.screenshot()
        # 取得したスクリーンショットは表示しきれないので画像リサイズ
        resizedImg = img.resize(
            size=(
                int(img.width / RESIZE_RETIO),
                int(img.height / RESIZE_RETIO)),
            resample=Image.BILINEAR
        )

        root = tk.Tk()
        root.attributes('-topmost', True) # tkinterウィンドウを常に最前面に表示

        # tkinterで表示できるように画像変換
        # 引数のmasterはその画像を表示するウィジェットが格納される
        img_tk = ImageTk.PhotoImage(resizedImg, master=root)
        # ガベージコレクションでimg変数が破棄されている可能性があるので
        # imgインスタンス・オブジェクトの中にimageアトリビュートを作成して保持する
        img.image = img_tk

        # Canvasウィジェットの描画
        canvas1 = tk.Canvas(
            root,
            bg='black',
            width=resizedImg.width,
            height=resizedImg.height
        )

        # Canvasウィジェットに取得した画像を描画
        canvas1.create_image(0, 0, image=img.image, anchor=tk.NW)

        # pack()でCanvasウィジェットを配置し、bind()で各種イベントを設定
        canvas1.pack()
        canvas1.bind('<ButtonPress-1>', startPointGet)
        canvas1.bind('<Button1-Motion>', rectDrawing)
        canvas1.bind('<ButtonRelease-1>', releaseAction)

        root.mainloop()
