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
```

## 🛡️ Technical Design & Logic

### 1. OAuth Flow Used

The application uses **OAuth 2.0 Authorization Code Flow** via the `InstalledAppFlow` strategy.

- **Initial Run**
  - The script checks for a local `credentials/token.json`.
  - If missing, it launches a local server to capture user consent via the browser.

- **Token Caching**
  - On successful authorization, the **Access Token** and **Refresh Token** are cached locally in `token.json`.

- **Security**
  - Enables subsequent executions without user intervention.
  - Keeps sensitive secrets (`credentials.json`) isolated from the codebase.

---

### 2. Duplicate Prevention Logic

To enforce **append-only behavior** and **zero duplicate rows**, a dual-layer strategy is used:

#### Primary Mechanism (API Level)
- Emails are queried using:
```
label:UNREAD
```
- After successful processing, the script removes the `UNREAD` label via the Gmail API.
- This ensures processed emails are never fetched again.

#### Secondary Mechanism (Application Level)
- Before inserting a row into Google Sheets, the script checks the unique **Gmail Message ID** against a local history list.
- If the ID already exists, the email is skipped.

---

### 3. State Persistence Method

A lightweight local JSON file is used for state management:
```
processed_emails.json
```

**Rationale:**
- Ensures idempotency across runs.
- If the script crashes after writing to Sheets but before updating Gmail state, the local file prevents duplicate rows on the next execution.

---

## ⚠️ Challenges & Solutions

### Challenge: Google Sheets Cell Character Limit (HttpError 400)

**Problem**  
The script crashed when processing very long email threads due to the Google Sheets API hard limit of **50,000 characters per cell**.

**Solution**
- Implemented strict truncation logic in `email_parser.py`.
- The parser validates email body length before insertion.
- Content exceeding **4,000 characters** is truncated and suffixed with:
```
... (TRUNCATED)
```

**Result**
- Eliminated API crashes entirely.
- Preserved the most relevant email context.

---

### Challenge: Parsing Multipart Emails

**Problem**  
Gmail API returns email bodies in complex nested `multipart/*` structures with Base64URL encoding.

**Solution**
- Implemented a recursive MIME parser in `email_parser.py`.
- Prioritizes `text/plain` MIME types.
- Falls back to the main body payload if plain text is unavailable.
- Handles Base64URL decoding internally.

---

## 🛑 Limitations

- **Local State Dependency**
-     `processed_emails.json` is stored locally.
-     Migrating the script to another machine or container without this file resets processing history.

- **Plain Text Focus**
-     HTML tags are stripped for Google Sheets readability.
-     HTML-heavy emails (e.g., newsletters) may lose formatting.

- **No Attachment Support**
-     Attachments are ignored.
-     Only textual email content is processed.

---

## 🚀 Bonus Features Implemented

- **HTML → Plain Text Conversion**
-     Prioritizes `text/plain` MIME parts.
-     Falls back to HTML parsing with tag stripping when required.

- **Structured Logging**
-     Uses Python’s `logging` module with timestamps:
      ```
      %(asctime)s - %(levelname)s - %(message)s
      ```
-     Replaces basic `print` statements for professional debugging and auditability.
