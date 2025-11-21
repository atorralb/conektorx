import re

# Replace with your actual file path
filepath = "YourJavaFile.java"

with open(filepath, "r") as file:
    content = file.read()

# Substitute @GetMapping() with @GetMapping("mystring")
new_content = re.sub(r'@GetMapping\s*\(\s*\)', '@GetMapping("mystring")', content)

# Save changes back to the file (optional, or use a different filename to avoid overwriting)
with open(filepath, "w") as file:
    file.write(new_content)