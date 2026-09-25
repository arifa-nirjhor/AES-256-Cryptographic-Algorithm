"""
AES-256 Key Expansion

32-byte key
    ->
8 initial words
    ->
60 total words
    ->
15 round keys
"""

from aes.sub_bytes import S_BOX


RCON = [
    0x00,
    0x01,
    0x02,
    0x04,
    0x08,
    0x10,
    0x20,
    0x40,
    0x80,
    0x1B,
    0x36,
]


def rot_word(
    word: list[int]
) -> list[int]:

    return word[1:] + word[:1]


def sub_word(
    word: list[int]
) -> list[int]:

    return [
        S_BOX[byte]
        for byte in word
    ]


def xor_words(
    word1: list[int],
    word2: list[int]
) -> list[int]:

    return [
        word1[i] ^ word2[i]
        for i in range(4)
    ]


def g_function(
    word: list[int],
    round_number: int
) -> list[int]:

    result = rot_word(word)

    result = sub_word(result)

    result[0] ^= RCON[round_number]

    return result


def key_expansion(
    key: bytes
) -> list[list[list[int]]]:

    if len(key) != 32:
        raise ValueError(
            "AES-256 key must be exactly 32 bytes."
        )

    # ------------------------------------------------
    # STEP 1:
    # Split 32-byte key into 8 words:
    #
    # W0 W1 W2 W3 W4 W5 W6 W7
    # ------------------------------------------------

    words = []

    for i in range(8):

        word = [
            key[4 * i],
            key[4 * i + 1],
            key[4 * i + 2],
            key[4 * i + 3],
        ]

        words.append(word)

    # ------------------------------------------------
    # STEP 2:
    # Generate W8 through W59.
    # ------------------------------------------------

    for i in range(8, 60):

        temp = words[i - 1].copy()

        # Every 8th word:
        #
        # RotWord
        # SubWord
        # RCON
        if i % 8 == 0:

            round_number = i // 8

            temp = g_function(
                temp,
                round_number
            )

        # AES-256 has this additional
        # SubWord operation.
        elif i % 8 == 4:

            temp = sub_word(temp)

        # Wi = W(i-8) XOR temp

        new_word = xor_words(
            words[i - 8],
            temp
        )

        words.append(new_word)

    # ------------------------------------------------
    # STEP 3:
    # Convert 60 words into
    # 15 round-key matrices.
    # ------------------------------------------------

    round_keys = []

    for round_number in range(15):

        start = round_number * 4

        w0 = words[start]
        w1 = words[start + 1]
        w2 = words[start + 2]
        w3 = words[start + 3]

        round_key = [
            [w0[0], w1[0], w2[0], w3[0]],
            [w0[1], w1[1], w2[1], w3[1]],
            [w0[2], w1[2], w2[2], w3[2]],
            [w0[3], w1[3], w2[3], w3[3]],
        ]

        round_keys.append(
            round_key
        )

    return round_keys