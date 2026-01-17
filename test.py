print("hello world")
def QuoteExtraction(Filename):
    with open(Filename,'r') as file:
        text=file.read()
    quotes=[]
    temp=""
    for char in text:
        if char == '"':
            if inside_quotes:
                quotes.append(current)
                current = ""
                inside_quotes = False
            else:
                inside_quotes = True
        elif inside_quotes:
            current += char

    return quotes