def extract_section(section, body):
    # Check if section exists in the body
    lower_body = body.lower()
    lower_section = section.lower()

    # Check if section exists in the body
    index = lower_body.find(lower_section)
    if index == -1:
        return "Section not found"
    
    # Check if the occurrence is prefixed with # or ##
    if index > 0 and (body[index-1] == '#' or (body[index-2:index] == '##' and index > 1)):
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
    body_text = "##Introduction This is the intro#Section1 This is section one##Conclusion"
    section_name = "Introduction"
    print(extract_section(section_name, body_text))