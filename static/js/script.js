$(document).ready(function () {
    $("#execute").click(function () {        
        var code = codeEditor.getValue();
        var executeBtn = $(this);
        document.getElementById("output").innerText = "";
        document.getElementById("error").innerText = "";

        executeBtn.prop('disabled', true);
        executeBtn.text('Executing...');

        $.ajax({
            url: '/execute',
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
    });
});