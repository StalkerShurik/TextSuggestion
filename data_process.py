import re

def delete_emails(text):
    pattern = r'\S+@\S+'
    text = re.sub(pattern, '', text)
    return text

def delete_links(text):
    pattern = r'\S+.com'
    text = re.sub(pattern, '', text)
    return text

def process_raw_body(text):
    text = text.replace('\n', ' ') #for valid deleting new lines
    chars_to_remove = ['\'','~', '$', '@', '_','\n','=','&','^','%' '\/', '\"', '\t','\r', '\v', '\f', ',', '<', '>', '[', ']', '(', ')', '#', '-', '*', ':', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',]
    text_filtered = text.translate(str.maketrans('','',''.join(chars_to_remove)))

    prev_len = len(text_filtered)
    cur_len = prev_len - 1

    text_filtered = delete_emails(text_filtered)
    text_filtered = delete_links(text_filtered)

    text_filtered = text_filtered.replace("!", ".")
    text_filtered = text_filtered.replace("?", ".")

    while (prev_len > cur_len): 
        text_filtered = text_filtered.replace("..", ".")
        text_filtered = text_filtered.replace(" .", ".")
        prev_len = cur_len
        cur_len = len(text_filtered)

    text_filtered = text_filtered.replace("PM", "")
    text_filtered = text_filtered.replace("AM", "")

    text_filtered = re.sub(' +', ' ', text_filtered)

    text_filtered = text_filtered.replace(".", " .")

    return text_filtered