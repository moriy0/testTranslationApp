from googletrans import Translator


def translateEngToJa(txt):
    translator = Translator()

    # googletrans 4.0.0のアルファバージョンが正常に動いた
    # ここで翻訳
    translation = translator.translate(txt, src='en', dest='ja')

    # 翻訳された結果を返す
    return translation.text