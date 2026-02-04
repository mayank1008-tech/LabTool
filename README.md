# LabTool 🚀

> **"Trust the process & U Are the process"** - Mayank Jain

**LabTool** is a powerful, cross-platform CLI utility designed to automate the boring process of creating lab reports. Stop manually formatting Word documents—just feed it your code, and let the tool handle the rest.

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Platform](https://img.shields.io/badge/Platform-Windows%20|%20Linux%20|%20MacOS-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen?style=for-the-badge)

---

## ⚡ Features

- **Multi-Language Support:** Auto-detects and formats `.java`, `.py`, `.c`, `.cpp`, `.cs`, and `.js` files.
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
curl -L -o LabTool.exe "https://github.com/mayank1008-tech/LabTool/releases/latest/download/LabTool.exe"
```

**Method 2: Manual Download**

1. Go to the [Releases Page](https://github.com/mayank1008-tech/LabTool/releases/latest)
2. Download `LabTool.exe`
3. **Move it to the folder containing your code files**

---

## 🛠️ How to Use

### Step 1: Run the Tool
- **Option A:** Double-click `LabTool.exe` 
- **Option B:** Open terminal in the folder and type `LabTool.exe`

> **💡 Tip:** Make sure you're in the folder that contains both `LabTool.exe` AND your code files!

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

Message admin on [LinkedIn](https://www.linkedin.com/in/mayank-jain-tech) for setup guidance.

---

## 🎨 Customization

Don't like the default fonts or styles?

1. Select **Option [2] - Customize Styles** from the main menu
2. Customize:
   - Heading Fonts & Sizes
   - Label Styles (Bold/Underline)
   - Body Text Formatting
   - Code Block Font & Size

Your preferences are applied to all future reports!

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

>> Filename: HelloWorld.java          ← Just the filename!
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
- 💼 LinkedIn: [Mayank Jain](https://www.linkedin.com/in/mayank-jain-tech)
- 📸 Instagram: [@mank_1008](https://instagram.com/mank_1008)

Built with ❤️ and Python

---

## 🌟 Star This Project!

If LabTool saved you time on your lab reports, give it a ⭐ on GitHub!

---

## 📞 Support

Need help? Have questions?

- 📧 Open an [Issue](https://github.com/mayank1008-tech/LabTool/issues)
- 💬 Connect on [LinkedIn](https://www.linkedin.com/in/mayank-jain-tech)
- 📱 DM on Instagram [@mank_1008](https://instagram.com/mank_1008)

---

**Made for students, by a student. Happy coding! 🎓**
