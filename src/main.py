import os, shutil

def main():
    print("running SSG...")
    copy_all_files("./static", "./public")

def copy_all_files(source_dir, dest_dir):
    print(f"Copying all files from {source_dir}/ to {dest_dir}/")
    if os.path.exists(dest_dir):
        print(f"Deleting old {dest_dir}/")
        shutil.rmtree(dest_dir)
    os.mkdir(dest_dir)
    contents = os.listdir(source_dir)
    for item in contents:
        print(f"Processing {source_dir}/{item}")
        source_item_path = os.path.join(source_dir, item)
        dest_item_path = os.path.join(dest_dir, item)
        if os.path.isfile(source_item_path):
            print(f"Copying {source_item_path} to {dest_item_path}")
            shutil.copy(source_item_path, dest_item_path)
        else:
            copy_all_files(source_item_path, dest_item_path)

if __name__ == "__main__":
    main()
