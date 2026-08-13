# PII Redaction Tool

A professional, high-fidelity hybrid PII (Personally Identifiable Information) Redaction and Pseudonymization Tool designed to automatically detect, redact, and replace sensitive data within Microsoft Word (`.docx`) corporate documents. 

This tool is optimized for Indian corporate filings (such as Red Herring Prospectuses) and handles complex formatting, multi-run text splits, linked headers/footers, and massive nested tables without disrupting formatting, styling, or generic financial and business terminology.

---

## 1. Project Structure

```text
pii-redaction-tool/
├── input/
│   └── Red Herring Prospectus.docx       # Input document
├── output/
│   ├── Redacted_Red_Herring_Prospectus.docx # Redacted output document
│   └── verification_summary.txt          # Automated leak detection report
├── src/
│   ├── __init__.py
│   ├── pii_detector.py                   # 9-category regex & rules engine
│   ├── redactor.py                       # Faker-based deterministic pseudonymizer
│   ├── document_processor.py             # Docx XML runs, tables, & headers processor
│   └── main.py                           # Orchestrator & verification script
├── evaluation/
│   ├── ground_truth.json                 # Curated evaluation dataset (pos/neg segments)
│   ├── evaluate.py                       # Performance metrics calculation script
│   └── evaluation_report.md              # Computed metrics & category report
├── tests/
│   ├── __init__.py
│   ├── test_detectors.py                 # Tests for all 9 detectors (pos/neg cases)
│   ├── test_redaction.py                 # Tests for mapping consistency
│   └── test_evaluation.py                # Tests for metric calculations
├── requirements.txt                      # Project dependencies
└── run_redaction.py                      # Main entrypoint script
```

---

## 2. Requirements & Installation

This tool requires **Python 3.8+** and utilizes `python-docx` for document manipulation and `faker` for generating realistic synthetic data.

