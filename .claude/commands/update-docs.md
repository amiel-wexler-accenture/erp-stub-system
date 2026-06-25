 ---
 description: Update all README.md files and output raw CLAUDE.md suggestions
 allowed-tools: Read, Edit, Bash, Glob
 ---

 Update the project's README.md files to reflect the current state of the codebase, then output proposed
 CLAUDE.md additions as raw text for the user to review.

 ## Step 1: Discover README files

 Find all project README.md files (skip external data directories):

 ```bash
 find . -name "README.md" \
   ! -path "*/node_modules/*" \
   ! -path "*/legacy-erp/data/*" \
   ! -path "*/.git/*" \
   2>/dev/null

 Step 2: Audit each README

 Read each README and compare against the actual code:
 - Ports, URLs, environment variables
 Read each README and compare against the actual code:
 - Ports, URLs, environment variables
 - Install/run commands (check pyproject.toml, package.json)
 - Endpoint lists (check routers/)
 - Docker service names (check docker-compose.yml)

 Flag any stale or missing content.