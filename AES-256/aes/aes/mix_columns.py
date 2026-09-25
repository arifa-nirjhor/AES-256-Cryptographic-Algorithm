"""
AES MixColumns and Inverse MixColumns

Arithmetic is performed in GF(2^8).
"""


def gf_multiply(a: int, b: int) -> int:

    result = 0

    for _ in range(8):

        # Check lowest bit of b.
        if b & 1:
            result ^= a

        # Remember high bit of a.
        high_bit = a & 0x80

        # Shift a left.
        a = (a << 1) & 0xFF

        # AES polynomial reduction.
        if high_bit:
            a ^= 0x1B

        # Move to next bit of b.
        b >>= 1

    return result


def multiply_by_02(byte: int) -> int:
    return gf_multiply(byte, 0x02)


def multiply_by_03(byte: int) -> int:
    return gf_multiply(byte, 0x03)


def mix_single_column(
    column: list[int]
) -> list[int]:

    s0, s1, s2, s3 = column

    r0 = (
        gf_multiply(s0, 0x02)
        ^ gf_multiply(s1, 0x03)
        ^ s2
        ^ s3
    )

    r1 = (
        s0
        ^ gf_multiply(s1, 0x02)
        ^ gf_multiply(s2, 0x03)
        ^ s3
    )

    r2 = (
        s0
        ^ s1
        ^ gf_multiply(s2, 0x02)
        ^ gf_multiply(s3, 0x03)
    )

    r3 = (
        gf_multiply(s0, 0x03)
        ^ s1
        ^ s2
        ^ gf_multiply(s3, 0x02)
    )

    return [r0, r1, r2, r3]


def mix_columns(
    state: list[list[int]]
) -> list[list[int]]:

    new_state = [
        [0 for _ in range(4)]
        for _ in range(4)
    ]

    for column_index in range(4):

        column = [
            state[0][column_index],
            state[1][column_index],
            state[2][column_index],
            state[3][column_index],
        ]

        mixed_column = mix_single_column(
            column
        )

        for row_index in range(4):

            new_state[row_index][column_index] = (
                mixed_column[row_index]
            )

    return new_state


def inv_mix_single_column(
    column: list[int]
) -> list[int]:

    s0, s1, s2, s3 = column

    r0 = (
        gf_multiply(s0, 0x0E)
        ^ gf_multiply(s1, 0x0B)
        ^ gf_multiply(s2, 0x0D)
        ^ gf_multiply(s3, 0x09)
    )

    r1 = (
        gf_multiply(s0, 0x09)
        ^ gf_multiply(s1, 0x0E)
        ^ gf_multiply(s2, 0x0B)
        ^ gf_multiply(s3, 0x0D)
    )

    r2 = (
        gf_multiply(s0, 0x0D)
        ^ gf_multiply(s1, 0x09)
        ^ gf_multiply(s2, 0x0E)
        ^ gf_multiply(s3, 0x0B)
    )

    r3 = (
        gf_multiply(s0, 0x0B)
        ^ gf_multiply(s1, 0x0D)
        ^ gf_multiply(s2, 0x09)
        ^ gf_multiply(s3, 0x0E)
    )

    return [r0, r1, r2, r3]


def inv_mix_columns(
    state: list[list[int]]
) -> list[list[int]]:

    new_state = [
        [0 for _ in range(4)]
        for _ in range(4)
    ]

    for column_index in range(4):

        column = [
            state[0][column_index],
            state[1][column_index],
            state[2][column_index],
            state[3][column_index],
        ]

        mixed_column = (
            inv_mix_single_column(column)
        )

        for row_index in range(4):

            new_state[row_index][column_index] = (
                mixed_column[row_index]
            )

    return new_state