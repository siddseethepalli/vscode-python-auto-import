import * as vscode from "vscode";

export function getExtensionPythonPath(): string {
    return extensionConfig("pythonInterpreterPath");
}


export function getCurrentPythonPath(): string | null {
    let pyBin = "";

    const file = vscode.window.activeTextEditor?.document.uri;
    const workspace = vscode.workspace.getWorkspaceFolder(file!);

    pyBin = vscode.workspace.getConfiguration("python", workspace?.uri).get("defaultInterpreterPath") as string;

    if (pyBin) {
        return pyBin;
    }

    return null;
}


function extensionConfig(property: string): string {
    const config = vscode.workspace.getConfiguration("python=auto-importer");
    const subConfig = config.get(property);

    if (typeof subConfig === "undefined") {
        vscode.window.showErrorMessage("No python interpreter configured for extension");
        throw new Error(`Configuration: ${property} doesn't exist`);
    }

    return subConfig as string;
}
