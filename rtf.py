import chardet
from striprtf.striprtf import rtf_to_text
from klu import Klu
import asyncio
import json

KLU_API_KEY = 'RB4jrsPWMkTTDobxZpG/MB6vNb/AfoQZzMG1FqeNOig='
KLU_ACTION_ID = 'dcd67ecf-afdc-47f0-afde-ec542e19b3db'

def remove_blank_lines(text):
    lines = text.splitlines()  # Split the text into lines
    non_blank_lines = [line for line in lines if line.strip() != '']  # Filter out blank lines
    return '\n'.join(non_blank_lines)

def get_specific_line(text, line_number):
    lines = text.splitlines()  # Split the text into lines
    if 0 <= line_number < len(lines):  # Check if the line number is within range
        return lines[line_number]
    else:
        return None

def convert_rtf_to_text(file_path: str) -> str:
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        rtf_content = raw_data.decode(encoding, errors='ignore')
    plain_text = rtf_to_text(rtf_content)
    return plain_text

# Replace 'path/to/your/file.rtf' with the actual path to your RTF file
file_path = '/Users/atiab/Downloads/cache1/1101-1.rtf'
plain_text = convert_rtf_to_text(file_path)
plain_text = remove_blank_lines(plain_text)
print('Extracted Text:\n', plain_text)
print('Breadcrumb: ', get_specific_line(plain_text, 0))
breadcrumbs = get_specific_line(plain_text, 0).split('/')
print(breadcrumbs)

klu = Klu(KLU_API_KEY)

def remove_first_last_three(s: str) -> str:
    if len(s) <= 6:
        return ''  # Return an empty string if the input string is too short
    return s[7:-3]

async def runKlu():
    result = await klu.actions.prompt(
    KLU_ACTION_ID,
    input={
      "text": plain_text,
    })

    print(result.msg)

    data = json.loads(remove_first_last_three(result.msg))
    print(data)

    # jsondict = {
    #     "title": 
    # }

    # jsondict['content'] = 



    # print(data)


# runKlu()
asyncio.run(runKlu())