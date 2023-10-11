$(document).ready(function () {
    $('#share').click(function () {
        var code = codeEditor.getValue();
        var output = $('#output').text();
        var error = $('#error').text();

        $.post('/share', { code: code, output: output, error: error }, function (response) {
            var url = response.url;

            const textToCopy = url;
            const tempTextarea = document.createElement('textarea');
            tempTextarea.value = textToCopy;
            document.body.appendChild(tempTextarea);
            tempTextarea.select();
            document.execCommand('copy');
            document.body.removeChild(tempTextarea);

            Swal.fire(
                'Successful!',
                'Text copied to clipboard!',
                'success'
            )
        });
    });
});