#!/usr/bin/env python
import os
import sys
import subprocess

def build_i3_msg(head_class):
    return f"[class=\"{head_class}\"] scratchpad show, resize set 1000 680, move position center"

def rotate(xs, direction):
    return xs[int(direction):] + xs[:int(direction)]

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
    rotate_direction = None
    if len(sys.argv) > 1:
      rotate_direction = sys.argv[1]
    script_path = os.path.abspath(__file__)
    script_dir  = os.path.dirname(script_path)
    store_name  = "class.store"
    store_path  = os.path.join(script_dir, store_name)
    assert_file_exists(store_path)
    try:
        with open(store_path, "r+") as f:
            win_classes = [line.rstrip() for line in f]
            head = win_classes[0]
            if rotate_direction:
                rotated = rotate(win_classes, rotate_direction)
                head = rotated[0]
                f_content = compile_to_contents(
                    rotate(win_classes, rotate_direction))
                seek_and_overwrite(f, f_content)
            subprocess.run(["i3-msg", build_i3_msg(head)])

    except Exception as e:
        print(f"ERROR: stuff gone wrong because of:\n${str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
