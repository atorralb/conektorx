# Replace all occurrences of '${{ project.modelVersion }}' with '4.0.0' in a file

input_file = "pom.yml.schema"  # Replace with your file path
output_file = "test.yml"  # Replace with your desired output file path

# Dictionary of replacements: {"string_to_replace": "replacement", ...}
replacements = {
    "${{ project.modelVersion }}": "4.0.0",
    "${{ parent.groupId }}": "org.springframework.boot",
}

with open(input_file, "r", encoding="utf-8") as f:
    content = f.read()

for old, new in replacements.items():
    content = content.replace(old, new)

with open(output_file, "w", encoding="utf-8") as f:
    f.write(content)
