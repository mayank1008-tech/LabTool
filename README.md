# LabTool 🚀

> **"Trust the process && U Are the process"** - Mayank Jain

**LabTool** is a powerful, cross-platform lab report generator that converts your source code into a print-ready Word (`.docx`) document in seconds. It ships as a **FastAPI web service** with a minimal browser UI, a JSON-driven template profile system, and — as of **M2** — a full DOCX template upload and field-mapping workflow.

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-teal?style=for-the-badge&logo=fastapi)
![Platform](https://img.shields.io/badge/Platform-Windows%20|%20Linux%20|%20MacOS-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-M2%20Release-brightgreen?style=for-the-badge)

---

## 🆕 M2 – Template Upload & Mapping (current)

Upload an existing `.docx` lab-report template, let LabTool suggest field mappings, confirm/adjust them in a simple UI, and save a reusable profile — all without touching JSON manually.

### 📁 Project Structure (M2)

```
app/
├── main.py                          # FastAPI app + route registration
├── core/config.py                   # App settings and storage paths
├── models/schemas.py                # Pydantic schemas (M1 + M2)
├── api/
│   ├── routes_profiles.py           # POST /profiles, GET /profiles/{id}
│   ├── routes_generate.py           # POST /generate, GET /download/{filename}
│   └── routes_templates.py          # M2: upload / suggest / from-template
├── services/
│   ├── profile_service.py           # Profile persistence (JSON files)
│   ├── docx_builder.py              # python-docx document assembly
│   ├── generator_service.py         # Orchestrates profile + builder
│   ├── template_extract_service.py  # M2: DOCX parsing & metadata extraction
│   └── mapping_service.py           # M2: heuristic field-mapping suggestions
├── storage/
│   ├── profiles/                    # Saved profile JSON files
│   ├── generated/                   # Generated .docx files
│   ├── templates/                   # Uploaded .docx template files
│   └── template_meta/               # Extracted metadata JSON files
└── templates/
    ├── index.html                   # Generate report UI
    ├── upload.html                  # M2: template upload UI
    └── confirm_mapping.html         # M2: mapping confirmation UI
```

### 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the server
uvicorn app.main:app --reload

# 3. Open the web UI
# http://127.0.0.1:8000/                  ← Generate report (M1)
# http://127.0.0.1:8000/upload-template   ← Upload template (M2)
# http://127.0.0.1:8000/docs              ← API docs
```

### 🔌 API Endpoints

#### M1 Endpoints (unchanged)

##### `POST /profiles` – Create a template profile manually

```bash
curl -X POST http://127.0.0.1:8000/profiles \
  -H "Content-Type: application/json" \
  -d '{
    "id": "java-default",
    "name": "Java Lab Default",
    "heading_style": {"font_family": "Times New Roman", "font_size": 16, "bold": true},
    "experiment_number_label": "Program",
    "aim_section": {
      "label": "Aim:- ",
      "label_style": {"font_size": 14, "bold": true, "underline": true},
      "body_style":  {"font_size": 12}
    },
    "source_code_section": {
      "label": "SOURCE CODE:-",
      "label_style": {"font_size": 14, "bold": true, "underline": true},
      "body_style":  {"font_family": "Courier New", "font_size": 11}
    },
    "output_section": {
      "label": "OUTPUT:-",
      "label_style": {"font_size": 14, "bold": true, "underline": true},
      "body_style":  {"font_size": 12, "italic": true}
    },
    "output_placeholder": "[ PASTE SCREENSHOT HERE ]"
  }'
```

##### `GET /profiles/{id}` – Fetch a profile

```bash
curl http://127.0.0.1:8000/profiles/java-default
```

##### `POST /generate` – Generate a `.docx` report

```bash
curl -X POST http://127.0.0.1:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "profile_id": "java-default",
    "experiment_number": "1",
    "aim": "Write a Java program to print Hello World",
    "source_code": "public class Hello {\n  public static void main(String[] args) {\n    System.out.println(\"Hello, World!\");\n  }\n}"
  }'
