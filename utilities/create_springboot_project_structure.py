"""
demo/
├── pom.xml
└── src/
    ├── main/
    │   ├── java/
    │   │   └── com/example/demo/
    │   └── resources/
    │       └── application.properties
    └── test/
        ├── java/
        │   └── com/example/demo/
        └── resources/
"""
import os

def create_spring_boot_project_structure(base_dir, base_package):
    package_path = base_package.replace('.', '/')
    dirs = [
        f"{base_dir}/src/main/java/{package_path}",
        f"{base_dir}/src/main/resources",
        f"{base_dir}/src/test/java/{package_path}",
        f"{base_dir}/src/test/resources",
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    # Add optional common files
    open(f"{base_dir}/src/main/resources/application.properties", 'a').close()
    open(f"{base_dir}/pom.xml", 'a').close()  # comment this if you want gradle instead

# Example usage:
create_spring_boot_project_structure('../demo', 'com.example.demo')
