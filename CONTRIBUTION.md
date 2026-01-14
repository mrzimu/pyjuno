## Development environment setup

### Step 1: Install uv

For macOS and Linux, run:

```shell
curl -LsSf https://astral.sh/uv/install.sh | sh
```

For Windows, run:

```shell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

> [!TIP]
> You can refer [this link](https://docs.astral.sh/uv/getting-started/installation/) to install `uv`.

### Step 2: Create and setup virtual environment

```shell
python3 -m venv .venv
source .venv/bin/activate
uv sync
```

> [!TIP]
> If the synchronization is too slow, you can run `export UV_DEFAULT_INDEX="https://pypi.tuna.tsinghua.edu.cn/simple"` to change the download mirror.

### Step 3: Setup pre-commit

```shell
pre-commit install
```

This may take several minutes. It downloads hooks from github repositories.

## Rebuild pyjuno when C++ files are modified

Every time you modify the C++ files, run following commands to rebuild the project:

```shell
uv pip install -e .
```
