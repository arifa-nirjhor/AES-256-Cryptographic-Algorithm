"""
AES State Matrix Module

AES always works on a 16-byte block.

The 16 bytes are arranged into
a 4x4 matrix column by column.
"""


def bytes_to_state(data: bytes) -> list[list[int]]:
    """
    Convert 16 bytes into a 4x4 AES state matrix.
    """

    if len(data) != 16:
        raise ValueError(
            "AES block must be exactly 16 bytes."
        )

    state = [
        [0 for _ in range(4)]
        for _ in range(4)
    ]

    for i in range(16):

        row = i % 4
        column = i // 4

        state[row][column] = data[i]

    return state


def state_to_bytes(state: list[list[int]]) -> bytes:
    """
    Convert a 4x4 AES state matrix
    back into 16 bytes.
    """

    output = bytearray(16)

    for i in range(16):

        row = i % 4
        column = i // 4

        output[i] = state[row][column]

    return bytes(output)


def print_state(
    state: list[list[int]],
    title: str = "State"
) -> None:

    print(f"\n{title}")
    print("-" * 25)

    for row in state:
        print(
            " ".join(
                f"{byte:02X}"
                for byte in row
            )
        )

    print()