# 🔐 Secure Steganography System

## Project Overview

The Secure Steganography System is a Python-based desktop application that combines steganography and cryptography to securely hide confidential messages inside digital media.

The application provides a graphical user interface built with Tkinter and allows users to hide encrypted messages inside image, video, and audio files.

The project uses a hybrid encryption approach combining AES-256 and RSA-2048. The secret message is encrypted using AES, while the AES encryption key is protected using RSA public-key encryption.

The system also uses password-based protection for the encrypted private key and the encrypted message.

## ✨ Features

- Hide encrypted secret messages inside images
- Hide encrypted messages inside video files
- Hide encrypted messages inside audio files
- Extract and decrypt hidden messages
- AES-256 encryption for secret messages
- RSA-2048 encryption for AES keys
- Password-protected RSA private key
- Separate passwords for private key protection and message encryption
- Password security strength meter
- Secure random password generation
- Show/hide password functionality
- Show/hide secret message functionality
- Image preview
- Audio playback controls
- Support for multiple image formats
- Support for multiple audio formats
- Support for multiple video formats
- Dark-themed graphical user interface

## 🔐 Security Architecture

The system uses a hybrid encryption mechanism.

### Message Encryption

The secret message is encrypted using AES-256 encryption.

The AES key is derived from the message encryption password using SHA-256.

### RSA Key Protection

A unique RSA-2048 key pair is generated for each encryption operation.

The AES encryption key is encrypted using the RSA public key with RSA-OAEP.

The RSA private key is encrypted using AES-256 with a separate private-key password.

This creates two layers of password protection:

1. Private Key Password
2. Message Encryption Password

### Encryption Workflow

```text
Secret Message
      │
      ▼
Message Encryption Password
      │
      ▼
SHA-256 Key Derivation
      │
      ▼
AES-256 Encryption
      │
      ▼
Encrypted Message
      │
      │
      ▼
AES Encryption Key
      │
      ▼
RSA-2048 Public Key
      │
      ▼
RSA-OAEP Encryption
      │
      ▼
Encrypted AES Key
      │
      │
      ▼
RSA Private Key
      │
      ▼
AES-256 Encryption
      │
      ▼
Password-Protected Private Key
```

## 🖼️ Image Steganography

For image files, the application uses Least Significant Bit (LSB) steganography.

The encrypted payload is converted into binary data and stored in the least significant bits of the RGB pixel values.

Supported image formats include:

- PNG
- JPG
- JPEG
- BMP

The resulting encoded image is saved as a PNG file.

## 🎵 Audio and 🎥 Video Steganography

For audio and video files, the application uses an EOF (End of File) based data-hiding technique.

The encrypted payload is appended to the end of the original media file using a custom marker.

The application supports media formats including:

### Audio

- MP3
- MP2
- WAV
- M4A
- FLAC

### Video

- MP4
- MKV
- AVI
- MOV

## 🖥️ Graphical User Interface

The application provides a dark-themed Tkinter interface with:

- Secret Message input
- Message visibility toggle
- Private Key Password input
- Public Key Password input
- Password visibility toggle
- Password security meter
- Random password generator
- Media carrier selection
- Image preview
- Audio playback controls
- Hide In Image button
- Hide In Video/Audio button
- Extract Message button

## 📂 Project Structure

```text
Secure-Steganography-System/
│
├── stego.py
├── steg_utils.py
├── requirements.txt
└── README.md
```

## 🛠️ Technologies Used

- Python
- Tkinter
- Pillow
- Pygame
- PyCryptodome
- AES-256
- RSA-2048
- RSA-OAEP
- SHA-256
- LSB Steganography
- EOF-based Data Hiding

## 📦 Installation

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Open the Project Folder

```bash
cd Secure-Steganography-System
```

### 3. Install Required Libraries

```bash
pip install -r requirements.txt
```

## ▶️ How to Run

Run the application using:

```bash
python stego.py
```

The graphical user interface will open.

## 🔒 Hiding a Secret Message in an Image

1. Run the application.
2. Enter your secret message.
3. Enter a Private Key Password.
4. Enter a Message Encryption Password.
5. Click `Browse & Select File`.
6. Select an image.
7. Click `Hide In Image`.
8. Select the location where you want to save the encoded image.
9. The encrypted message will be hidden inside the output image.

## 🎵 Hiding a Secret Message in Audio or Video

1. Run the application.
2. Enter your secret message.
3. Enter a Private Key Password.
4. Enter a Message Encryption Password.
5. Select an audio or video file.
6. Click `Hide In Video/Audio`.
7. Choose the output file location.
8. The encrypted message will be embedded into the output media file.

## 🔓 Extracting a Hidden Message

1. Run the application.
2. Click `Browse & Select File`.
3. Select the encoded image, audio, or video file.
4. Enter the Private Key Password used during encryption.
5. Enter the Message Encryption Password used during encryption.
6. Click `Extract Message`.
7. If the passwords are correct, the hidden message will be decrypted and displayed.

## 🔑 Password Security

The application uses two separate passwords:

### Private Key Password

Protects the RSA private key using AES-256 encryption.

### Message Encryption Password

Used to derive the AES-256 key used for message encryption.

The application also provides a password security meter that evaluates:

- Password length
- Uppercase characters
- Lowercase characters
- Numbers
- Special characters

A random 16-character password can also be generated using the built-in password generator.

## ⚠️ Security Note

This project is an educational cryptographic steganography application.

For production-grade security, additional measures should be considered, including authenticated encryption such as AES-GCM, secure key derivation functions such as Argon2 or PBKDF2, stronger integrity verification, secure password storage practices, and protection against tampering.

## 🚀 Future Improvements

- Add AES-GCM authenticated encryption
- Add PBKDF2 or Argon2 password-based key derivation
- Add message integrity verification
- Add digital signatures
- Add support for additional media formats
- Improve large-file handling
- Add secure key management
- Add user authentication
- Add file integrity verification
- Add drag-and-drop file selection

## 👨‍💻 Author

**Rizwa Hassan**

Computer Science Student
