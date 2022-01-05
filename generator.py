from jamo import j2h, j2hcj
from itertools import product
import bisect
import itertools
import random


CHOSUNG_LIST = [
    "ㄱ",
    "ㄲ",
    "ㄴ",
    "ㄷ",
    "ㄸ",
    "ㄹ",
    "ㅁ",
    "ㅂ",
    "ㅃ",
    "ㅅ",
    "ㅆ",
    "ㅇ",
    "ㅈ",
    "ㅉ",
    "ㅊ",
    "ㅋ",
    "ㅌ",
    "ㅍ",
    "ㅎ",
]

JUNGSUNG_LIST = [
    "ㅏ",
    "ㅐ",
    "ㅑ",
    "ㅒ",
    "ㅓ",
    "ㅔ",
    "ㅕ",
    "ㅖ",
    "ㅗ",
    "ㅘ",
    "ㅙ",
    "ㅚ",
    "ㅛ",
    "ㅜ",
    "ㅝ",
    "ㅞ",
    "ㅟ",
    "ㅠ",
    "ㅡ",
    "ㅢ",
    "ㅣ",
]

JONGSUNG_LIST = [
    " ",
    "ㄱ",
    "ㄲ",
    "ㄳ",
    "ㄴ",
    "ㄵ",
    "ㄶ",
    "ㄷ",
    "ㄹ",
    "ㄺ",
    "ㄻ",
    "ㄼ",
    "ㄽ",
    "ㄾ",
    "ㄿ",
    "ㅀ",
    "ㅁ",
    "ㅂ",
    "ㅄ",
    "ㅅ",
    "ㅆ",
    "ㅇ",
    "ㅈ",
    "ㅊ",
    "ㅋ",
    "ㅌ",
    "ㅍ",
    "ㅎ",
]


def korean_jamo(korean_word):
    r_lst = []
    for w in list(korean_word.strip()):
        if "가" <= w <= "힣":
            ch1 = (ord(w) - ord("가")) // 588
            ch2 = ((ord(w) - ord("가")) - (588 * ch1)) // 28
            ch3 = (ord(w) - ord("가")) - (588 * ch1) - 28 * ch2
            r_lst.append([CHOSUNG_LIST[ch1], JUNGSUNG_LIST[ch2], JONGSUNG_LIST[ch3]])
        else:
            r_lst.append([w])
    return r_lst


def change(a):
    if a[1] == "ㅔ":
        return [[a[0], "ㅔ", a[2]], [a[0], "ㅐ", a[2]]]
    if a[1] == "ㅐ":
        return [[a[0], "ㅔ", a[2]], [a[0], "ㅐ", a[2]]]
    if a[1] == "ㅖ":
        return [[a[0], "ㅖ", a[2]], [a[0], "ㅒ", a[2]]]
    if a[1] == "ㅒ":
        return [[a[0], "ㅖ", a[2]], [a[0], "ㅒ", a[2]]]
    else:
        return [a]


def doSomeThing(data, length):
    if len(data) < 2:
        return data[0]
    elif len(data) < 3:
        return j2h(data[0], data[1])
    else:
        return j2h(data[0], data[1], data[2])


# a = korean_jamo("텔레비전")

# data = []
# w2 = []

# for i in range(0, len(a)):
#     w = change(a[i])
#     w2.append(w)

# w3 = list(product(*w2))


# for i in w3:
#     lk = []
#     for kk in i:
#         ll = "".join(kk)
#         lk.append(doSomeThing(j2hcj(ll), len(j2hcj(ll))))
#     data.append("".join(lk))


# print(data)


# 글자 교체
# 글자 추가
# 글자 삭제
# 초성 전환

from random import randrange, choice, sample


def character_generator():
    chosung, jungsung, jongsung = "", "", ""
    chosung = CHOSUNG_LIST[randrange(0, len(CHOSUNG_LIST))]
    if randrange(0, 10) < 8:
        jungsung = JUNGSUNG_LIST[randrange(0, len(JUNGSUNG_LIST))]
        if randrange(0, 10) < 8:
            jongsung = JONGSUNG_LIST[randrange(0, len(JONGSUNG_LIST))]
    ll = "".join([chosung, jungsung, jongsung]).strip()
    return doSomeThing(j2hcj(ll), len(j2hcj(ll)))


def split_chractor(w):
    if "가" <= w <= "힣":
        ch1 = (ord(w) - ord("가")) // 588
        ch2 = ((ord(w) - ord("가")) - (588 * ch1)) // 28
        ch3 = (ord(w) - ord("가")) - (588 * ch1) - 28 * ch2
        return [CHOSUNG_LIST[ch1], JUNGSUNG_LIST[ch2], JONGSUNG_LIST[ch3]]
    else:
        return [w]


def random_replace(word, charactor):
    sample_values = sample(range(0, len(word)), randrange(0, len(word) // 2))
    for rand_index in sample_values:
        if rand_index >= len(word):
            break
        split_charactor_value = word[rand_index]
        if rand_index == 0:  # float("inf")
            split_charactor_value = choice([charactor, word[rand_index]])
        splited_charasctor = split_chractor(split_charactor_value)
        random_charactor = splited_charasctor[
            randrange(0, len(splited_charasctor))
        ].strip()
        word = word.replace(word[rand_index], random_charactor)
    return word


for _ in range(100):
    generated_charactor = character_generator()
    print(
        generated_charactor,
        ", ",
        split_chractor(generated_charactor),
        ", ",
        random_replace("성모외과병원", generated_charactor),
    )