```

Response:
```json
{
  "filename": "report_java-default_exp1_a1b2c3d4.docx",
  "file_path": "app/storage/generated/report_java-default_exp1_a1b2c3d4.docx",
  "download_url": "/download/report_java-default_exp1_a1b2c3d4.docx",
  "profile_id": "java-default",
  "experiment_number": "1",
  "aim": "Write a Java program to print Hello World"
}
```

##### `GET /download/{filename}` – Download generated file

```bash
curl -O http://127.0.0.1:8000/download/report_java-default_exp1_a1b2c3d4.docx
```

> A ready-to-use default profile (`java-default`) is pre-loaded in `app/storage/profiles/`.

---

#### M2 Endpoints

##### `POST /templates/upload` – Upload a DOCX template

Accepts a `.docx` file, stores it, extracts block metadata, and returns a `template_id`.

```bash
curl -X POST http://127.0.0.1:8000/templates/upload \
  -F "file=@/path/to/your/lab_template.docx"
```

Response:
```json
{
  "template_id": "196e1a88efaf4f5b",
  "original_filename": "lab_template.docx",
  "stored_path": "app/storage/templates/196e1a88efaf4f5b.docx",
  "metadata_path": "app/storage/template_meta/196e1a88efaf4f5b.json",
  "paragraph_count": 6,
  "table_count": 0
}
```

##### `POST /templates/{template_id}/suggest-mapping` – Get heuristic field suggestions

Analyses the extracted metadata and returns scored candidates for `experiment_number`, `aim`, `source_code`, and `output`.

```bash
curl -X POST http://127.0.0.1:8000/templates/196e1a88efaf4f5b/suggest-mapping
```

Response:
```json
{
  "template_id": "196e1a88efaf4f5b",
  "suggestions": [
    {
      "block_index": 0,
      "text_snippet": "Program 1",
      "style_hint": "bold 16.0pt center",
      "confidence": 0.7,
      "field_name": "experiment_number"
    },
    {
      "block_index": 1,
      "text_snippet": "Aim:- To write a Java program...",
      "style_hint": "bold underline 12.0pt",
      "confidence": 0.4,
      "field_name": "aim"
    }
  ]
}
```

##### `POST /profiles/from-template` – Create a profile from confirmed mappings

Takes user-confirmed `block_index → field_name` assignments and saves a fully reusable profile.

```bash
curl -X POST http://127.0.0.1:8000/profiles/from-template \
  -H "Content-Type: application/json" \
  -d '{
    "template_id": "196e1a88efaf4f5b",
    "profile_id": "my-lab-profile",
    "profile_name": "My Lab Template",
    "confirmed_mappings": [
      {"block_index": 0, "field_name": "experiment_number"},
      {"block_index": 1, "field_name": "aim"},
      {"block_index": 2, "field_name": "source_code"},
      {"block_index": 4, "field_name": "output"}
    ]
  }'
```

The returned profile is immediately usable with `POST /generate`:

```bash
curl -X POST http://127.0.0.1:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "profile_id": "my-lab-profile",
    "experiment_number": "3",
    "aim": "To implement bubble sort in Java",
    "source_code": "// your code here"
  }'
```

---

### 🖥 M2 UI Workflow

1. **Open** `http://127.0.0.1:8000/upload-template`
2. **Drag & drop** (or click to browse) your `.docx` lab report template
3. Click **Upload Template** → you are redirected to the confirmation page
4. On the confirmation page:
   - Review each block candidate and its suggested field assignment
   - Adjust any incorrect dropdown selections
   - Enter a **Profile ID** and **Profile Name**
   - Click **Save Profile** once all required fields (aim, source_code, output) are mapped
5. Use the saved profile with `POST /generate` or the Generate Report UI at `/`

---

