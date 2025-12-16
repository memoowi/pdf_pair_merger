# PDF Pair Merger (N-1 & N-2 → N)

A Python utility to **automatically merge paired PDF files** based on a strict naming convention:

- `N-1.pdf`
- `N-2.pdf`

The script merges each valid pair into a single output file:

- `N.pdf`

This is useful for batch-processing scanned documents, split exam papers, invoices, or any workflow where PDFs are exported in numbered pairs.

---

## 📁 Folder Structure

```bash
project-root/
│
├── source/ # Input PDFs go here
│ ├── 1-1.pdf
│ ├── 1-2.pdf
│ ├── 2-1.pdf
│ ├── 2-2.pdf
│ └── ...
│
├── merged/ # Output PDFs will be generated here
│ ├── 1.pdf
│ ├── 2.pdf
│ └── ...
│
├── merge.py # Main Python script
└── README.md
```


> ⚠️ The script will **automatically create** `source/` and `merged/` folders if they do not exist.

---

## 🧠 How It Works

1. Scans the `source/` directory
2. Detects PDF files matching the format: `N-1.pdf N-2.pdf`
3. Groups files by `N`
4. Merges `N-1.pdf` followed by `N-2.pdf`
5. Writes the result as: `merged/N.pdf`
6. Skips incomplete pairs and logs a warning

---

## 🔧 Requirements

- Python **3.8+**
- `pypdf` library

---

## 🚀 Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/memoowi/pdf_pair_merger.git
cd pdf_pair_merger
```

### 2️⃣ Create a Virtual Environment (Recommended)

#### Linux / macOS
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Install Dependencies
```bash
pip install pypdf
```

---

## 📄 Preparing Input Files

1. Put all input PDFs inside the source/ folder
2. Files must follow this naming format:
   ```
   N-1.pdf
   N-2.pdf
   ```
   ✅ Valid Examples
   ```
   1-1.pdf   + 1-2.pdf  → merged/1.pdf
   12-1.pdf  + 12-2.pdf → merged/12.pdf
   ```
   ❌ Invalid / Skipped
   ```
   3-1.pdf          # Missing 3-2.pdf
   abc-1.pdf        # Invalid number
   4-3.pdf          # Only sub-number 1 or 2 allowed
   ```

---

## ▶️ Running the Script

From the project root:
```bash
python merge.py
```

---


## 🖨️ Console Output Example

```bash
------------------------------
Searching files in: /path/to/source
Output will be saved in: /path/to/merged

Merging 1-1.pdf and 1-2.pdf -> 1.pdf
Merging 2-1.pdf and 2-2.pdf -> 2.pdf
⚠️ Skipping file: 3-1.pdf. Pair is incomplete.

------------------------------
✅ Process finished. Total 2 pairs merged successfully.
```

---

## 📦 Output

- All merged PDFs are saved to: `merged/`
- Output filenames are only the base number: `N.pdf`

---

## 🛡️ Error Handling

- Invalid filenames are silently ignored
- Incomplete pairs are skipped with a warning
- Corrupt or unreadable PDFs will not crash the entire process

---

## 🔄 Customization

You can easily extend this script to:

- Merge more than 2 files per group
- Change file naming rules
- Sort PDFs differently before merging
- Add logging to a file instead of stdout

---

## 📜 License

MIT License — free to use, modify, and distribute.

---

## 🤝 Contributions

Pull requests are welcome.
If you find a bug or want an enhancement, feel free to open an issue.

Happy merging! 📄✨

