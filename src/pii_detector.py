import re

# Known names discovered in the KSH International Limited RHP
KNOWN_NAMES = {
    "Kushal Subbayya Hegde",
    "Pushpa Kushal Hegde",
    "Rajesh Kushal Hegde",
    "Rohit Kushal Hegde",
    "Sarthak Malvadkar",
    "Rakhi Girija Shetty",
    "Dinesh Hirachand Munot",
    "Ajay Shriram Patil",
    "Ram Kumar Tiwari",
    "Indu Jacob",
    "Lokesh Shah",
    "Soumavo Sarkar",
    "Kishan Rastogi",
    "Abhijit Diwan",
    "Prakash Boricha",
    "Sheetal Parab",
    "Cherag Gyara",
    "Eric Bacha",
    "Hitesh Ramani",
    "Anand Soni",
    "Ashish M P",
    "Ashish M. P.",
    "Shanti Gopalkrishnan"
}

# Known companies discovered in the KSH International Limited RHP
KNOWN_COMPANIES = {
    "KSH International Limited",
    "Bhandary Metal Extrusion Private Limited",
    "Waterloo Industrial Park VI Private Limited",
    "Link Intime India Private Limited",
    "Nuvama Wealth Management Limited",
    "ICICI Securities Limited",
    "MUFG Intime India Private Limited",
    "Hingne Tare & Associates",
    "Trilegal",
    "Waterloo Motors Private Limited",
    "BSE Limited",
    "HDFC Bank Limited",
    "ICICI Bank Limited",
    "IndusInd Bank Limited",
    "Bajaj Finance Limited",
    "Bajaj Finserv Limited",
    "CARE Analytics and Advisory Private Limited",
    "CG Power and Industrial Solutions Limited",
    "Elantas Beck India Limited",
    "Emirates Transformer & Switchgear Limited",
    "Georgia Transformer Corporation",
    "Cindus Corporation",
    "KSH Infra Park 4 Private Limited",
    "KSH Distriparks Private Limited",
    "KSH Infra Park 5 Private Limited",
    "Dhaulagiri Family Trust",
    "Everest Family Trust",
    "Makalu Family Trust",
    "Broad Family Trust",
    "Annapurna Family Trust"
}

# Terminology blacklist - these should NEVER be treated as personal names
BLACKLISTED_NAME_TERMS = {
    "Red Herring Prospectus",
    "Risk Factors",
    "Book Building Process",
    "Financial Statements",
    "Board of Directors",
    "Registered Office",
    "Corporate Office",
    "Executive Director",
    "Independent Director",
    "Managing Director",
    "Whole-time Director",
    "Company Secretary",
    "Compliance Officer",
    "Promoter Selling Shareholder",
    "Selling Shareholder",
    "Equity Shares",
    "Equity Share",
    "Initial Public Offering",
    "Depositories Act",
    "Companies Act",
    "Income-tax Act",
    "Fugitive Economic Offender",
    "Foreign Venture Capital",
    "Foreign Portfolio Investor",
    "Central Government",
    "Registrar of Companies",
    "Jansatta",
    "Jansatta Newspaper",
    "National Stock Exchange",
    "NSE",
    "BSE",
    "SEBI",
    "RoC",
    "Syndicate Members",
    "Legal Counsel",
    "Registrar to the Offer",
    "SCSBs",
    "UPI",
    "ASBA",
    "PAN",
    "CIN",
    "DIN",
    "DP ID",
    "Client ID",
    "Bids",
    "Bidders",
    "Anchor Investors",
    "Anchor Investor",
    "Offer for Sale",
    "Weighted Average Cost",
    "Average Cost",
    "Cost of Acquisition",
    "Acquisition Cost",
    "Public Offering",
    "Syndicate Member",
    "Self Certified Syndicate",
    "Statutory Auditors",
    "Auditors",
    "Auditor",
    "Identification Number",
    "Identification",
    "Number",
    "Shareholder",
    "Shareholders",
    "Group",
    "Promoter",
    "Promoters",
    "Director",
    "Directors",
    "Manager",
    "Managers",
    "Officer",
    "Officers",
    "Secretary",
    "Compliance Officer",
    "Company Secretary",
    "Executive Director",
    "Independent Director",
    "Managing Director",
    "Whole-time Director",
    "Statutory Auditors",
    "Auditors",
    "Auditor",
    "Syndicate Members",
    "Syndicate Member",
    "Registrar",
    "Underwriters",
    "Underwriter",
    "Book Running Lead Managers",
    "Book Running Lead Manager",
    "BRLMs",
    "BRLM",
    "SCSB",
    "SCSBs",
    "UPI",
    "ASBA",
    "Self-Certified Syndicate Bank",
    "Self-Certified Syndicate Banks",
    "Self Certified Syndicate Bank",
    "Self Certified Syndicate Banks",
    "Certified Syndicate Bank",
    "Certified Syndicate Banks",
    "Syndicate Bank",
    "Syndicate Banks",
    "Escrow Collection Bank",
    "Escrow Collection Banks",
    "Escrow Bank",
    "Escrow Banks",
    "Refund Bank",
    "Refund Banks",
    "Sponsor Bank",
    "Sponsor Banks",
    "Public Offer Account Bank",
    "Public Offer Account Banks"
}

