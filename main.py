#!/usr/bin/env python
import os
import sys
import subprocess

def build_i3_msg(curr):
    return (f"[class=\"{curr}\"] scratchpad show, "
             "resize set 1000 680, move position center")

def show_and_hide_prev(classes, direction):
    d = int(direction)
    curr = classes[0]
    prev, *_ = classes[(-1) * d:]
    subprocess.run(["i3-msg", build_i3_msg(prev)])
    subprocess.run(["i3-msg", build_i3_msg(curr)])
    subprocess.run(["i3-msg", build_i3_msg(curr)])

def show_head_class(head_class):
    subprocess.run(["i3-msg", build_i3_msg(head_class)])

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

def exit_if_locked(l):
    if int(l):
        sys.exit(0)

def turn_lock(l):
    return str(int(not int(l)))

def main():
    rotate_direction = None
    if len(sys.argv) > 1:
      rotate_direction = sys.argv[1]
    script_path = os.path.abspath(__file__)
    script_dir  = os.path.dirname(script_path)
    store_name  = "class.store"
    lock_name   = "lock.store"
    store_path  = os.path.join(script_dir, store_name)
    lock_path   = os.path.join(script_dir, lock_name)
    assert_file_exists(store_path)
    try:
        with open(store_path, "r+") as f, open(lock_path, "r+") as l:
            lock_status, *_ = [line.rstrip() for line in l]
            win_classes     = [line.rstrip() for line in f]
            print(lock_status)
            if rotate_direction:
                exit_if_locked(lock_status)
                win_classes = rotate(win_classes, rotate_direction)
                f_content = compile_to_contents(win_classes)
                seek_and_overwrite(f, f_content)
                show_and_hide_prev(win_classes, rotate_direction)
                sys.exit(0)
            seek_and_overwrite(l, turn_lock(lock_status))
            show_head_class(win_classes[0])
    except Exception as e:
        print(f"ERROR: stuff gone wrong because of:\n${str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
