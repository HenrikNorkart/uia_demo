# Project guidelines

## Docker

Do NOT use `--rm` when running containers on CAIR. Containers must persist after exit so they can be inspected with `docker ps -a`.

## LaTeX

When editing `.tex` files, make only the change that was explicitly requested. Do not rewrite surrounding text, update other values, or improve phrasing unless specifically asked.

## WandB

All interaction with WandB (querying runs, reading metrics, checking status) must go through the WandB MCP server tools. Do not use the wandb Python API in a container for querying — only use it when the MCP server is unavailable.
