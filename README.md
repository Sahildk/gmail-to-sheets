# Gmail to Google Sheets Automation

## 📌 Project Overview
A Python-based automation tool that reads real incoming emails from a Gmail inbox, parses key details (Sender, Subject, Date, Body), and logs them into a Google Sheet. This system uses OAuth 2.0 for secure authentication and implements state management to prevent duplicate entries.

**Author:** Sahil Deore
**Repository:** [https://github.com/Sahildk/gmail-to-sheets](https://github.com/Sahildk/gmail-to-sheets)
**Submission Date:** 15-01-2026

---

## 🏗️ High-Level Architecture
The system follows a modular ETL (Extract, Transform, Load) pattern:

1.  **Extract:** `gmail_service.py` connects to Gmail API to fetch message IDs labeled `UNREAD`.
2.  **Transform:** `email_parser.py` decodes the complex nested JSON payload from Gmail, extracts plain text, and truncates it to fit Google Sheets limits.
3.  **Load:** `sheets_service.py` appends the cleaned data to the specified Google Sheet.
4.  **State Management:** A local JSON file tracks processed IDs to ensure idempotency.

[Architecture Diagram]<img width="1065" height="1280" alt="image" src="https://github.com/user-attachments/assets/b1250eb1-d517-4b44-a829-e7491cbd089c" />


---

## ⚙️ Step-by-Step Setup Instructions


### 1. Prerequisites
* Python 3.x installed.
* A Google Cloud Project with **Gmail API** and **Google Sheets API** enabled.

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
    * Download your OAuth 2.0 Client ID JSON from Google Cloud Console.
    * Rename it to `credentials.json`.
    * Place it inside the `credentials/` folder.
    * *Note: This file is git-ignored for security.*
4.  **Configuration:**
    * Open `config.py`.
    * Update `SPREADSHEET_ID` with the ID from your target Google Sheet URL.

### 3. Running the Script
```bash
python src/main.py
