# Secure Password Manager

A simple, secure, and user-friendly desktop application developed as a university project to help users manage their credentials efficiently. This project demonstrates the practical application of **Model-View-Controller (MVC)** design patterns, secure cryptographic protocols, and relational database management.


## Key Features
* **Secure Authentication**: A robust login and sign-up system using encrypted user credentials.
*  **Dynamic Category Management**: Users can organize accounts into custom categories (Add, Edit, and Remove).
*  **Full Account CRUD**: Comprehensive interface to add, edit, and delete account details including URLs, notes, and private notes.
*  **Cryptographic Security**: Implementation of authenticated encryption for sensitive data.
*  **Password Generator**: Built-in tool to create strong, random passwords using a mix of alphanumeric characters and symbols.
*  **Intuitive UI**: A responsive interface built with PyQt5, featuring password masking and quick-search functionality.
*  **Undo System**: Recovery mechanism for accidental account deletions.

---

## Technical Stack
*  **Language**: Python 3.12[cite: 48].
*  **Framework**: **PyQt5** for Cross-platform GUI development.
*  **ORM**: **SQLModel** (built on SQLAlchemy) for professional database abstractions.
*  **Database**: **SQLite** for lightweight, local storage.
* **Security**: 
    *  **Fernet (AES-128)**: For symmetric authenticated encryption of stored passwords.
    *  **PBKDF2HMAC (SHA256)**: For secure key derivation from user master passwords.
*  **Utilities**: `pyperclip` for secure clipboard management and `secrets` for cryptographically strong entropy.

---

## System Architecture
 The application follows a modular **MVC** architecture to ensure separation of concerns and maintainability:

*  **Models**: Defined using `SQLModel` classes (`Users`, `Category`, `Table_widget`) to manage the relational database schema.
*  **Views**: Designed using **Qt Designer** and compiled into modular Python classes (`Ui_Login`, `Ui_MainWindow`).
*  **Controllers**: Logic is encapsulated in specialized handlers that manage user interactions and bridge the gap between the UI and the database.

---

##  Installation & Setup
1.   **Environment**: Ensure Python 3.12 is installed.
2.  **Dependencies**: Install the required libraries using the provided requirements file:
    ```bash
    pip install pyperclip PyQt5 cryptography sqlmodel
    ```
3.  **Run**: Execute the main entry point to launch the application:
    ```bash
    python main.py
    ```

---

## Academic Context
This project was developed as a final assignment for **EE202**.  The repository includes comprehensive documentation, UML diagrams, and reflections on design challenges—such as implementing robust undo functionality and securing local key persistence[cite: 110, 116, 318, 321].

---
*Developed by Group B at King Abdulaziz University.*
