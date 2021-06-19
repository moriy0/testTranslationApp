from PIL import Image
import pyocr

import translation

def imageToString(image):
    # OCRエンジン取得
    tools = pyocr.get_available_tools()
    tool = tools[0]

    print(type(image))

    # 使用する画像を指定してOCRを実行
    txt = tool.image_to_string(
        # Image.open(image),　　# 画像ファイルを読み込む場合
        image,
        lang='eng',
        builder=pyocr.builders.TextBuilder()
    )

    # 翻訳を実行
    translatedTxt = translation.translateEngToJa(txt)

    print(translatedTxt)

    # 翻訳結果を返却
    return translatedTxt