1. Navigate to the project root directory:
   ```bash
   cd pii-redaction-tool
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## 3. Usage

### A. Run Redaction Pipeline
Processes the input document, redacts all PII, saves the redacted file, and automatically executes a post-redaction verification scan for residual leaks:
```bash
python run_redaction.py
```
* **Input Path**: `pii-redaction-tool/input/Red Herring Prospectus.docx`
* **Output Path**: `pii-redaction-tool/output/Redacted_Red_Herring_Prospectus.docx`
* **Verification Log**: `pii-redaction-tool/output/verification_summary.txt`

### B. Run Independent Evaluation
Evaluates the detector and redactor against the manually curated ground-truth dataset (containing actual RHP PII and hard negatives) to calculate precision, recall, and accuracy:
```bash
python evaluation/evaluate.py
```
* **Output Report**: `pii-redaction-tool/evaluation/evaluation_report.md`

### C. Run Unit Tests
Executes the comprehensive unit test suite covering detectors, mappings, and evaluations:
```bash
python -m unittest discover -s tests -p "test_*.py"
```

---

## 4. Technical Architecture

### A. 9-Category Detection Engine (`src/pii_detector.py`)
Features individual rule-based and regex detectors for:
* **Full Names**: Preceded by titles (`Mr.`, `Shri`, `Smt.`, `Dr.`) or context words (`Contact Person:`, `Compliance Officer:`, etc.). Integrates a whitelist of known promoters/officers and a blacklist of business terms.
* **Email Addresses**: robust email-address regular expression.
* **Phone Numbers**: Captures Indian landlines and mobiles with country codes (+91), spaces, and area codes. Excludes monetary figures by requiring contextual labels (`Tel`, `Mobile`, `Phone`).
* **Company Names**: Capitalized word chains ending in suffixes like `Limited`, `Private Limited`, `LLP`, `Corporation`, etc. Excludes blacklisted terms.
* **Mailing Addresses**: Captured via Registered/Corporate Office labels, street/village keywords, and Indian PIN codes (6-digit patterns).
* **DOB**: Evaluates date patterns *only* when accompanied by birth context (`DOB`, `born`, `birth`, `date of birth`).
* **Credit Cards**: Matches digit groupings and validates authenticity using the **Luhn Algorithm**.
* **IP Addresses**: Validates numeric ranges (0–255) for IPv4 octets.
* **Social Security Numbers (SSN)**: Standard US format pattern.

### B. Deterministic Pseudonymizer (`src/redactor.py`)
Ensures that the same original PII entity always maps to the same realistic synthetic alternative. It generates:
* Real Indian and Western names (using `faker` seed engines).
* Consistent email mappings (e.g. `sarthak@ksh.com` -> `sarthak@example.com`).
* Deduplicated synthetic values to prevent collision (two different original names mapping to the same fake name).

### C. Docx Runs & Tables Processor (`src/document_processor.py`)
Modifies Word XML directly to preserve fonts, colors, styles, and spacing:
* **Single-Replacement Loop**: Replaces PII spans character-by-character and runs detection iteratively after each replacement. This avoids the run-offset shifting bug that breaks standard right-to-left index redaction in complex documents.
* **Merged Cells Deduplication**: Avoids processing duplicate cell elements caused by merged cells in Word tables using XML element ID hashing (`cell._tc`).
* **Table Header Column Mapping Heuristics**: Dynamically scans row 0 headers (e.g., column labeled "Name" or "Address") to map and redact column cells, using cell-value type validation to filter out blank entries, NA placeholders, and mismatch types.
* **Deduplicated Headers/Footers**: Tracks processed sections to avoid double-processing linked headers or footers, preventing double-redaction bugs.

---

## 5. Performance Metrics Summary

Based on the evaluation against the manually verified ground-truth dataset (`evaluation/ground_truth.json`):

The tool achieved 100% precision, recall, and accuracy on the curated ground-truth evaluation set.

> [!IMPORTANT]
> **Evaluation Scope & Limitation**  
> The reported metrics represent performance on the manually curated 56-case ground-truth evaluation set. They should not be interpreted as a universal guarantee of 100% performance on unseen documents or arbitrary PII patterns. The tool is not claimed to be universally 100% accurate.

### Evaluation Metrics & Methodology

The metrics are computed using the following standard definitions:
* **True Positive (TP)**: Expected PII that was successfully detected and correctly typed.
* **False Positive (FP)**: Non-PII (negative example) that was incorrectly flagged by the detector.
* **False Negative (FN)**: Expected PII that was missed by the detector.
* **True Negative (TN)**: Expected non-PII that was correctly left alone by the detector.

**Formulas:**
* **Precision** = $\frac{\text{TP}}{\text{TP} + \text{FP}}$
* **Recall** = $\frac{\text{TP}}{\text{TP} + \text{FN}}$
* **Accuracy** = $\frac{\text{TP} + \text{TN}}{\text{TP} + \text{TN} + \text{FP} + \text{FN}}$

### Evaluation Results (56 Labeled Cases)
* **Positive Cases**: 29
* **Negative/Hard-Negative Cases**: 27
* **Total Labeled Cases**: 56

**Results Summary:**
* **True Positives (TP)**: 29
* **False Positives (FP)**: 0
* **False Negatives (FN)**: 0
* **True Negatives (TN)**: 27
* **Precision**: 100%
* **Recall**: 100%
* **Accuracy**: 100%

### Category Breakdown
* **FULL_NAME**: Precision: 100.00% | Recall: 100.00% | Accuracy: 100.00%
* **EMAIL**: Precision: 100.00% | Recall: 100.00% | Accuracy: 100.00%
* **PHONE**: Precision: 100.00% | Recall: 100.00% | Accuracy: 100.00%
* **COMPANY**: Precision: 100.00% | Recall: 100.00% | Accuracy: 100.00%
* **ADDRESS**: Precision: 100.00% | Recall: 100.00% | Accuracy: 100.00%
* **SSN / Credit Card / IP / DOB**: Precision: 100.00% | Recall: N/A (0 positive cases in document) | Accuracy: 100.00%

### Post-Redaction Leak Verification Results
The automated post-redaction leak verification scan (which parses all text from the output document and checks if any original mapped PII is still present) reports:
No original PII values identified in the source document remained in the generated output.

* **Secondary detector candidate matches**: **37** (All 37 are verified **False Positives** triggered by our high-fidelity synthetic replacements being matched by the detector again; none of them represent original PII leakage)
