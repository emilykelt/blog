import os
import sys
import datetime
import subprocess
from slugify import slugify  

# === CONFIG ===
POSTS_DIR = "_posts"
DEFAULT_LAYOUT = "post"
GIT_AUTO_PUSH = True

def read_txt_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def generate_post_filename(title, date):
    slug = slugify(title)
    date_str = date.strftime("%Y-%m-%d")
    return f"{date_str}-{slug}.md"

def create_post(title, content, date=None):
    if not date:
        date = datetime.datetime.now()

    filename = generate_post_filename(title, date)
    filepath = os.path.join(POSTS_DIR, filename)

    # YAML front matter
    front_matter = f"""---
layout: {DEFAULT_LAYOUT}
title: "{title}"
date: {date.strftime('%Y-%m-%d %H:%M:%S')}
---
"""

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(front_matter + '\n' + content)

    print(f"✅ Created post: {filepath}")
    return filepath

def git_commit_and_push(filepath):
    try:
        subprocess.run(["git", "add", filepath], check=True)
        subprocess.run(["git", "commit", "-m", f"Add blog post: {os.path.basename(filepath)}"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("🚀 Post pushed to GitHub!")
    except subprocess.CalledProcessError:
        print("❌ Git push failed. Are you in a Git repo with permissions set up?")

def main(txt_file_path):
    if not os.path.exists(POSTS_DIR):
        os.makedirs(POSTS_DIR)

    content = read_txt_file(txt_file_path)
    # First line = title
    lines = content.strip().split('\n')
    title = lines[0].strip()
    body = '\n'.join(lines[1:]).strip()

    post_path = create_post(title, body)

    if GIT_AUTO_PUSH:
        git_commit_and_push(post_path)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python upload.py <post.txt>")
        sys.exit(1)

    main(sys.argv[1])
