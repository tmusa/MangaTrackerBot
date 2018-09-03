from lark import Lark
from lark.exceptions import ParseError, UnexpectedCharacters
import config
import re

GRAMMAR = r'''
            submission  : disc WS* title WS* [break] WS* [chapter] WS* string* WS* [end]
            disc        : "[DISC]"
            break       : WS"-"WS | WS":"WS
            title       : string | string (WS+ string)*  | string ( ", " string)+
            chapter     : ch WS* SIGNED_NUMBER 
                        | ch WS* SIGNED_NUMBER WS* dash WS* SIGNED_NUMBER
                        | SIGNED_NUMBER
                        | chapter WS* and WS* chapter
                        | leftbound WS* chapter WS* rightbound
            ch          : "CHAPTER" | "CH" | "CH."
            dash        : "-"
            end         : "RAW" | "END"
            leftbound   : "[" | "("
            rightbound  : "]" | ")"
            and         : "AND" | "&"
            string: (/[:a-zA-Z'-\.\?^CHAPTER]/)+ | leftbound (string WS*)+ rightbound

            %import common.ESCAPED_STRING   
            %import common.SIGNED_NUMBER    
            %import common.WS
            '''


def get_parse(submission, grammar=GRAMMAR):
    title_parser = Lark(grammar, start='submission')

    # retrieve parse tree and transform it into a flat string
    parse_tree = ''
    try:
        parse_tree = title_parser.parse(submission)
    except ParseError:
        return ''
    except UnexpectedCharacters:
        return ''

    pretty_parse = parse_tree.pretty()
    collapsed_parse = ' '.join(pretty_parse.split())
    return collapsed_parse


def extract_title(submission, grammar):
    collapsed_parse = get_parse(submission, grammar)

    # parse flat string for submission title
    str_arr = collapsed_parse.split()
    # print(str_arr)
    chapter_discovered = False
    bill = ""
    for token in str_arr:
        if token == 'chapter':
            chapter_discovered = True
        elif len(token) == 1 and not chapter_discovered:
            bill += token
        elif token == 'string':
            bill += ' '
    return bill.strip()


def line_fixer(li):
    li = li.replace('\'', '\'')
    li = li.replace(',', '')
    li = li.replace('"', ' ')
    li = li.replace('!', '')
    li = li.replace('CH.', 'CH. ')
    return li


def title(submission):
    line = line_fixer(submission)
    removes_disc = line.split()[1:]
    test_line = ' '.join(removes_disc)
    name = extract_title(line, GRAMMAR)
    if test_line != name and name != '':
        return name
    simple_chop = chop_chapter(test_line)
    if test_line != simple_chop and simple_chop != '':
        return simple_chop
    return config.PARSE_ERROR


def main():
    lines = []
    with open(r"testtitles.txt") as f:
        lines = f.readlines()

    for line in lines:
        line = line_fixer(line)
        print(line)
        l = line.split()[1:]
        l = ' '.join(l)
        print(l)
        extracted = extract_title(line, GRAMMAR)
        if l != extracted and extracted != '':
            print(extracted)
        elif l != chop_chapter(l) and chop_chapter(l) != '':
            print(chop_chapter(l))
        else:
            print("failed", extracted)


def chop_chapter(tok):
    p = re.compile('( - )?(CH\.|CHAPTER|CH)')
    name = p.split(tok)[0]
    if name != tok:
        return name
    return ''


if __name__ == '__main__':
    main()
