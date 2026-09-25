"""
AES-256 Single Block Decryption
"""

from aes.state import (
    bytes_to_state,
    state_to_bytes,
    print_state,
)

from aes.sub_bytes import inv_sub_bytes
from aes.shift_rows import inv_shift_rows
from aes.mix_columns import inv_mix_columns
from aes.add_round_key import add_round_key
from aes.key_expansion import key_expansion


def decrypt_block(
    ciphertext: bytes,
    key: bytes,
    show_steps: bool = True
) -> bytes:

    if len(ciphertext) != 16:
        raise ValueError(
            "AES ciphertext block must be exactly 16 bytes."
        )

    if len(key) != 32:
        raise ValueError(
            "AES-256 key must be exactly 32 bytes."
        )

    state = bytes_to_state(ciphertext)

    if show_steps:
        print_state(
            state,
            "Initial Ciphertext State"
        )

    round_keys = key_expansion(key)

    # Undo final encryption AddRoundKey.
    state = add_round_key(
        state,
        round_keys[14]
    )

    if show_steps:
        print_state(
            state,
            "After AddRoundKey K14"
        )

    # --------------------------------------------
    # Reverse rounds 13 through 1
    # --------------------------------------------

    for round_number in range(13, 0, -1):

        if show_steps:

            print("=" * 50)
            print(
                f"DECRYPTION ROUND {round_number}"
            )
            print("=" * 50)

        state = inv_shift_rows(state)

        if show_steps:
            print_state(
                state,
                f"Round {round_number} - After InvShiftRows"
            )

        state = inv_sub_bytes(state)

        if show_steps:
            print_state(
                state,
                f"Round {round_number} - After InvSubBytes"
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

        state = inv_mix_columns(state)

        if show_steps:
            print_state(
                state,
                f"Round {round_number} - After InvMixColumns"
            )

    # --------------------------------------------
    # Final inverse round
    # --------------------------------------------

    if show_steps:

        print("=" * 50)
        print("FINAL DECRYPTION ROUND")
        print("=" * 50)

    state = inv_shift_rows(state)

    if show_steps:
        print_state(
            state,
            "Final Round - After InvShiftRows"
        )

    state = inv_sub_bytes(state)

    if show_steps:
        print_state(
            state,
            "Final Round - After InvSubBytes"
        )

    state = add_round_key(
        state,
        round_keys[0]
    )

    if show_steps:
        print_state(
            state,
            "Final Round - After AddRoundKey K0"
        )

    return state_to_bytes(state)