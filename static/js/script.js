var codeTextArea = document.getElementById("code");
var codeEditor = CodeMirror.fromTextArea(codeTextArea, {
    lineNumbers: true,
    mode: "python",
    theme: "monokai"
});

codeEditor.on("keydown", function (editor, event) {
    var openChars = ["(", "{", "[", "\"", "'", "<"];
    var closeChars = [")", "}", "]", "\"", "'", ">"];
    var cursor = codeEditor.getCursor();

    if (event.key && openChars.includes(event.key)) {
        var closeChar = closeChars[openChars.indexOf(event.key)];
        codeEditor.replaceRange(event.key + closeChar, cursor);
        codeEditor.setCursor({ line: cursor.line, ch: cursor.ch + 1 });
        event.preventDefault();
    }

    if (event.ctrlKey && event.key === "/") {
        event.preventDefault();
        var cursor = codeEditor.getCursor();
        var selection = codeEditor.getSelection();

        if (selection) {
            var lines = selection.split("\n");
            var allCommented = true;

            for (var i = 0; i < lines.length; i++) {
                if (lines[i].trim() === "" || !lines[i].trim().startsWith("#")) {
                    allCommented = false;
                    break;
                }
            }

            if (allCommented) {
                var uncommentedLines = lines.map(function (line) {
                    return line.replace(/^# \s*/, "");
                });
                codeEditor.replaceSelection(uncommentedLines.join("\n"));
            } else {
                var commentedLines = lines.map(function (line) {
                    return "# " + line;
                });
                codeEditor.replaceSelection(commentedLines.join("\n"));
            }
        } else {
            var lineContent = codeEditor.getLine(cursor.line);
            if (lineContent.trim().startsWith("#")) {
                codeEditor.replaceRange(lineContent.replace(/^# \s*/, ""), { line: cursor.line, ch: 0 }, { line: cursor.line, ch: lineContent.length });
            } else {
                codeEditor.replaceRange("# " + lineContent, { line: cursor.line, ch: 0 }, { line: cursor.line, ch: lineContent.length });
            }
        }
    }
    if (event.key === "Tab") {
        event.preventDefault();
        codeEditor.replaceRange("  ", cursor);
    }
});