## ⚡ Features (M1 Web Service)

- **Multi-Language Support:** `.java`, `.py`, `.c`, `.cpp`, `.cs`, and `.js` files.
- **Instant Formatting:** Generates a professional Word (`.docx`) file with Standard Heading, Aim, Source Code, and Output sections.
- **Background Transmission:** Send your report via email in the background (Multi-threaded) so you can start working on the next experiment immediately.
- **Crash Proof:** Intelligent file-locking detection prevents crashes if Microsoft Word is currently open.
- **Style Lab:** Fully customizable fonts, sizes, and styles via the CLI menu.
- **Portable:** No Python installation required. Runs as a standalone `.exe`.

---

## 📥 Installation (No Setup Required)

You do **not** need to install Python or any libraries. Just download the executable.

### ⚠️ IMPORTANT: Installation Location

**Download `LabTool.exe` to the SAME folder where your code files are located.**

For example:
```
📁 My Java Lab/
  ├── LabTool.exe          ← Place the tool here
  ├── Experiment1.java     ← Your code files
  ├── Experiment2.java
  └── HelloWorld.java
```

This way, you can simply type the filename (e.g., `Experiment1.java`) without needing to provide the full file path.

---

### Windows - Quick Install

**Method 1: Download to Your Code Folder**

1. **Navigate to your code folder** in File Explorer
2. **Open PowerShell in that folder** (Shift + Right-click → "Open PowerShell window here")
3. **Run this command:**

```powershell
curl.exe -L -o LabTool.exe "https://github.com/mayank1008-tech/LabTool/releases/latest/download/LabTool.exe"
```

**Method 2: Manual Download**

