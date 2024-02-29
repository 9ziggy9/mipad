#!/usr/bin/env python
import os
import sys

def rotate(xs):
    return xs[1:] + xs[:1]

def seek_and_overwrite(file, content):
    file.seek(0)
    file.write(content)
    file.truncate()

def compile_to_contents(xs):
    return "\n".join(xs)

def usage():
    print("USAGE")
    print("Here how you do:")

def assert_file_exists(file_path):
    if not os.path.exists(file_path):
      print(f"ERROR: class store at {file_path} no existy, friendo")
      usage()
      sys.exit(1)

def main():
    store_path = "./class.store"
    assert_file_exists(store_path)

    try:
        with open(store_path, "r+") as f:
            win_classes = [line.rstrip() for line in f]
            f_content = compile_to_contents(rotate(win_classes))
            seek_and_overwrite(f, f_content)
    except Exception as e:
        print(f"ERROR: stuff gone wrong because of:\n${str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
