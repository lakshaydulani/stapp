def extract_section(section, body):
    # Check if section exists in the body
    lower_body = body.lower()
    lower_section = section.lower()

    # Check if section exists in the body
    index = lower_body.find(lower_section)
    if index == -1:
        return "Section not found"
    
    # Check if the occurrence is prefixed with # or ##
    if index > 0 and (body[index-2] == '#' or (body[index-3:index-1] == '##' and index > 1)):
        # Find the end of the prefix
        start = index - 2 if body[index-2:index] == '##' else index - 1
        
        # Find the next # after the section to limit the substring
        end_index = body.find('#', index + len(section))
        
        # If no # is found, take the rest of the string
        if end_index == -1:
            end_index = len(body)
        
        # Extract and return the substring
        return body[start + 1:end_index].strip()
    else:
        return "Valid prefix not found"

if __name__ == "__main__":
    body_text = """# Inspection Report

|Client Name|John Smith|
|---|---|
|Report No.|2017010100 - YK|
|Report Date|Jan 5th, 2020|
|Contact|Kai Arcinas|
|E-mail|info@guidedimports.com|
|Location|Ningbo, Zhejiang, China|
|Inspector|Rico Zhu|
|Weather|Sunny|

## PRODUCT DESCRIPTION

|Supplier/Vendor|xxxxxxxxxx|
|---|---|
|Manufacturer|xxxxxxxxxx|
|Product Name|Stainless Steel Bottle Insulator|
|Order No.|N/A|
|Order Quantity|2,268 pcs (756 pcs + 1,512 pcs)|
|Inspection Quantity|2,268 pcs (756 pcs + 1,512 pcs)|
|Reference Sample|No sample|
|Inspection Type|Pre-Shipment Inspection|

## Inspection Standard

|Factory cooperation during the inspection|Average|
|---|---|
|Factory Quality organization|Average|
|Inspector’s general opinion on the factory|Average|

## Defects

|Inspection Standard|ISO 2859-1(ANSI/ASQ Z1.4)|
|---|---|
|Sampling Plan|Single, Normal|
|AQL|Critical: 0, Major: 2.5, Minor: 4.0|
|Defects Found|Critical: 0, Major: 0, Minor: 18|
|Sample Size|300 Pcs|
|Max. Allowed|Critical: 0, Major: 14, Minor: 21|
|Overall Inspection Conclusion|PASS|

## Remarks

Client did not provide any artwork for reference prior to the inspection of the goods. The client will need to confirm the artwork.

Guided Imports Quality Inspection Service | Page 1 | www.guidedimports.com"""
    section_name = "Defects"
    print(extract_section(section_name, body_text))