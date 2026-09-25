"""
AES ShiftRows and Inverse ShiftRows
"""


def shift_rows(
    state: list[list[int]]
) -> list[list[int]]:

    shifted_state = []

    for row_index in range(4):

        row = state[row_index]

        shifted_row = (
            row[row_index:]
            + row[:row_index]
        )

        shifted_state.append(
            shifted_row
        )

    return shifted_state


def inv_shift_rows(
    state: list[list[int]]
) -> list[list[int]]:

    new_state = []

    for row_index in range(4):

        row = state[row_index]

        if row_index == 0:

            shifted_row = row.copy()

        else:

            shifted_row = (
                row[-row_index:]
                + row[:-row_index]
            )

        new_state.append(
            shifted_row
        )

    return new_state