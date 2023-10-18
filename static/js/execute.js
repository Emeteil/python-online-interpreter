$(document).ready(function () {
    function executeCode() {
        var code = codeEditor.getValue();
        var executeBtn = $("#execute");
        document.getElementById("output").innerText = "";
        document.getElementById("error").innerText = "";

        executeBtn.prop('disabled', true);
        executeBtn.text('Executing...');

        $.ajax({
            url: '/api/execute',
            type: 'POST',
            data: JSON.stringify({ 'code': code }),
            contentType: 'application/json',
            success: function (response) {
                $("#output").text(response.output);
                $("#error").text(response.error);

                executeBtn.prop('disabled', false);
                executeBtn.text('Execute');
            }
        });
    }

    $("#execute").click(executeCode);

    $(document).keydown(function (e) {
        if (e.which === 119) { // Press F8
            executeCode();
        }
    });
});
