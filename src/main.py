from os.path import dirname
import os, shutil

from htmlnode import markdown_to_html_node

def main():
    print("running SSG...")
    copy_all_files("./static", "./public")
    generate_pages_recursively("content", "template.html", "public")

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

def extract_title(markdown):
    for line in markdown.split("\n"):
        if line[:2] == "# ":
            return line[2:]
    raise Exception("No '# ' header found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    from_file = open(from_path)
    from_contents = from_file.read()
    template_file = open(template_path)
    template_contents = template_file.read()
    title = extract_title(from_contents)
    html = markdown_to_html_node(from_contents).to_html()
    title_splits = template_contents.split("{{ Title }}")
    html_with_title = title_splits[0] + title + title_splits[1]
    content_splits = html_with_title.split("{{ Content }}")
    html_with_content = content_splits[0] + html + content_splits[1]
    if not os.path.exists(dirname(dest_path)):
        os.makedirs(dirname(dest_path))
    out_file = open(dest_path, "w")
    out_file.write(html_with_content)
    from_file.close()
    template_file.close()
    out_file.close()

def generate_pages_recursively(dir_path_content, template_path, dest_dir_path):
    contents = os.listdir(dir_path_content)
    for item in contents:
        item_path = os.path.join(dir_path_content, item)
        if os.path.isfile(item_path) and item[-3:] == ".md":
            generate_page(item_path, template_path, os.path.join(dest_dir_path, item[:-3] + ".html"))
        else:
            generate_pages_recursively(item_path, template_path, os.path.join(dest_dir_path, item))

if __name__ == "__main__":
    main()
