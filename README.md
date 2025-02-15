# Open-AutoTools

Open-AutoTools is an innovative project developed in Python, specifically designed to offer a suite of automated tools directly accessible via the terminal. This project aims to simplify and automate daily tasks for developers and terminal users, such as converting text to uppercase.

https://github.com/BabylooPro/Open-AutoTools/assets/35376790/d57f2b9d-55f8-4368-bb40-c0010eb9d49a

## Installation

To install Open-AutoTools, use the following command in your terminal: `pip install open-autotools`

This command installs all the necessary tools to integrate Open-AutoTools into your workflow.

## Key Features

### AutoCaps

- **Description:** Converts any text entered by the user to uppercase.
- **Usage:**
  ```
  ~ ❯ autocaps "Your text here."
  ```
- **Output:**
  ```
  YOUR TEXT HERE.
  ```

### AutoPassword

- **Description:** Generates secure random passwords and encryption keys with customizable options.
- **Usage:**
  ```
  ~ ❯ autopassword --length 16
  ~ ❯ autopassword --no-special --length 8
  ~ ❯ autopassword --gen-key
  ~ ❯ autopassword --password-key "your-password" --analyze
  ```
- **Options:**
  - `--length, -l`: Set password length (default: 12)
  - `--no-uppercase`: Exclude uppercase letters
  - `--no-numbers`: Exclude numbers
  - `--no-special`: Exclude special characters
  - `--min-special`: Minimum number of special characters (default: 1)
  - `--min-numbers`: Minimum number of numbers (default: 1)
  - `--gen-key`: Generate a random encryption key
  - `--password-key`: Generate an encryption key from a password
  - `--analyze`: Show password strength analysis

These examples demonstrate how the terminal will display the results after executing each command, providing a straightforward way for users to understand the immediate effects of these commands.

### AutoTranslate

- **Description:** Translates text between languages with automatic source language detection.
- **Usage:**

  ```
  ~ ❯ autotranslate "Bonjour le monde" --to en
  Hello world

  ~ ❯ autotranslate "Hello world" --to fr --copy
  Bonjour le monde
  // Result also copied to clipboard

  ~ ❯ autotranslate "こんにちは" --to en --detect
  [Detected: ja] Hello

  ~ ❯ autotranslate --list-languages
  // Shows all supported languages
  ```

- **Options:**
  - `--to`: Target language code (default: en)
  - `--from`: Source language code (default: auto-detect)
  - `--copy`: Copy translation to clipboard
  - `--detect`: Show detected source language
  - `--list-languages`: Show all supported language codes and names

## General Usage

Open-AutoTools is designed to be used as a set of CLI commands, making its features directly accessible from the user's terminal.

## Technologies, Frameworks, Libraries, and APIs

- **Programming Language:** Python (3.8 or higher)
- **Frameworks and Libraries:**
  - Click (CLI framework)
  - deep-translator (Translation)
  - langdetect (Language detection)

## Contributing

This project is a work in progress, and we welcome any contributions that can help improve Open-AutoTools. If you're interested in contributing, please check the project's issues or submit a pull request.

## License

This project is licensed under the MIT License. For more details, see the [LICENSE](LICENSE) file.

---

For more information and updates, please follow the project's GitHub repository.
