# AES-256 Encryption and Decryption in Python

**An educational, from-scratch implementation of the AES-256 block cipher**, featuring key expansion, encryption, decryption, and step-by-step visualization of intermediate AES state matrices.

This project implements the core AES-256 transformations directly in Python to demonstrate how the Advanced Encryption Standard operates internally. It is designed for studying symmetric-key cryptography, finite-field arithmetic, and the AES round structure.

> **Educational use only.** This is a single-block AES implementation, not a complete secure messaging or file-encryption system. It does not implement a mode of operation, random nonce/IV management, authentication, or secure key storage. For real-world encryption, use a maintained cryptographic library with an authenticated mode such as AES-GCM.

## Overview

| Property | Value |
| --- | --- |
| Algorithm | AES-256 (Advanced Encryption Standard) |
| Cipher type | Symmetric-key block cipher |
| Key length | 256 bits (32 bytes) |
| Block length | 128 bits (16 bytes) |
| Number of rounds | 14 |
| Expanded round keys | 15 (K0–K14) |
| Expanded key words | 60 words (4 bytes each) |
| Language | Python 3 |
| External Python packages | None |

## Features

- **AES-256 block encryption:** Encrypts exactly one 16-byte plaintext block with a 32-byte key.
- **AES-256 block decryption:** Reverses the encryption process and restores the original 16-byte block.
- **Key expansion:** Derives 15 round keys from the original 256-bit key using `RotWord`, `SubWord`, round constants (`Rcon`), and XOR.
- **Core transformations:** Implements `SubBytes`, `ShiftRows`, `MixColumns`, and `AddRoundKey`.
- **Inverse transformations:** Implements `InvSubBytes`, `InvShiftRows`, and `InvMixColumns` for decryption.
- **Finite-field arithmetic:** Performs `MixColumns` multiplication in GF(2⁸), with reduction based on the AES polynomial.
- **Step-by-step output:** Displays round keys and intermediate 4×4 state matrices in hexadecimal.
- **Known-answer verification:** Compares the result with a standard AES-256 test vector and checks that decryption restores the input.

## Project Structure

Organize the files as follows. The `aes/` package is required because `main.py` imports modules using `from aes...`.

```text
AES-256/
├── main.py
├── README.md
└── aes/
    ├── __init__.py
    ├── state.py
    ├── sub_bytes.py
    ├── shift_rows.py
    ├── mix_columns.py
    ├── add_round_key.py
    ├── key_expansion.py
    ├── encrypt_block.py
    └── decrypt_block.py
```

Create an empty `aes/__init__.py` file if it does not already exist. The eight Python module files in `aes/` correspond to the supplied source files; `main.py` remains in the project root.

### Module Responsibilities

| File | Responsibility |
| --- | --- |
| `main.py` | Runs the demonstration, prints the round keys, and verifies encryption/decryption. |
| `aes/state.py` | Converts 16-byte blocks to/from the 4×4 column-major AES state and prints states. |
| `aes/sub_bytes.py` | Applies the AES S-box and inverse S-box. |
| `aes/shift_rows.py` | Performs row shifts and inverse row shifts. |
| `aes/mix_columns.py` | Mixes columns and reverses the mixing using GF(2⁸) arithmetic. |
| `aes/add_round_key.py` | XORs the state with the corresponding round key. |
| `aes/key_expansion.py` | Expands a 32-byte key into 60 words and 15 round-key matrices. |
| `aes/encrypt_block.py` | Implements 14-round AES-256 encryption of one block. |
| `aes/decrypt_block.py` | Implements inverse AES-256 decryption of one block. |

## How AES-256 Encryption Works

AES processes each 16-byte block as a **4×4 state matrix**, filled column by column.

### 1. Key Expansion

The 32-byte input key is divided into eight initial 4-byte words. The key schedule generates a total of **60 words**, grouped into **15 round keys**, K0 through K14.

The AES-256 key schedule includes an extra `SubWord` operation when the generated word index satisfies `i % 8 == 4`.

### 2. Initial Transformation

Before the main rounds, the plaintext state is XORed with **K0** using `AddRoundKey`.

### 3. Main Rounds (1–13)

Each round performs these transformations in order:

1. **SubBytes:** Replaces each byte using the AES substitution box.
2. **ShiftRows:** Cyclically shifts the four rows left by 0, 1, 2, and 3 positions.
3. **MixColumns:** Transforms each column using matrix multiplication in GF(2⁸).
4. **AddRoundKey:** XORs the state with that round's key.

### 4. Final Round (14)

The final round performs `SubBytes`, `ShiftRows`, and `AddRoundKey` with **K14**. **MixColumns is omitted in the final round.**