def luhn_check(num_str):
    """Luhn algorithm validation for credit/debit cards."""
    digits = [int(d) for d in num_str if d.isdigit()]
    if len(digits) < 13 or len(digits) > 19:
        return False
    checksum = 0
    for i, d in enumerate(reversed(digits)):
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        checksum += d
    return checksum % 10 == 0

class PIIDetector:
    def __init__(self):
        # Base Regexes
        self.email_regex = re.compile(r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b")
        self.ssn_regex = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
        self.cc_regex = re.compile(r"\b(?:\d{4}[ -]?){3}\d{4}\b|\b\d{16}\b")
        self.ip_regex = re.compile(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b")
        
        # Phone regex: matches typical Indian/international numbers
        # e.g., +91 20 4505 3237, +91-9876543210, +91 22 40094400, 022-68052182
        self.phone_regex = re.compile(
            r"\+?\s*91[\s\-]?\d{10}\b|\+?\s*91[\s\-]?\d{2,4}[\s\-]?\d{3,4}[\s\-]?\d{4}\b|\b0\d{2,3}-\d{6,8}\b|\b\d{10}\b"
        )
        
        # General date pattern
        self.date_regex = re.compile(
            r"\b\d{1,2}[\s\-\/](?:January|February|March|April|May|June|July|August|September|October|November|December|[A-Za-z]{3}|\d{1,2})[\s\-\/,]\s*\d{2,4}\b"
            r"|\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s*\d{4}\b"
        )

        # Name Title Regex: matches names with common titles (Shri, Smt, Mr, Ms, Mrs, Dr, Late)
        self.name_title_regex = re.compile(
            r"\b(?:Mr\.|Ms\.|Mrs\.|Dr\.|Shri|Smt\.|Late|Mr|Ms|Mrs|Smt)\s+([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+){1,3})\b"
        )
        
        # Company Suffix Regex
        self.company_regex = re.compile(
            r"\b[A-Z][a-zA-Z0-9]*(?:\s+[A-Z][a-zA-Z0-9]*)*\s+(?:Limited|Private Limited|LLP|Corporation|Inc\.|Ltd\.|Pvt\.\s*Ltd\.|Industries|Securities|Bank|Foundation|Trust|Services|Technologies|Associates)\b"
        )

        # Address indicator keywords
        self.address_indicators = ["Registered Office", "Corporate Office", "Address", "Plot No.", "Village", "Taluka", "District", "Gat No.", "Flat No.", "S. no.", "Building No.", "lane no. 3 Prabhat Road", "Buena Monte"]

    def detect_emails(self, text):
        matches = []
        for m in self.email_regex.finditer(text):
            val = m.group(0)
            matches.append({
                "type": "EMAIL",
                "original": val,
                "start": m.start(),
                "end": m.end(),
                "confidence": 1.0
            })
        return matches

    def detect_ssns(self, text):
        matches = []
        for m in self.ssn_regex.finditer(text):
            val = m.group(0)
            # Perform context check to avoid false positives (SSNs should have digits and hyphens)
            # SSN context keywords: ssn, social security
            context_area = text[max(0, m.start() - 40): min(len(text), m.end() + 40)].lower()
            confidence = 0.8 if any(k in context_area for k in ["ssn", "social security", "security number"]) else 0.5
            matches.append({
                "type": "SSN",
                "original": val,
                "start": m.start(),
                "end": m.end(),
                "confidence": confidence
            })
        return matches

    def detect_credit_cards(self, text):
        matches = []
        for m in self.cc_regex.finditer(text):
            val = m.group(0)
            clean_cc = re.sub(r"\D", "", val)
            if luhn_check(clean_cc):
                matches.append({
                    "type": "CREDIT_CARD",
                    "original": val,
                    "start": m.start(),
                    "end": m.end(),
                    "confidence": 1.0
                })
        return matches

    def detect_ip_addresses(self, text):
        matches = []
        for m in self.ip_regex.finditer(text):
            val = m.group(0)
            octets = val.split(".")
            if len(octets) == 4 and all(o.isdigit() and 0 <= int(o) <= 255 for o in octets):
                # Ensure it's not part of a date or version number like 1.2.0.4 (version) or 31.03.2025 (date)
                # Check character immediately preceding and succeeding the match
                start = m.start()
                end = m.end()
                pre_char = text[start - 1] if start > 0 else ""
                post_char = text[end] if end < len(text) else ""
                if pre_char.isdigit() or post_char.isdigit():
                    continue
                if pre_char == "." and start > 1 and text[start - 2].isdigit():
                    continue
                if post_char == "." and end + 1 < len(text) and text[end + 1].isdigit():
                    continue
                matches.append({
                    "type": "IP_ADDRESS",
                    "original": val,
                    "start": m.start(),
                    "end": m.end(),
                    "confidence": 0.9
                })
        return matches

    def detect_dates_of_birth(self, text):
        """DOBs must have explicit birth context to protect ordinary business dates."""
        matches = []
        for m in self.date_regex.finditer(text):
            val = m.group(0)
            start, end = m.start(), m.end()
            context_area = text[max(0, start - 60): min(len(text), end + 60)].lower()
            # Require explicit DOB/birth context
            if any(k in context_area for k in ["dob", "date of birth", "birth date", "born", "birthdate"]):
                matches.append({
                    "type": "DOB",
                    "original": val,
                    "start": start,
                    "end": end,
                    "confidence": 0.95
                })
        return matches

    def detect_phone_numbers(self, text):
        """Detect phone numbers conservatively, avoiding financials, CINs, share counts."""
        matches = []
        for m in self.phone_regex.finditer(text):
            val = m.group(0)
            start, end = m.start(), m.end()
            
            # Clean non-digit characters
            digits = re.sub(r"\D", "", val)
            
            # Skip if digits are too short or long to be a phone number
            # Indian landlines are usually 8 digits, mobile is 10 digits
            # Total digits with 91 could be 12.
            if len(digits) < 8 or len(digits) > 13:
                continue
                
            # Avoid matching PIN codes (6 digits)
            if len(digits) == 6:
                continue
                
            # Context check to ensure it's not a financial number, CIN, or share count
            context_area = text[max(0, start - 50): min(len(text), end + 50)].lower()
            
            # If ₹, million, shares, or percentage is immediately nearby, discard
            if any(k in context_area for k in ["₹", "rs.", "rupees", "million", "billion", "shares", "%", "percent", "cagr"]):
                # But keep if we also have strong phone keywords
                if not any(k in context_area for k in ["telephone", "tel:", "phone", "mobile", "contact", "fax"]):
                    continue
                    
            # Avoid matching portion of a larger word or CIN (U28129PN1979PLC141032)
            pre_char = text[start - 1] if start > 0 else ""
            post_char = text[end] if end < len(text) else ""
            if pre_char.isalnum() or post_char.isalnum():
                continue
                
            # If it's just a raw 10-digit number without any phone context, check if phone keyword is near
            if len(digits) == 10 and not val.startswith(("+", "0")):
                if not any(k in context_area for k in ["telephone", "tel", "phone", "mobile", "contact", "call"]):
                    continue
                    
            # Check for phone keywords or formatting (like +91 or dash)
            confidence = 0.6
            if any(k in context_area for k in ["telephone", "tel", "phone", "mobile", "contact", "fax", "call"]):
                confidence = 0.9
            elif val.startswith(("+91", "+ 91", "022", "020", "080", "011")):
                confidence = 0.8
            else:
                # If no strong context and no formatting indicators, skip
                continue
                
            matches.append({
                "type": "PHONE",
                "original": val,
                "start": start,
                "end": end,
                "confidence": confidence
            })
        return matches

    def detect_names(self, text):
        """Detect personal names conservatively using known names, titles, and context labels."""
        matches = []
        text_len = len(text)
        
        # 1. Direct Known Names search (exact and case-sensitive)
        for name in KNOWN_NAMES:
            for m in re.finditer(r"\b" + re.escape(name) + r"\b", text):
                matches.append({
                    "type": "FULL_NAME",
                    "original": m.group(0),
                    "start": m.start(),
                    "end": m.end(),
                    "confidence": 1.0
                })
                
        # 2. Match based on title regex (e.g. Mr. Rajesh Kushal Hegde, Smt. Pushpa Hegde)
        for m in self.name_title_regex.finditer(text):
            name_candidate = m.group(1).strip()
            
            # Clean name candidate from trailing commas/whitespace
            name_candidate = re.sub(r"[,\s]+$", "", name_candidate)
            
            # Filter out blacklisted words
            if name_candidate in BLACKLISTED_NAME_TERMS:
                continue
            if any(term in name_candidate for term in BLACKLISTED_NAME_TERMS):
                continue
            if name_candidate.endswith(("Limited", "Ltd", "LLP", "Inc", "Pvt", "Industries", "Securities", "Bank", "Foundation", "Trust", "Services", "Technologies", "Associates")):
                continue
                
            # Confidence check
            matches.append({
                "type": "FULL_NAME",
                "original": name_candidate,
                "start": m.start(1),
                "end": m.start(1) + len(name_candidate),
                "confidence": 0.9
            })
            
        # 3. Match based on Contact Person/Compliance Officer/Company Secretary context labels
        # e.g., "Contact Person: Sarthak Malvadkar", "Compliance Officer: Rajesh Bhandary"
        # Match case-sensitive names following case-insensitive prefixes
        context_name_regex = re.compile(
            r"\b(?:[Cc]ontact\s+[Pp]erson|[Cc]ompany\s+[Ss]ecretary|[Cc]ompliance\s+[Oo]fficer|[Dd]irector|[Pp]romoter)\s*[:\-–]?\s*([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+){1,2})\b"
        )
        for m in context_name_regex.finditer(text):
            name_candidate = m.group(1).strip()
            # Normalize whitespace for blacklist checking
            norm_name = re.sub(r"\s+", " ", name_candidate)
            if norm_name in BLACKLISTED_NAME_TERMS:
                continue
            if any(term in norm_name for term in BLACKLISTED_NAME_TERMS):
                continue
            if name_candidate.endswith(("Limited", "Ltd", "LLP", "Inc", "Pvt", "Industries", "Securities", "Bank", "Foundation", "Trust", "Services", "Technologies", "Associates")):
                continue
            matches.append({
                "type": "FULL_NAME",
                "original": name_candidate,
                "start": m.start(1),
                "end": m.start(1) + len(name_candidate),
                "confidence": 0.8
            })
            
        # Remove duplicate ranges and subset matches
        return self._deduplicate_matches(matches)

    def detect_company_names(self, text):
        """Detect company names using known companies and suffix-based patterns, avoiding blacklists."""
        matches = []
        
        # 1. Known Companies search
        for company in KNOWN_COMPANIES:
            for m in re.finditer(r"\b" + re.escape(company) + r"\b", text):
                matches.append({
                    "type": "COMPANY",
                    "original": m.group(0),
                    "start": m.start(),
                    "end": m.end(),
                    "confidence": 1.0
                })
                
        # 2. Regex-based Company search
        for m in self.company_regex.finditer(text):
            val = m.group(0).strip()
            start_idx = m.start()
            end_idx = m.end()
            
            # If it starts with "Formerly ", strip it to avoid redacting "Formerly"
            if val.startswith("Formerly "):
                val = val[9:]
                start_idx += 9
                
            # Normalize whitespace for blacklist checking
            norm_val = re.sub(r"\s+", " ", val)
            # Avoid matching terms that contain blacklisted words
            if any(term in norm_val for term in BLACKLISTED_NAME_TERMS):
                continue
                
            # Filter out strings that start with lowercase or common verbs
            if not val or not val[0].isupper():
                continue
                
            # Ensure it is longer than 2 words
            if len(val.split()) < 2:
                continue
                
            matches.append({
                "type": "COMPANY",
                "original": val,
                "start": start_idx,
                "end": end_idx,
                "confidence": 0.85
            })
            
        return self._deduplicate_matches(matches)

    def detect_addresses(self, text):
        """Detect addresses using indicators and pin codes, redacting full spans rather than cities."""
        matches = []
        
        # 1. Find address blocks using registered/corporate office labels
        # e.g., "Registered Office: 11/3, 11/4 and 11/5, Village Birdewadi, Chakan Taluka - Khed, Pune – 410 501, Maharashtra, India"
        address_prefix_regex = re.compile(
            r"\b(?:Registered Office|Corporate Office|Address|RoC Office|RoC|situated at the following address|situated at)s?[\s\:\-\–]*([A-Za-z0-9\s,\.\-&/()“#\[\]●–\—]{10,250}?\b\d{3}\s?\d{3}\b(?:\s*,?\s*[A-Za-z\s,]+)?)",
            re.IGNORECASE
        )
        for m in address_prefix_regex.finditer(text):
            val = m.group(1).strip()
            # Reconstruct the full span including prefix for safety
            full_span = text[m.start(): m.end()]
            matches.append({
                "type": "ADDRESS",
                "original": full_span,
                "start": m.start(),
                "end": m.end(),
                "confidence": 0.95
            })
            
        # 2. Find address blocks that start with Plot No / Gat No / Flat No / S. no / S. No. / Gat no. / Flat no.
        address_start_regex = re.compile(
            r"\b(?:Plot No\.|Plot no\.|Gat No\.|Gat no\.|Flat No\.|Flat no\.|S\.\s*No\.|S\.\s*no\.)[\s\:\-\–]*[A-Za-z0-9\s,\.\-&/()“#\[\]●–\—]{10,200}?\b\d{3}\s?\d{3}\b(?:\s*,?\s*[A-Za-z\s,]+)?",
            re.IGNORECASE
        )
        for m in address_start_regex.finditer(text):
            val = m.group(0).strip()
            matches.append({
                "type": "ADDRESS",
                "original": val,
                "start": m.start(),
                "end": m.end(),
                "confidence": 0.9
            })

        # 3. Handle specific address text formats found in tables/cells that may not fit regex
        for m in re.finditer(r"\b\d{1,3}\s+Buena Monte\b[A-Za-z0-9\s,\.\-–\—]+?\b\d{3}\s?\d{3}\b", text):
            matches.append({
                "type": "ADDRESS",
                "original": m.group(0),
                "start": m.start(),
                "end": m.end(),
                "confidence": 0.95
            })
            
        return self._deduplicate_matches(matches)

    def detect_all(self, text):
        """Run all detectors and return a consolidated list of matches."""
        all_matches = []
        all_matches.extend(self.detect_emails(text))
        all_matches.extend(self.detect_ssns(text))
        all_matches.extend(self.detect_credit_cards(text))
        all_matches.extend(self.detect_ip_addresses(text))
        all_matches.extend(self.detect_dates_of_birth(text))
        all_matches.extend(self.detect_phone_numbers(text))
        all_matches.extend(self.detect_names(text))
        all_matches.extend(self.detect_company_names(text))
        all_matches.extend(self.detect_addresses(text))
        
        return self._deduplicate_matches(all_matches)

    def _deduplicate_matches(self, matches):
        """Helper to deduplicate overlapping matches, preferring higher confidence or larger spans."""
        if not matches:
            return []
            
        # Sort matches by start position ascending, then end position descending (larger first)
        matches = sorted(matches, key=lambda x: (x["start"], -x["end"]))
        
        deduped = []
        current = matches[0]
        
        for next_match in matches[1:]:
            # Check for overlap
            if next_match["start"] < current["end"]:
                # They overlap. Decide which to keep.
                # Address matches usually override smaller entities like company, name, phone, or date inside them
                if current["type"] == "ADDRESS" and next_match["type"] != "ADDRESS":
                    # Keep current (address)
                    continue
                elif next_match["type"] == "ADDRESS" and current["type"] != "ADDRESS":
                    # Replace current with next (address)
                    current = next_match
                # Otherwise, keep the one with longer span or higher confidence
                elif (next_match["end"] - next_match["start"]) > (current["end"] - current["start"]):
                    current = next_match
                elif next_match["confidence"] > current["confidence"]:
                    current = next_match
            else:
                deduped.append(current)
                current = next_match
                
        deduped.append(current)
        return deduped
