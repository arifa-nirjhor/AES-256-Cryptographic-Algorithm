"""
AES-256 Educational Implementation

Tests AES-256 encryption and decryption
using a standard known-answer test vector.
"""

from aes.encrypt_block import encrypt_block
from aes.decrypt_block import decrypt_block
from aes.key_expansion import key_expansion
from aes.state import print_state


def print_hex(data: bytes) -> None:

    print(
        " ".join(
            f"{byte:02X}"
            for byte in data
        )
    )


def main():

    print("\n" + "=" * 70)
    print("AES-256 ENCRYPTION AND DECRYPTION")
    print("=" * 70)

    # Standard AES-256 test plaintext.
    plaintext = bytes.fromhex(
        "00112233445566778899AABBCCDDEEFF"
    )

    # 256-bit / 32-byte key.
    key = bytes.fromhex(
        "000102030405060708090A0B0C0D0E0F"
        "101112131415161718191A1B1C1D1E1F"
    )

    # Expected ciphertext.
    expected_ciphertext = bytes.fromhex(
        "8EA2B7CA516745BFEAFC49904B496089"
    )

    print("\nPLAINTEXT:")
    print_hex(plaintext)

    print("\nAES-256 KEY:")
    print_hex(key)

    print("\n" + "=" * 70)
    print("KEY EXPANSION")
    print("=" * 70)

    round_keys = key_expansion(key)

    print(
        f"\nTotal Round Keys: {len(round_keys)}"
    )

    for round_number in range(15):

        print_state(
            round_keys[round_number],
            f"Round Key K{round_number}"
        )

    print("\n" + "#" * 70)
    print("AES-256 ENCRYPTION")
    print("#" * 70)

    ciphertext = encrypt_block(
        plaintext,
        key,
        show_steps=True
    )

    print("\n" + "=" * 70)
    print("ENCRYPTION RESULT")
    print("=" * 70)

    print("\nCiphertext:")
    print_hex(ciphertext)

    print("\nContinuous Hex:")
    print(
        ciphertext.hex().upper()
    )

    print("\nExpected:")
    print(
        expected_ciphertext.hex().upper()
    )

    if ciphertext == expected_ciphertext:

        print(
            "\nEncryption test: SUCCESS"
        )

    else:

        print(
            "\nEncryption test: FAILED"
        )

    print("\n" + "#" * 70)
    print("AES-256 DECRYPTION")
    print("#" * 70)

    recovered_plaintext = decrypt_block(
        ciphertext,
        key,
        show_steps=True
    )

    print("\n" + "=" * 70)
    print("DECRYPTION RESULT")
    print("=" * 70)

    print("\nRecovered Plaintext:")
    print_hex(recovered_plaintext)

    print("\nOriginal Plaintext:")
    print_hex(plaintext)

    if recovered_plaintext == plaintext:

        print(
            "\nDecryption test: SUCCESS"
        )

    else:

        print(
            "\nDecryption test: FAILED"
        )

    print("\n" + "=" * 70)

    if (
        ciphertext == expected_ciphertext
        and recovered_plaintext == plaintext
    ):

        print(
            "AES-256 IMPLEMENTATION VERIFIED SUCCESSFULLY"
        )

    else:

        print(
            "AES-256 VERIFICATION FAILED"
        )

    print("=" * 70)


if __name__ == "__main__":
    main()