1. Go to the [Releases Page](https://github.com/mayank1008-tech/LabTool/releases/latest)
2. Download `LabTool.exe`
3. **Move it to the folder containing your code files**

---

## 🛠️ How to Use

### Step 1: Run the Tool
- **Option A:** Double-click `LabTool.exe` 
- **Option B:** Open terminal in the folder and type `LabTool` OR `./LabTool`

> **💡 Tip:** Make sure you're in the folder that contains both `LabTool` AND your code files!

### Step 2: Generate Report
1. Select **Option [1]** from the main menu
2. Enter the filename (e.g., `Experiment1.java`)
   - Just type the filename, not the full path (since LabTool is in the same folder)
3. Enter the Aim of your program

### Step 3: Add Output
1. The tool will generate the Word doc and automatically open it
2. **IMPORTANT:** Take a screenshot of your program's output
3. **PASTE** it manually into the designated section in the Word document
4. **Save and CLOSE** the document

### Step 4: Email (Optional)
The tool will ask if you want to email the file. You can:
- Send it immediately, or
- Send it in the **background** while you continue working on your next experiment

---

## 🔑 Email Configuration (One-Time Setup)

To use the **Auto-Email** feature, the tool requires a Google App Password to securely send emails via SMTP.

### Important Notes:
- ✅ **One-Time Setup:** You only need to enter this key once
- ✅ **Not Your Login Password:** This is a special app-specific password
- ✅ **Secure Storage:** The tool encrypts and saves it locally on your machine

### How to Get an App Password:

Message admin on [LinkedIn](https://www.linkedin.com/in/mayank-jain-78a6bb321/) for setup guidance.

---

# 🎨 Customization Guide

Don't like the default fonts? You can tweak every aspect of the document generation.

## Getting Started

1. Select **Option [2] - Styles** from the main menu.
2. You will see a list of keys (e.g., `h_font`, `c_size`).
3. Select the number corresponding to the setting you want to change.

## 📖 Style Key Guide

The settings use prefixes to indicate which part of the document they affect:

| Prefix | Meaning | Example |
|--------|---------|---------|
| `h_` | **Header** (The main title "Program") | `h_size` = Title font size |
| `l_` | **Label** (Section titles like "Aim:", "Source Code:") | `l_bold` = Make labels bold |
| `b_` | **Body** (The content of your Aim) | `b_font` = Font family for body text |
| `c_` | **Code** (The source code block) | `c_font` = Font used for code (e.g., Consolas) |

## Example Usage

To change the code font size to 10:
- Select `c_size`
- Enter `10`

---

Customize your documents to match your preferred style and formatting!

---

## 📋 Example Usage

```
📁 Current Directory: C:\Users\Student\Java Lab\

$ LabTool.exe

██╗      █████╗ ██████╗ ████████╗ ██████╗  ██████╗ ██╗     
██║     ██╔══██╗██╔══██╗╚══██╔══╝██╔═══██╗██╔═══██╗██║     
██║     ███████║██████╔╝   ██║   ██║   ██║██║   ██║██║     
██║     ██╔══██║██╔══██╗   ██║   ██║   ██║██║   ██║██║     
███████╗██║  ██║██████╔╝   ██║   ╚██████╔╝╚██████╔╝███████╗

--- MAIN COMMAND CENTER ---
[1] Generate Report
[2] Customize Styles
[3] Reset Email Config
[4] Exit

Selection: 1

>> Filename: HelloWorld.java          ← Filename with EXTENSION!!!!
>> Enter Aim: To print "Hello World" using Java

✔ Document Generated: HelloWorld_Report.docx

>> Email file? (y/n): y
>> Destination Email: professor@university.edu
>> Send in background? (y/n): y

✔ Email bot dispatched in background.
```

---

## 🔧 Troubleshooting

### Issue: "File Not Found" Error
**Solution:** 
- **Most Common Cause:** `LabTool.exe` is not in the same folder as your code file
- **Fix:** Move `LabTool.exe` to the folder containing your `.java`, `.py`, or `.c` files
- **Alternative:** Provide the full file path (e.g., `C:\Users\Student\Desktop\Experiment1.java`)

### Issue: "Permission Denied" Error
**Solution:** Close Microsoft Word and try again. The document must be closed before emailing.

### Issue: Email Not Sending
**Solution:** 
1. Check the app password key is correct
2. Enter a valid email address
3. Ensure you have internet connection

---

## 📁 Recommended Folder Structure

For best results, organize your files like this:

```
📁 My Lab Work/
  ├── 📁 Java Experiments/
  │   ├── LabTool.exe              ← Copy here for Java
  │   ├── Experiment1.java
  │   ├── Experiment2.java
  │   └── Experiment1_Report.docx  ← Generated
  │
  ├── 📁 Python Projects/
  │   ├── LabTool.exe              ← Copy here for Python
  │   ├── script1.py
  │   └── script1_Report.docx
  │
  └── 📁 C Programs/
      ├── LabTool.exe              ← Copy here for C
      ├── program1.c
      └── program1_Report.docx
```

**💡 Pro Tip:** Keep a copy of `LabTool.exe` in each of your code folders for convenience!

---

## 🤝 Contributing

Found a bug? Have a feature request? Contributions are welcome!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Developer

**Mayank Jain**

- 🌐 GitHub: [@mayank1008-tech](https://github.com/mayank1008-tech)
- 💼 LinkedIn: [Mayank Jain](https://www.linkedin.com/in/mayank-jain-78a6bb321/)
- 📸 Instagram: [@mank_1008](https://instagram.com/mank_1008)

Built with ❤️ and Python

---

## 🌟 Star This Project!

If LabTool saved you time on your lab reports, give it a ⭐ on GitHub!

---

## 📞 Support

Need help? Have questions?

- 📧 Open an [Issue](https://github.com/mayank1008-tech/LabTool/issues)
- 💬 Connect on [LinkedIn](https://www.linkedin.com/in/mayank-jain-78a6bb321/)
- 📱 DM on Instagram [@mank_1008](https://instagram.com/mank_1008)

---

**Made for students, by a student. Happy coding! 🎓**
