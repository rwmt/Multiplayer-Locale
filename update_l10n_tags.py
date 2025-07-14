#!/bin/env python3
import argparse
from xml.dom.minidom import parseString # we use such brute method to keep comments (inline at least), formatting and ordering

# read English version, and replace lines with already translated tags
def retranslate(base_list: list, translation_list: list):
    result: list = []
    for line in base_list:
        if "<Mp" in line: # all translation strings starts with Mp prefix, and use only one line
            tag_name: str = parseString(line).firstChild.nodeName
            translated: list = list(filter(lambda l: f"<{tag_name}>" in l, translation_list))

            if len(translated) == 1:
                result.append(translated[0])
            elif len(translated) > 1:
                print(f"ERROR: Multiple tags: {tag_name} found in translation")
                exit(1)
            else:
                result.append(line)
        else:
            result.append(line)
    return result
        


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t","--translation", required=True)
    parser.add_argument("-b","--base", default="English/Keyed/Multiplayer.xml", required=False)
    parser.add_argument("-w","--write", default=False, required=False, action=argparse.BooleanOptionalAction)
    parser.add_argument("-d","--destination", required=False)
    parser.add_argument("-p","--print", default=False, required=False, action=argparse.BooleanOptionalAction)
    args = parser.parse_args()

    base_list: list = open(args.base).readlines()
    translation_list: list = open(args.translation).readlines()

    if not args.write and not args.print:
        print("no output selected")
        exit(1)

    res: list = retranslate(base_list, translation_list)
    if args.write:
        result_name = args.destination if args.destination else args.translation + ".out"
        with open(result_name, "w", newline='\r\n') as out_file: # all translation files use CRLF, to make diff job easier keep same windows newlines
            out_file.writelines(res)

    if args.print:
        print(*res)

main()