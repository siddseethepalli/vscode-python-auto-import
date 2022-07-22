import * as vscode from "vscode";

import * as path from "path";
import * as cp from "child_process";

import * as utils from "./utils";

export function fixImports(): void {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        vscode.window.showErrorMessage("There's no active editor");
        return;
    }

    const filePath = editor.document.fileName;
    if (!filePath.endsWith(".py")) {
        vscode.window.showErrorMessage("This is not a python file");
        return;
    }

    const indexPath = getIndexPath(filePath);
    if (!indexPath) {
        vscode.window.showErrorMessage("Unable to create index");
        return;
    }

    const transformedCode = getFixedFileContents(filePath, indexPath);
    if (!transformedCode) {
        return;
    }

    write(editor, transformedCode);
}

function getIndexPath(filePath: string): string | null {
    const pyBin = utils.getExtensionPythonPath();
    if (!pyBin) {
        vscode.window.showErrorMessage("No python interpreter found");
        return null;
    }

    const extPath = vscode.extensions.getExtension("siddseethepalli.python-auto-importer")
        ?.extensionPath as string;
    const script = path.join(extPath, "indexer", "main.py");

    try {
        const result = cp.execSync(`${pyBin} ${script} ${filePath}`);
        return result.toString();
    } catch (error: any) {
        return null;
    }
}

function getFixedFileContents(filePath: string, indexPath: string): string | null {
    const pyBin = utils.getExtensionPythonPath();
    if (!pyBin) {
        vscode.window.showErrorMessage("No python interpreter found");
        return null;
    }

    const extPath = vscode.extensions.getExtension("siddseethepalli.python-auto-importer")
        ?.extensionPath as string;
    const script = path.join(extPath, "fixer", "main.py");

    try {
        const result = cp.execSync(`${pyBin} ${script} ${filePath} --index-path ${indexPath}`);
        return result.toString();
    } catch (error: any) {
        vscode.window.showErrorMessage(error.message);
        return null;
    }
}

function write(editor: vscode.TextEditor, code: string): void {
    const edit = new vscode.WorkspaceEdit();

    const wholeDocument = new vscode.Range(
        new vscode.Position(0, 0),
        new vscode.Position(editor.document.lineCount, 0)
    );
    const updateCode = new vscode.TextEdit(wholeDocument, code);

    edit.set(editor.document.uri, [updateCode]);

    vscode.workspace.applyEdit(edit).then(() => {
        editor.document.save().then(() => {
            formatFile(editor.document.fileName);
        });
    });
}

function formatFile(filePath: string): void {
    const pyBin = utils.getCurrentPythonPath();
    if (!pyBin) {
        vscode.window.showErrorMessage("No python interpreter found");
        return;
    }

    const dirPath = filePath.substring(0, filePath.lastIndexOf('/'));

    cp.execSync(`cd ${dirPath} && ${pyBin} -m isort ${filePath}`);
    cp.execSync(`cd ${dirPath} && ${pyBin} -m black ${filePath}`);
}
