"""
AES AddRoundKey Transformation
"""


def add_round_key(
    state: list[list[int]],
    round_key: list[list[int]]
) -> list[list[int]]:

    new_state = [
        [0 for _ in range(4)]
        for _ in range(4)
    ]

    for row in range(4):

        for column in range(4):

            new_state[row][column] = (
                state[row][column]
                ^ round_key[row][column]
            )

    return new_state