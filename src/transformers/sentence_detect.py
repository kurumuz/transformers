from functools import wraps
from icecream import ic
import time
from transformers import GPT2TokenizerFast
tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

def timeit(my_func):
    @wraps(my_func)
    def timed(*args, **kw):
    
        tstart = time.time()
        output = my_func(*args, **kw)
        tend = time.time()
        
        print('"{}" took {:.3f} ms to execute\n'.format(my_func.__name__, (tend - tstart) * 1000))
        return output
    return timed

end_characters = ['!', '.', ';', '?']
allowed_period_uses = ['Dr', 'Mr', 'Ms', 'Mrs']
closing_characters = [')', '}', ']', "'", '"']

def benchmark():
    tokens = [12]
    for x in range(0, 250):
        text = tokenizer.decode(tokens)
        tokens = tokens + [12]

def create_feature_list(text):
    values = {
        ".": [], "!": [], "?": [], ";": [],
        ")": [], "}": [], "]": [], "'": [], '"': [],
        " Dr.": [], " Mr.": [], " Ms.": [], " Mrs.": [],
    }

    for end_char in values:
        start_index = 0
        while True:
            #print(start_index)
            x = text.find(end_char, start_index, len(text))
            if x != -1: 
                values[end_char].append(x)
                start_index = x + 1
            else:
                break

    testx = []
    for allowed_use in allowed_period_uses:
        x = 0
        while x < len(values["."]):
            if allowed_use in text[values["."][x]-3:values["."][x]]:
                if values["."][x] not in testx:
                    testx.append(values["."][x])

            x += 1

    for test in testx:
        values["."].remove(test)

    return values

def get_last_closing_char(values):
    x = (-1, None)
    for close in closing_characters:
        for value in values[close]:
            if value > x[0]:
                x = (value, close)
    return x

def get_last_end_char(values):
    x = (-1, None)
    for end in end_characters:
        for value in values[end]:
            if value > x[0]:
                x = (value, end)
    return x

def is_sentence(text, values):
    last_end_char = get_last_end_char(values)
    #ic(last_end_char)
    if last_end_char[0] == len(text)-1:
        return True
    else:
        last_closing_char = get_last_closing_char(values)
        #ic(last_closing_char)
        if last_end_char[0] == len(text)-2 and last_closing_char[0] == len(text)-1:
            return True

    return False

def is_sentence_tokens(tokens):
    text = tokenizer.decode(tokens)
    #ic(text)
    features = create_feature_list(text)
    out = is_sentence(text, features)
    return out

if __name__ == '__main__':
    features = create_feature_list(texts[0])
    #print(features)
    print(is_sentence(texts[0], features))
    benchmark()