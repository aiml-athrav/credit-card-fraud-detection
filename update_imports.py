import os

backend_dir = r"c:\Users\TANVI\OneDrive\Desktop\credit-card-fraud-detection\backend"
updated_count = 0

for root, dirs, files in os.walk(backend_dir):
    for file in files:
        if file.endswith(".py"):
            filepath = os.path.join(root, file)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            if "backend.app." in content:
                new_content = content.replace("backend.app.", "")
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Updated {filepath}")
                updated_count += 1

print(f"Total files updated: {updated_count}")
