import re
import hashlib
from faker import Faker

class PIIRedactor:
    def __init__(self):
        # Seed the faker to ensure reproducible results across runs
        self.fake = Faker(['en_IN', 'en_US'])
        self.fake.seed_instance(42)
        
        # Consistent mapping from original entity to synthetic alternative
        self.mapping = {}
        
        # Keep track of generated values to prevent collisions
        self.generated_values = set()

    def get_replacement(self, original, pii_type):
        """Get or create a deterministic replacement for a given PII value."""
        # Normalize whitespace and case in original to avoid matching discrepancies
        normalized = re.sub(r"\s+", " ", original.strip())
        lookup_key = normalized.lower()
        
        if lookup_key in self.mapping:
            return self.mapping[lookup_key]
            
        replacement = self._generate_value(normalized, pii_type)
        
        # Prevent collisions (ensure the new value hasn't been generated already)
        attempts = 0
        while replacement in self.generated_values and attempts < 100:
            replacement = self._generate_value(normalized, pii_type)
            attempts += 1
            
        # Match the case formatting of the original value
        if original.isupper():
            replacement = replacement.upper()
        elif original.islower():
            replacement = replacement.lower()
            
        self.mapping[lookup_key] = replacement
        self.generated_values.add(replacement)
        return replacement

    def _generate_value(self, original, pii_type):
        if pii_type == "EMAIL":
            # Generate a completely synthetic fake email to protect the original username.
            # We seed Faker deterministically using the original email hash to ensure reproducibility.
            original_hash = int(hashlib.md5(original.lower().encode('utf-8')).hexdigest(), 16)
            local_fake = Faker()
            local_fake.seed_instance(original_hash % (2**32))
            username = local_fake.free_email().split('@')[0]
            # Strip non-alphanumeric chars for cleanliness if needed
            username = re.sub(r"[^a-zA-Z0-9\._\-]", "", username).lower()
            if not username:
                username = "contact"
            return f"{username}@example.com"
            
        elif pii_type == "FULL_NAME":
            # Generate realistic synthetic name
            # Check gender cues if any (Smt./Mrs. usually female)
            if any(cue in original for cue in ["Smt", "Mrs", "Smt.", "Mrs."]):
                return self.fake.first_name_female() + " " + self.fake.last_name()
            else:
                return self.fake.first_name_male() + " " + self.fake.last_name()
                
        elif pii_type == "PHONE":
            # Generate realistic Indian or international phone number based on pattern
            if "022" in original or "020" in original or "011" in original:
                # Landline pattern
                area_code = "022" if "022" in original else ("020" if "020" in original else "011")
                # Generate 8 digit number
                num_str = self.fake.numerify("########")
                return f"{area_code}-{num_str}"
            else:
                # Mobile / Standard
                # Check for country code +91
                has_plus = original.startswith("+")
                num_str = self.fake.numerify("##########")
                # Format mobile numbers like +91 9XXXX XXXXX
                if has_plus or "91" in original[:5]:
                    return f"+91 {num_str[:5]} {num_str[5:]}"
                else:
                    return num_str
                    
        elif pii_type == "COMPANY":
            # Generate synthetic company name with appropriate suffix
            suffix = "Limited"
            if "Private Limited" in original or "Pvt. Ltd." in original:
                suffix = "Private Limited"
            elif "LLP" in original:
                suffix = "LLP"
            elif "Corporation" in original:
                suffix = "Corporation"
            elif "Inc." in original:
                suffix = "Inc."
            elif "Bank" in original:
                suffix = "Bank Limited"
                
            company_base = self.fake.company()
            # Clean company base of existing endings if any
            company_base = re.sub(r"\s*(?:Ltd|Ltd\.|Limited|Pvt|Pvt\.|Private|LLP|Corporation|Inc\.)\s*$", "", company_base)
            # Add synthetic qualifier to ensure it looks fake and premium
            return f"Apex {company_base} {suffix}"
            
        elif pii_type == "ADDRESS":
            # Reconstruct address using fake building, street, city, state, pin
            # Match registered/corporate prefix if present
            prefix = ""
            for indicator in ["Registered Office", "Corporate Office", "RoC Office", "RoC"]:
                if original.lower().startswith(indicator.lower()):
                    prefix = original[:len(indicator) + 1] + " "
                    break
                    
            building_no = self.fake.building_number()
            street = self.fake.street_name()
            city = self.fake.city()
            state = self.fake.state()
            # Get PIN code: 6 digits (e.g. 411001)
            pin = self.fake.postcode()
            if len(pin) != 6:
                pin = "411099" # Default fake pin
                
            return f"{prefix}{building_no}, Industrial Estate, {street}, {city} – {pin[:3]} {pin[3:]}, {state}, India"
            
        elif pii_type == "SSN":
            # Standard SSN format: 000-00-0000
            num = self.fake.numeric_iter(9)
            digits = [str(next(num)) for _ in range(9)]
            return f"{''.join(digits[:3])}-{''.join(digits[3:5])}-{''.join(digits[5:])}"
            
        elif pii_type == "CREDIT_CARD":
            # Must pass Luhn check. Standard visa/mastercard pattern.
            # Faker credit_card_number uses Luhn
            return self.fake.credit_card_number(card_type='visa')
            
        elif pii_type == "DOB":
            # Generate fake date of birth, formatted similarly to original if possible
            fake_date = self.fake.date_of_birth(minimum_age=25, maximum_age=80)
            # Check format of original
            if "/" in original:
                return fake_date.strftime("%d/%m/%Y")
            elif "-" in original:
                return fake_date.strftime("%d-%m-%Y")
            else:
                return fake_date.strftime("%d %B %Y")
                
        elif pii_type == "IP_ADDRESS":
            return self.fake.ipv4()
            
        else:
            return f"[REDACTED_{pii_type}]"
