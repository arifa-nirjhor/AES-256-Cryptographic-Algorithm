"""
AES-256 Single Block Encryption
"""

from aes.state import (
    bytes_to_state,
    state_to_bytes,
    print_state,
)

from aes.sub_bytes import sub_bytes
from aes.shift_rows import shift_rows
from aes.mix_columns import mix_columns
from aes.add_round_key import add_round_key
from aes.key_expansion import key_expansion


def encrypt_block(
    plaintext: bytes,
    key: bytes,
    show_steps: bool = True
) -> bytes:

    if len(plaintext) != 16:
        raise ValueError(
            "AES plaintext block must be exactly 16 bytes."
        )

    if len(key) != 32:
        raise ValueError(
            "AES-256 key must be exactly 32 bytes."
        )

    # Convert plaintext into state.
    state = bytes_to_state(plaintext)

    if show_steps:
        print_state(
            state,
            "Initial Plaintext State"
        )

    # Generate K0 through K14.
    round_keys = key_expansion(key)

    # Initial AddRoundKey.
    state = add_round_key(
        state,
        round_keys[0]
    )

    if show_steps:
        print_state(
            state,
            "After Initial AddRoundKey"
        )

    # --------------------------------------------
    # Rounds 1 through 13
    # --------------------------------------------

    for round_number in range(1, 14):

        if show_steps:

            print("=" * 50)
            print(f"ROUND {round_number}")
            print("=" * 50)

        state = sub_bytes(state)

        if show_steps:
            print_state(
                state,
                f"Round {round_number} - After SubBytes"
            )

        state = shift_rows(state)

        if show_steps:
            print_state(
                state,
                f"Round {round_number} - After ShiftRows"
            )

        state = mix_columns(state)

        if show_steps:
            print_state(
                state,
                f"Round {round_number} - After MixColumns"
            )

        state = add_round_key(
            state,
            round_keys[round_number]
        )

        if show_steps:
            print_state(
                state,
                f"Round {round_number} - After AddRoundKey"
            )

    # --------------------------------------------
    # Round 14
    # NO MixColumns
    # --------------------------------------------

    if show_steps:

        print("=" * 50)
        print("ROUND 14 - FINAL ROUND")
        print("=" * 50)

    state = sub_bytes(state)

    if show_steps:
        print_state(
            state,
            "Round 14 - After SubBytes"
        )

    state = shift_rows(state)

    if show_steps:
        print_state(
            state,
            "Round 14 - After ShiftRows"
        )

    state = add_round_key(
        state,
        round_keys[14]
    )

    if show_steps:
        print_state(
            state,
            "Round 14 - After AddRoundKey"
        )

    return state_to_bytes(state)