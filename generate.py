from yaml import load, dump
import os


def convert(word):
    return ''.join(x.capitalize() or '_' for x in word.split('_'))


def generate(filename):
    name = filename.replace(".yml", "")
    print(" "*4, "public partial class {0}".format(convert(name)))
    print(" "*4, "{")
    with open('./author/sections/' + filename) as f:
        for api_call in load(f.read()):
            for key, value in api_call.items():
                function_name = convert(key)
                if type(value) is not str:
                    continue
                values = value.split(" ")
                return_type = "bool"
                if len(values) < 2:
                    continue
                if len(values) > 2:
                    return_type = convert(values[0])
                    request_type = values[2]
                    url = values[3]
                else:
                    request_type = values[0]
                    url = values[1]
                if request_type == "POST":
                    continue
                arguments = [convert(x)[1:] for x in url.split("/") if x[0] == ":"]
                args = []
                for arg in arguments:
                    if "id" in str.lower(arg):
                        args.append("int " + arg)
                    else:
                        args.append("string " + arg)
                arg_str = ", ".join(args)
                print(" "*8, "public async Task<{0}> {1}Async({1})".format(return_type, function_name, arg_str))
                print(" "*8, "{")
                print(" "*8, "}")
    print(" "*4, "}")



def main():
    for filename in os.listdir('./author/sections'):
        generate(filename)


main()
