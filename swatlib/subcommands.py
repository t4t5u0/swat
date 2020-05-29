import unicodedata

# 全角を2半角を1として文字列長を計算する
def get_east_asian_count(text):
    count = 0
    for c in text:
        if unicodedata.east_asian_width(c) in 'FWA':
            count += 2
        else:
            count += 1
    return count

# 日本語の文字数を数える
def count_east_asian_character(text):
    count = 0
    for c in text:
        # ローマ数字の判定おかしいので
        if c in ['Ⅰ', 'Ⅱ', 'Ⅲ', 'Ⅳ', 'Ⅴ', 'Ⅵ', 'Ⅶ', 'Ⅷ', 'Ⅸ', 'Ⅹ', '⏩']:
            count -= 1
        if unicodedata.east_asian_width(c) in 'FWA':
            count += 1
    return count

# リストから複数の文字列を検索し、それらのインデックスを返す
def serch_words_index(ls, words):
    result = []
    for i, item in enumerate(ls):
        if item in words:
            result.append(i)
    return result


# 文字列をn文字ごとに区切って、インデックスのリストを返す関数。もしくは、区切ったあとの文字列を返す関数
def turn_back_text(text:str, n:int) -> list:
    result = []
    count = 0
    tmp = ''
    for c in text:
        tmp += c
        if c in ['Ⅰ', 'Ⅱ', 'Ⅲ', 'Ⅳ', 'Ⅴ', 'Ⅵ', 'Ⅶ', 'Ⅷ', 'Ⅸ', 'Ⅹ', '⏩']:
            count += 2
        elif unicodedata.east_asian_width(c) in 'FWA':
            count += 2
        else:
            count += 1
        if count > n-1:
            count = 0
            result.append(tmp)
            tmp = ''
    else:
        if tmp != '':
            result.append(tmp)
    return result

