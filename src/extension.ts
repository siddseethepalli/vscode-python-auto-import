import * as vscode from "vscode";

import * as fixer from "./fixer";

export function activate(context: vscode.ExtensionContext) {
  context.subscriptions.push(
    vscode.commands.registerCommand(
      "python-auto-importer.autoImportPython",
      () => {
        fixer.fixImports();
      }
    )
  );

  context.subscriptions.push(
    vscode.commands.registerCommand(
      "python-auto-importer.buildIndex",
      () => {
        fixer.buildIndex();
      }
    )
  );
}

export function deactivate() { }
