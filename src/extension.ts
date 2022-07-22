import * as vscode from "vscode";

import * as fixer from "./fixer";

export function activate(context: vscode.ExtensionContext) {
  let disposable = vscode.commands.registerCommand(
    "python-auto-importer.autoImportPython",
    () => {
      fixer.fixImports();
    }
  );

  context.subscriptions.push(disposable);
}

export function deactivate() { }
