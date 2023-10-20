$(document).ready(function () {
    function shareCode() {
        var code = codeEditor.getValue();
        var shareBtn = $('#share');
        var output = $('#output').text();
        var error = $('#error').text();

        shareBtn.prop('disabled', true);
        shareBtn.text('Share...');

        $.post('/api/share', { code: code, output: output, error: error }, function (response) {
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
            shareBtn.prop('disabled', false);
            shareBtn.text('Share');
        });
    }

    $("#share").click(shareCode);

    $(document).keydown(function (e) {
        if (e.ctrlKey && e.which === 83) { // Press Ctrl+S
            e.preventDefault();
            shareCode();
        }
    });
});