```text
Plaintext (16 bytes)
        |
        v
  State Matrix
        |
        v
  AddRoundKey (K0)
        |
        v
  Rounds 1–13:
    SubBytes
    ShiftRows
    MixColumns
    AddRoundKey (K1–K13)
        |
        v
  Final Round 14:
    SubBytes
    ShiftRows
    AddRoundKey (K14)
        |
        v
Ciphertext (16 bytes)
```

## How Decryption Works

Decryption reverses the encryption transformations using the expanded round keys in reverse order:

1. Apply `AddRoundKey` with **K14**.
2. For rounds **13 down to 1**, apply `InvShiftRows`, `InvSubBytes`, `AddRoundKey`, and `InvMixColumns`.
3. Finish with `InvShiftRows`, `InvSubBytes`, and `AddRoundKey` using **K0**.
4. Convert the state back to the recovered 16-byte plaintext block.

## Getting Started

### Requirements

- Python **3.9 or newer** (the implementation uses built-in generic type annotations such as `list[int]`).
- A terminal or command prompt.

No third-party packages or `requirements.txt` file are necessary for the supplied implementation.

### Installation

Clone your GitHub repository (replace `<your-username>` and `<repository-name>` with the actual values):

```bash
git clone https://github.com/<your-username>/<repository-name>.git
cd <repository-name>
```

Alternatively, download the repository ZIP from GitHub and extract it.

### Run the Demonstration

From the **project root**, run:

```bash
python main.py
```

If your system uses `python3`:

```bash
python3 main.py
```

The program prints the input plaintext and key, all 15 expanded round keys, the state after each transformation, the final ciphertext, the recovered plaintext, and verification messages.

## Verification with a Standard AES-256 Test Vector

The supplied `main.py` includes this known-answer test case:

**Plaintext (16 bytes)**

```text
00112233445566778899AABBCCDDEEFF
```

**Key (32 bytes)**

```text
000102030405060708090A0B0C0D0E0F101112131415161718191A1B1C1D1E1F
```

**Expected ciphertext (16 bytes)**

```text
8EA2B7CA516745BFEAFC49904B496089
```

### Verified Result

The supplied block encryption and decryption functions were executed with this test vector during README preparation:

| Check | Result |
| --- | --- |
| Encrypted ciphertext matches the expected test vector | **PASS** |
| Decrypted ciphertext equals the original plaintext | **PASS** |

The demonstration in `main.py` also reports success or failure for both checks. These checks validate this specific test vector; they do not constitute a comprehensive security audit.

## Using the Block Cipher from Python

The functions can also be called directly:

```python
from aes.encrypt_block import encrypt_block
from aes.decrypt_block import decrypt_block

plaintext = bytes.fromhex("00112233445566778899AABBCCDDEEFF")
key = bytes.fromhex(
    "000102030405060708090A0B0C0D0E0F"
    "101112131415161718191A1B1C1D1E1F"
)

ciphertext = encrypt_block(plaintext, key, show_steps=False)
recovered = decrypt_block(ciphertext, key, show_steps=False)

print("Ciphertext:", ciphertext.hex().upper())
print("Recovered: ", recovered.hex().upper())
assert recovered == plaintext
```

Both functions require exactly **16 bytes of block data** and a **32-byte key**. The optional `show_steps` argument controls intermediate state printing; it defaults to `True`.

## Scope and Security Limitations

This repository demonstrates the **AES-256 block primitive**, rather than a complete encryption protocol:

- It processes **one 16-byte block per call**; it does not provide multi-block message handling or padding.
- It does **not** implement CBC, CTR, GCM, or any other block cipher mode.
- It does **not** provide authentication or tamper detection.
- It does **not** handle random nonces/IVs or production key management.
- The Python implementation is intended for clarity and is **not designed or audited for side-channel resistance**.
- The test key and plaintext in `main.py` are **public demonstration values**, not secrets.

**Do not use this implementation to protect real passwords, files, personal information, or production traffic.** Use a well-maintained cryptographic library and an authenticated encryption mode such as AES-GCM instead.

## Educational Objectives

This project is intended to help learners understand:

- AES state representation and column-major byte ordering.
- Substitution, permutation, diffusion, and round-key addition.
- Finite-field multiplication and polynomial reduction in GF(2⁸).
- AES-256 key scheduling and its difference from AES-128.
- How encryption transformations are inverted during decryption.
- How to validate a cryptographic implementation using known-answer tests.

## References

- [NIST FIPS 197 — Advanced Encryption Standard (AES)](https://doi.org/10.6028/NIST.FIPS.197)

## Author

**Umme Arifa Zaman Nirjhor**

**Educational** Python implementation for learning and demonstrating **AES-256 internals**.
