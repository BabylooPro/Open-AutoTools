# Open-AutoTools - ***WORK IN PROGRESS (WIP)***
Open-AutoTools is an innovative project developed in Python, specifically designed to offer a suite of automated tools directly accessible via the terminal. This project aims to simplify and automate daily tasks for developers and terminal users, such as converting text to uppercase, automatically correcting text errors, and real-time text translation.

https://github.com/BabylooPro/Open-AutoTools/assets/35376790/d57f2b9d-55f8-4368-bb40-c0010eb9d49a

## Installation
To install Open-AutoTools, use the following command in your terminal: ``pip install open-autotools``

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

### AutoCorrect
- **Description:** Automatically corrects mistakes in any text.
- **Usage:** 
    ```
    ~ ❯ autocorrect "Your text with mistakes here."
    ```
- **Output:**
    ```
    Your text without mistakes here.
    ```
(Note: The exact output for AutoCorrect will vary depending on the mistakes in the input text and the correction applied.)

### AutoTranslate
- **Description:** Translates text from one language to another in real-time, offering users a convenient solution to overcome the language barrier.
- **Usage:** 
    ```
    ~ ❯ autotranslate "Bonjour le monde" --from fr --to en
    ```
- **Output:**
    ```
    Hello world
    ```

These examples demonstrate how the terminal will display the results after executing each command, providing a straightforward way for users to understand the immediate effects of these commands.

## General Usage
Open-AutoTools is designed to be used as a set of CLI commands, making its features directly accessible from the user's terminal.

## Technologies, Frameworks, Libraries, and APIs
- **Programming Language:** Python (3.8 or higher)
- **Frameworks and Libraries:** Click
- **APIs:** Text correction API (multi-language), Text translation API (multi-language)

## Contributing
This project is a work in progress, and we welcome any contributions that can help improve Open-AutoTools. If you're interested in contributing, please check the project's issues or submit a pull request.

## License
This project is licensed under the MIT License. For more details, see the [LICENSE](LICENSE) file.

---

For more information and updates, please follow the project's GitHub repository.
