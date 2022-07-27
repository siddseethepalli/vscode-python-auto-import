# Python Auto Importer

## Setup

### Installing the extension

```bash
npm install -g vsce
vsce package  # This step will output a path to a vsix file
code --install-extension <path-to-vsix>
```

### Extension setup

Create a new Python 3.10 virtualenv.
```bash
python3.10 -m venv <path-to-venv>
```
In your vscode `settings.json` set `python-auto-importer.pythonInterpreterPath` to the virtualenv's python.

## Key bindings

Fix imports (for the current file): `Cmd + Shift + I`

Rebuild index (for the current project): `Cmd + Shift + J`
