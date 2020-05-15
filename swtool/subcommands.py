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
        if unicodedata.east_asian_width(c) in 'FWA':
            count += 1
    return count