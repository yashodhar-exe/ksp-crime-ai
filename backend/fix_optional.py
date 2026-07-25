import os
import re

def fix_optional(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()

                # Replace "Type | None" with "Optional[Type]"
                new_content = re.sub(r'([A-Za-z0-9_]+)\s*\|\s*None', r'Optional[\1]', content)
                # Also handle "None | Type"
                new_content = re.sub(r'None\s*\|\s*([A-Za-z0-9_]+)', r'Optional[\1]', new_content)

                if new_content != content:
                    # Make sure Optional is imported
                    if "from typing import Optional" not in new_content and "typing import" not in new_content:
                        # Insert after __future__ import if it exists
                        if new_content.startswith("from __future__ import annotations"):
                            new_content = new_content.replace("from __future__ import annotations", "from __future__ import annotations\nfrom typing import Optional", 1)
                        else:
                            new_content = "from typing import Optional\n" + new_content
                    elif "typing import" in new_content and "Optional" not in new_content:
                        new_content = re.sub(r'from typing import (.*)', r'from typing import Optional, \1', new_content, count=1)
                    
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"Fixed {path}")

fix_optional("app/models")
fix_optional("app/schemas")
fix_optional("app/api")
fix_optional("app/services")
fix_optional("app/core")
fix_optional("app/db")
