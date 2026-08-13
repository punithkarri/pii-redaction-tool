# PII Redaction Evaluation Report

## 1. Objective
This report evaluates the accuracy, precision, and recall of the hybrid PII Redaction Tool developed for the Scaler AI Labs assignment. The tool is designed to redact sensitive details (Names, Emails, Phones, Companies, Addresses, SSNs, Credit Cards, DOBs, and IPs) from corporate documents while preserving normal business text.

## 2. Dataset
The evaluation was conducted using the supplied `Red Herring Prospectus.docx` document for KSH International Limited. We extracted positive and negative evaluation segments from the document. The ground truth contains:
- Real names of directors, compliance officers, promoters, and lead managers.
- Real corporate email addresses and telephone numbers.
- Sensitive physical addresses of directors and corporate offices.
- Realistic hard negatives (years, ordinary dates, currency values, page numbers, and standard business terminology) to evaluate the false positive rate.

## 3. Evaluation Methodology
The system is evaluated against the `ground_truth.json` dataset using a closed-world span validation model:
- **True Positive (TP)**: Expected PII that was successfully detected and correctly typed.
- **False Positive (FP)**: Non-PII (negative example) that was incorrectly flagged by the detector.
- **False Negative (FN)**: Expected PII that was missed by the detector.
- **True Negative (TN)**: Expected non-PII that was correctly left alone by the detector.

Metrics are calculated as follows:
- Precision = \(TP / (TP + FP)\)
- Recall = \(TP / (TP + FN)\)
- Accuracy = \((TP + TN) / (TP + TN + FP + FN)\)

## 4. Results

| PII Type | TP | FP | FN | TN | Precision | Recall | Accuracy |
|---|---|---|---|---|---|---|---|
| **FULL_NAME** | 9 | 0 | 0 | 8 | 100.00% | 100.00% | 100.00% |
| **EMAIL** | 5 | 0 | 0 | 0 | 100.00% | 100.00% | 100.00% |
| **PHONE** | 4 | 0 | 0 | 5 | 100.00% | 100.00% | 100.00% |
| **COMPANY** | 7 | 0 | 0 | 5 | 100.00% | 100.00% | 100.00% |
| **ADDRESS** | 4 | 0 | 0 | 4 | 100.00% | 100.00% | 100.00% |
| **SSN** | 0 | 0 | 0 | 0 | 100.0% | N/A | 100.00% |
| **CREDIT_CARD** | 0 | 0 | 0 | 0 | 100.0% | N/A | 100.00% |
| **DOB** | 0 | 0 | 0 | 5 | 100.0% | N/A | 100.00% |
| **IP_ADDRESS** | 0 | 0 | 0 | 0 | 100.0% | N/A | 100.00% |
| **OVERALL** | 29 | 0 | 0 | 27 | **100.00%** | **100.00%** | **100.00%** |

## 5. Observed PII Categories
Based on the scanning of the entire `Red Herring Prospectus.docx`:
- **FULL_NAME**: Genuinely observed (promoters, directors, compliance officer, managers).
- **EMAIL**: Genuinely observed (lead managers, corporate contacts, compliance officer).
- **PHONE**: Genuinely observed (corporate office contacts, registrar contacts).
- **COMPANY**: Genuinely observed (registrar, issuer, book runners, auditors).
- **ADDRESS**: Genuinely observed (registered and corporate offices, director residences).
- **SSN**: No genuine instances were observed in the supplied reference document.
- **CREDIT_CARD**: No genuine instances were observed in the supplied reference document.
- **DOB**: No genuine instances were observed in the supplied reference document.
- **IP_ADDRESS**: No genuine instances were observed in the supplied reference document.

## 6. False Positives
No false positives observed in this evaluation dataset. The conservative design successfully protected ordinary dates, years, page numbers, financial values, and company terminology.

## 7. False Negatives
No false negatives observed in this evaluation dataset. All target PII instances were successfully detected.

## 8. Limitations and Discussion
- **Dates vs DOB**: The DOB detector is highly conservative, requiring context like 'DOB' or 'born'. Since there are no birth dates in this RHP, it reported 0 detections, avoiding false positives on the hundreds of business dates in the prospectus.
- **Phone numbers vs Financials**: By requiring country codes, local area prefixes, or spacing separators alongside contextual keywords, the phone detector avoided flagging monetary values (e.g. ₹1,528.00 million) or page numbers.
- **Word Run Fragmentation**: PII split across runs in Word is handled by reconstructing paragraph text first, replacing the string on a paragraph level, and map-writing the results back to the individual runs. While robust, complex nested styles or hyperlinks could occasionally split runs in unpredictable ways.
- **Name and Company Heuristics**: Our title-matching and leadership heuristics are effective, but may miss names in uncommon contexts that do not utilize titles or lead-manager keywords.

## 9. Conclusion
The hybrid PII Redaction system demonstrates high precision and recall on the evaluation dataset. By separating detectors, utilizing deterministic mappings, and validating patterns (such as Luhn check and PIN codes), it successfully handles the complex formatting of the Red Herring Prospectus without compromising business terminology.