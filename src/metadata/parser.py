"""
parser.py

Unified metadata parser for EXIF, Zsteg, Steghide, and Binwalk outputs.
"""

import re


class MetadataParser:
    """
    Parses raw and structured outputs from various metadata scrapers into
a consistent Python dictionary schema.
    """
    def __init__(self):
        """
        Initialize a MetadataParser. No state is stored between parse calls.
        """
        pass



    @staticmethod
    def _parse_key_value(line: str):
        """
        Extract a key and value from a "Key: Value" formatted string.
        Returns a tuple (key, value) or (None, None) if no match.
        """
        match = re.match(r'^\s*([^:]+?)\s*:\s*(.+)$', line)
        if match:
            return match.group(1).strip(), match.group(2).strip()
        return None, None
    


    def parse_exif(self, exif_output):
        """
        Parse EXIF metadata.

        Accepts either:
        - A dict from an EXIF scraper (e.g., exiftool JSON or Pillow fallback)
        - A raw multiline string in "Key: Value" format

        Returns:
            dict: Parsed EXIF fields and values
        """
        parsed = {}
        if isinstance(exif_output, dict):
            # Copy to avoid mutating original
            return exif_output.copy()

        # Raw string input
        for line in exif_output.splitlines():
            key, value = self._parse_key_value(line)
            if key:
                parsed[key] = value
        return parsed
    


    def parse_zsteg(self, zsteg_output):
        """
        Parse Zsteg output (raw text or dict).

        Returns:
            dict: Parsed key/value pairs
        """
        parsed = {}
        if isinstance(zsteg_output, dict):
            return zsteg_output.copy()
        for line in zsteg_output.splitlines():
            key, value = self._parse_key_value(line)
            if key:
                parsed[key] = value
        return parsed
    


    def parse_steghide(self, steghide_output):
        """
        Parse Steghide "info" output (raw text or dict).

        Returns:
            dict: Parsed steghide metadata fields
        """
        parsed = {}
        if isinstance(steghide_output, dict):
            return steghide_output.copy()
        for line in steghide_output.splitlines():
            key, value = self._parse_key_value(line)
            if key:
                parsed[key] = value
        return parsed



    def parse_binwalk(self, binwalk_output):
        """
        Parse Binwalk scan or extract output.

        Accepts either:
        - A dict with key 'Signatures' (as from a BinwalkScraper)
        - A raw multiline string

        Returns:
            dict: {'Signatures': [ {'Offset': ..., 'Description': ...}, ... ]}
        """
        # If already structured
        if isinstance(binwalk_output, dict) and 'Signatures' in binwalk_output:
            # Copy list of dicts
            return {'Signatures': list(binwalk_output['Signatures'])}

        # Raw text input
        signatures = []
        for line in binwalk_output.splitlines():
            m = re.match(r'^\s*([0-9A-Fa-fx]+)\s*:\s*(.+)$', line)
            if m:
                signatures.append({
                    'Offset': m.group(1),
                    'Description': m.group(2).strip()
                })
        return {'Signatures': signatures}
    

    def _add_derived_search_terms(self, categories):
        """Add derived search terms based on categorized data"""
        print(f"DEBUG: Adding derived search terms for categories: {list(categories.keys())}")
        
        # Professional vs Amateur detection
        device_info = categories['device_info']
        technical_specs = categories['technical_specs']
        
        print(f"DEBUG: Device info: {device_info}")
        print(f"DEBUG: Technical specs: {technical_specs}")
        
        # Professional camera indicators
        camera_make = str(device_info.get('camera_make', '')).lower()
        camera_model = str(device_info.get('camera_model', '')).lower()
        
        if any(brand in camera_make for brand in ['canon', 'nikon', 'sony', 'fujifilm']):
            print(f"DEBUG: Professional camera brand detected: {camera_make}")
            if any(model_indicator in camera_model 
                   for model_indicator in ['d850', 'd750', '5d', '7r', 'x-t', 'coolpix']):
                categories['search_keywords'].append("professional_photography")
                print("DEBUG: Added professional_photography keyword")
        
        # Mobile photography detection
        if any(mobile_brand in camera_make 
               for mobile_brand in ['apple', 'samsung', 'google', 'huawei', 'iphone']):
            categories['search_keywords'].append("mobile_photography")
            print("DEBUG: Added mobile_photography keyword")
        
        # Event type detection based on technical specs
        flash_info = str(technical_specs.get('flash_used', '')).lower()
        if flash_info and 'fired' in flash_info:
            if categories['temporal_data']:
                categories['search_keywords'].append("indoor_event")
                print("DEBUG: Added indoor_event keyword")
        
        # Landscape photography indicators
        focal_length = str(technical_specs.get('focal_length', '')).lower()
        if focal_length and any(wide_focal in focal_length 
                               for wide_focal in ['14mm', '16mm', '18mm', '20mm', '24mm']):
            categories['search_keywords'].append("landscape_photography")
            print("DEBUG: Added landscape_photography keyword")
        
        # Portrait photography indicators
        if focal_length and any(portrait_focal in focal_length 
                               for portrait_focal in ['85mm', '105mm', '135mm']):
            categories['search_keywords'].append("portrait_photography")
            print("DEBUG: Added portrait_photography keyword")
        
        # Vintage photography detection
        if categories['temporal_data']:
            for date_key, date_value in categories['temporal_data'].items():
                year_match = re.search(r'(\d{4})', str(date_value))
                if year_match:
                    year = int(year_match.group(1))
                    if year < 2010:
                        categories['search_keywords'].append("vintage_photography")
                        print(f"DEBUG: Added vintage_photography keyword for year {year}")
                    break
        
        print(f"DEBUG: Final search keywords: {categories['search_keywords']}")

    def get_iris_search_terms(self, categorized_data):
        """
        Extract the most relevant search terms for IRIS from categorized data.
        
        Args:
            categorized_data (dict): Output from categorize_exif_for_iris()
            
        Returns:
            list: Prioritized search terms for reverse image search
        """
        print(f"DEBUG: Extracting IRIS search terms from: {type(categorized_data)}")
        
        if not isinstance(categorized_data, dict):
            print("DEBUG: Input is not a dict, returning empty list")
            return []
        
        search_terms = []
        
        # Prioritize terms based on confidence and relevance
        if categorized_data.get('location_data'):
            print(f"DEBUG: Found location data: {categorized_data['location_data']}")
            # Location data is highly valuable for image search
            for term in categorized_data['search_keywords']:
                if term.startswith('location:'):
                    search_terms.append(term)
                    print(f"DEBUG: Added location term: {term}")
        
        # Device information
        for term in categorized_data['search_keywords']:
            if term.startswith('camera:'):
                search_terms.append(term)
                print(f"DEBUG: Added camera term: {term}")
        
        # Photography type
        photo_types = [term for term in categorized_data['search_keywords'] 
                      if 'photography' in term]
        search_terms.extend(photo_types)
        print(f"DEBUG: Added photography types: {photo_types}")
        
        # Year-based terms
        year_terms = [term for term in categorized_data['search_keywords'] 
                     if term.startswith('year:')]
        search_terms.extend(year_terms)
        print(f"DEBUG: Added year terms: {year_terms}")
        
        # Technical terms
        tech_terms = [term for term in categorized_data['search_keywords'] 
                     if term in ['low_light', 'flash_photography', 'high_resolution']]
        search_terms.extend(tech_terms)
        print(f"DEBUG: Added technical terms: {tech_terms}")
        
        # Remove duplicates while preserving order
        seen = set()
        unique_terms = []
        for term in search_terms:
            if term not in seen:
                seen.add(term)
                unique_terms.append(term)
        
        final_terms = unique_terms[:10]  # Limit to top 10 most relevant terms
        print(f"DEBUG: Final IRIS search terms: {final_terms}")
        return final_terms

    def categorize_exif_for_iris(self, exif_data):
        """
        Categorize EXIF metadata into useful search parameters for IRIS.
        
        Takes parsed EXIF data and organizes it into categories that can
        enhance reverse image search queries.
        
        Args:
            exif_data (dict): Parsed EXIF metadata from parse_exif()
            
        Returns:
            dict: Categorized metadata for search enhancement
        """
        print(f"DEBUG: Starting categorize_exif_for_iris with data type: {type(exif_data)}")
        print(f"DEBUG: Input data keys: {list(exif_data.keys()) if isinstance(exif_data, dict) else 'Not a dict'}")
        
        categories = {
            'device_info': {},
            'location_data': {},
            'temporal_data': {},
            'technical_specs': {},
            'search_keywords': [],
            'confidence_score': 0.0
        }
        
        # If input is not a dict, try to parse it first
        if not isinstance(exif_data, dict):
            print("DEBUG: Input is not a dict, parsing first...")
            exif_data = self.parse_exif(exif_data)
            print(f"DEBUG: Parsed data keys: {list(exif_data.keys())}")
        
        confidence_factors = []
        
        # Device Information
        device_fields = [
            ('Make', 'camera_make'),
            ('Model', 'camera_model'),
            ('Software', 'software'),
            ('Camera Make', 'camera_make'),
            ('Camera Model', 'camera_model'),
            ('Camera Software', 'software'),
            ('Lens Make', 'lens_make'),
            ('Lens Model', 'lens_model')
        ]
        
        print("DEBUG: Processing device fields...")
        for exif_key, cat_key in device_fields:
            if exif_key in exif_data:
                value = exif_data[exif_key]
                categories['device_info'][cat_key] = value
                categories['search_keywords'].append(f"camera:{value}")
                confidence_factors.append(0.2)
                print(f"DEBUG: Found device field {exif_key}: {value}")
        
        # Location Data
        location_fields = [
            ('GPS Latitude', 'latitude'),
            ('GPS Longitude', 'longitude'),
            ('GPS Altitude', 'altitude'),
            ('Location', 'location_name'),
            ('City', 'city'),
            ('State', 'state'),
            ('Country', 'country'),
            ('GPS Position', 'coordinates')
        ]
        
        print("DEBUG: Processing location fields...")
        for exif_key, cat_key in location_fields:
            if exif_key in exif_data:
                value = exif_data[exif_key]
                categories['location_data'][cat_key] = value
                if 'GPS' in exif_key:
                    categories['search_keywords'].append("location:gps_tagged")
                    confidence_factors.append(0.3)
                    print(f"DEBUG: Found GPS field {exif_key}: {value}")
                else:
                    categories['search_keywords'].append(f"location:{value}")
                    confidence_factors.append(0.25)
                    print(f"DEBUG: Found location field {exif_key}: {value}")
        
        # Temporal Data
        temporal_fields = [
            ('DateTime', 'creation_date'),
            ('Date/Time Original', 'original_date'),
            ('Create Date', 'create_date'),
            ('Modify Date', 'modify_date'),
            ('DateTimeOriginal', 'datetime_original')
        ]
        
        print("DEBUG: Processing temporal fields...")
        for exif_key, cat_key in temporal_fields:
            if exif_key in exif_data:
                date_value = exif_data[exif_key]
                categories['temporal_data'][cat_key] = date_value
                print(f"DEBUG: Found temporal field {exif_key}: {date_value}")
                
                # Extract year for search keywords
                year_match = re.search(r'(\d{4})', str(date_value))
                if year_match:
                    year = year_match.group(1)
                    categories['search_keywords'].append(f"year:{year}")
                    confidence_factors.append(0.15)
                    print(f"DEBUG: Extracted year: {year}")
        
        # Technical Specifications
        technical_fields = [
            ('ISO', 'iso'),
            ('Aperture', 'aperture'),
            ('Shutter Speed', 'shutter_speed'),
            ('Focal Length', 'focal_length'),
            ('Flash', 'flash_used'),
            ('White Balance', 'white_balance'),
            ('Exposure Mode', 'exposure_mode'),
            ('Image Width', 'width'),
            ('Image Height', 'height'),
            ('Resolution', 'resolution'),
            ('Color Space', 'color_space')
        ]
        
        print("DEBUG: Processing technical fields...")
        for exif_key, cat_key in technical_fields:
            if exif_key in exif_data:
                value = exif_data[exif_key]
                categories['technical_specs'][cat_key] = value
                print(f"DEBUG: Found technical field {exif_key}: {value}")
                
                # Add specific technical keywords
                if cat_key == 'iso':
                    iso_str = str(value)
                    if iso_str.isdigit():
                        iso_val = int(iso_str.split()[0])  # Handle "ISO 800" format
                        if iso_val >= 1600:
                            categories['search_keywords'].append("low_light")
                            print(f"DEBUG: High ISO detected ({iso_val}), added low_light keyword")
                        confidence_factors.append(0.1)
                
                elif cat_key == 'flash_used':
                    if 'fired' in str(value).lower():
                        categories['search_keywords'].append("flash_photography")
                        print(f"DEBUG: Flash fired detected, added flash_photography keyword")
                    confidence_factors.append(0.1)
                
                elif cat_key in ['width', 'height']:
                    if str(value).isdigit() and int(value) >= 4000:
                        categories['search_keywords'].append("high_resolution")
                        print(f"DEBUG: High resolution detected ({value}), added high_resolution keyword")
                    confidence_factors.append(0.05)
        
        # Calculate confidence score (0.0 to 1.0)
        if confidence_factors:
            categories['confidence_score'] = min(sum(confidence_factors), 1.0)
            print(f"DEBUG: Calculated confidence score: {categories['confidence_score']} from {len(confidence_factors)} factors")
        
        # Add derived search terms
        print("DEBUG: Adding derived search terms...")
        self._add_derived_search_terms(categories)
        
        print(f"DEBUG: Final categorized data:")
        print(f"  - Device info: {categories['device_info']}")
        print(f"  - Location data: {categories['location_data']}")
        print(f"  - Temporal data: {categories['temporal_data']}")
        print(f"  - Technical specs: {categories['technical_specs']}")
        print(f"  - Search keywords: {categories['search_keywords']}")
        print(f"  - Confidence score: {categories['confidence_score']}")
        
        return categories
    

    def get_metadata(self):
        """
        For compatibility: returns an empty dict (no persistent state).
        """
        return {}
