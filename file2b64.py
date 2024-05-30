import base64

def ftob64(fpath):
    with open(fpath, "rb") as file:
        b63estring = base64.b64encode(file.read()).decode("utf-8")
    return b63estring

if __name__ == "__main__":
    fpath = input("filepath: ")
    try:
        base64_string = ftob64(fpath)
        print("Base64:")
        print(base64_string)
    except FileNotFoundError:
        print("not found.")