# Gmail to Google Sheets Automation

## 📌 Project Overview
A Python-based automation tool that reads real incoming emails from a Gmail inbox, parses key details (Sender, Subject, Date, Body), and logs them into a Google Sheet. This system uses OAuth 2.0 for secure authentication and implements state management to prevent duplicate entries.

**Author:** Sahil Deore  
**Repository:** [https://github.com/Sahildk/gmail-to-sheets](https://github.com/Sahildk/gmail-to-sheets)  
**Submission Date:** 15-01-2026

---

## 🏗️ Architecture
The system follows a modular ETL (Extract, Transform, Load) pattern:

1.  **Extract:** `gmail_service.py` connects to Gmail API to fetch message IDs labeled `UNREAD`.
2.  **Transform:** `email_parser.py` decodes the complex nested JSON payload from Gmail, extracts plain text, and truncates it to fit Google Sheets limits.
3.  **Load:** `sheets_service.py` appends the cleaned data to the specified Google Sheet.
4.  **State Management:** A local JSON file tracks processed IDs to ensure idempotency.

*(See `proof/` folder for the architecture diagram.)*

---

## ⚙️ Setup Instructions

### 1. Prerequisites
* Python 3.x
* A Google Cloud Project with Gmail and Sheets APIs enabled.

### 2. Installation
1.  Clone the repository:
    ```bash
    git clone [https://github.com/Sahildk/gmail-to-sheets.git](https://github.com/Sahildk/gmail-to-sheets.git)
    cd gmail-to-sheets
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Credentials Setup:**
    * Place your `credentials.json` (OAuth 2.0 Client ID) inside the `credentials/` folder.
    * *Note: This file is git-ignored for security.*
4.  **Configuration:**
    * Open `config.py` and add your `SPREADSHEET_ID`.

### 3. Running the Script
```bash
python src/main.py
