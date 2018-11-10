from yaml import load, dump
import os


def convert(word):
    return ''.join(x.capitalize() or '_' for x in word.split('_'))


def generate(filename):
    name = filename.replace(".yml", "")
    class_name = "Gitlab{0}Api".format(convert(name)).strip()
    class_set = set()
    #class_set.add(class_name)
    print(" "*4, "public partial class {0} : GitlabApiBase".format(class_name))
    print(" "*4, "{")
    print(" "*8, "private string _baseUrl;")
    print(" "*8, "public override string Token { get; set; }")
    print(" "*8, "public override WebClient WebClient { get; set; }")
    print(" "*8, "public {0}(string baseUrl, string token)".format(class_name))
    print(" "*8, "{")
    print(" "*12, "_baseUrl = baseUrl;")
    print(" "*12, "_baseUrl += \"api/v4/\";")
    print(" "*12, "Token = token;")
    print(" "*12, "WebClient = new WebClient();")
    print(" "*8, "}")
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
                    return_type = "Gitlab"+convert(values[0])
                    class_set.add(return_type)
                    request_type = values[2]
                    url = values[3]
                else:
                    request_type = values[0]
                    url = values[1]
                url.replace("?","")
                if request_type == "POST":
                    continue
                request_type = str.capitalize(str.lower(request_type))
                arguments = [convert(x)[1:] for x in url.split("/") if x[0] == ":"]
                args = []
                for arg in arguments:
                    if "id" in str.lower(arg) and str.lower(arg) != "projectid":
                        args.append("int " + arg)
                    else:
                        args.append("string " + arg)
                args.append("NameValueCollection nameValueCollection = null")
                arg_str = ", ".join(args)
                print(" "*8, "public async Task<{0}> {1}{2}Async({3})".format(return_type, request_type, function_name, arg_str))
                print(" "*8, "{")
                formated_url = "/".join(["{"+convert(x)[1:]+"}" if x[0] == ":" else x for x in url.split("/")])
                print(" " * 12, "var uri = new UriBuilder(_baseUrl + $@\"{0}\");".format(formated_url))
                print(" " * 12, "return await GetFromUrl<"+return_type+">(uri, nameValueCollection);")
                print(" "*8, "}")
    print(" "*4, "}")
    return class_set


def main():
    class_set = []
    for filename in os.listdir('./author/sections'):
        class_set += generate(filename)
    for c in class_set:
        print(" "*4, "public partial class {0} : GitlabApiElementBase".format(c))
        print(" " * 4,"{")
        print(" " * 4,"}")


main()
