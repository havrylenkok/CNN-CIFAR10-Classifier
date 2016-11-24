/**
 * Created by robben1 on 10/16/16.
 */


$(window).on('load', function () {
    $(".loader").fadeOut("slow");
});

$(document).ready(function () {

    var files;
    $('#knowform').hide();
    $('#container').hide();
    $('#result').hide();
    $('#again').hide();

    // Add scrollspy to <body>
    $('body').scrollspy({target: ".navbar", offset: 50});

// Add smooth scrolling on all links inside the navbar
    $("#myNavbar a").on('click', function (event) {

        // Make sure this.hash has a value before overriding default behavior
        if (this.hash !== "") {

            // Prevent default anchor click behavior
            event.preventDefault();

            // Store hash
            var hash = this.hash;

            // Using jQuery's animate() method to add smooth page scroll
            // The optional number (800) specifies the number of milliseconds it takes to scroll to the specified area
            $('html, body').animate({
                scrollTop: $(hash).offset().top
            }, 800, function () {

                // Add hash (#) to URL when done scrolling (default click behavior)
                window.location.hash = hash;
            });

        } // End if

    });

    $('input').iCheck({
        // checkboxClass: 'icheckbox_square-red',
        radioClass: 'iradio_square-red',
        increaseArea: '20%' // optional
    });

    $('input').on('ifChecked', function (event) {
        if (this.value == 'know') {
            // console.log(this.value);
            // console.log($('#knowform'));
            $('#knowform').fadeIn();
        } else {
            $('#knowform').fadeOut();
        }
    });

    $('#again').click(function () {
        window.location.reload();
    });

    var bar = new ProgressBar.SemiCircle('#container', {
        easing: 'easeInOut',
        strokeWidth: 6,
        color: '#FFEA82',
        trailColor: '#eee',
        trailWidth: 1,
        duration: 4500,
        svgStyle: null,
        text: {
            value: '',
            alignToBottom: true,
            // style: {
//         // position: 'absolute',
//         left: '50%',
            // top: '15%',
//         // padding: '0px',
//         // margin: '0px',
//         // bottom: '0px',
// }
        },
        from: {
            color: '#FFEA82'
        }
        ,
        to: {
            color: '#ED6A5A'
        }
        ,
        step: (state, bar) => {
            bar.path.setAttribute('stroke', state.color);
            var value = Math.round(bar.value() * 100);
            if (value === 0) {
                bar.setText('');
            }
            else {
                bar.setText(value);
            }
            bar.text.style.color = state.color;
        }
    });

    $('input[type=file]').on('change', function () {
        files = event.target.files;
        console.log(files);
    });

    $('#sbm').click(function () {
        var res = {gen: false, type: ''};
        var data = new FormData();
        data.append('file', files[0]);
        $.ajax({
            // url: 'http://127.0.0.1:5000/upload',
            url: '/upload',
            type: 'POST',
            data: data,
            cache: false,
            dataType: 'json',
            processData: false,
            contentType: false,
            success: function (data, tStatus, jqXHR) {
                if (typeof data.error === 'undefined') {
                    console.log(data);
                    res.gen = true;
                    res.type = data.class_of_image;
                    if ($('#know:checked').length > 0) {
                        var know = {
                            first: $('#first-class').find('option:selected').text(),
                            second: $('#second-class').find('option:selected').text()
                        };
                        if (data.class_of_image == know.second) {
                            $('#result-span').text(know.second);
                        }
                        else {
                            $('#result-span').text(know.first);
                        }
                    } else {
                        $('#result-span').text(data.class_of_image);
                    }
                } else {
                    console.log('ERRORS FILE SUBMIT: ' + data.error);
                }
                bar.animate(1);
            },
            error: function (xhr, tStatus, errorThrown) {
                console.log('ERRORS: ' + tStatus);
                bar.animate(0);
                $('#result p').text("");
                $('#resp').text("Sorry, network can't classify image.");

            }
        }).always(function () {
            setTimeout(function () {
                setTimeout(function () {
                    $('#container').fadeOut();
                    setTimeout(function () {
                        $('#result').fadeIn();
                        $('#again').fadeIn();
                    }, 400);
                }, 4550);
            });
        });
        $('#input-form').fadeOut();
        setTimeout(function () {
            $('#container').fadeIn(800);
            bar.text.style.fontSize = '3rem';
            bar.text.style.top = '18%';
            bar.animate(0.63);
        }, 400);

    });

    $('#file').change(function () {
        var filename = $('#file').val().split('\\').pop();
        $('#file-status').text(filename);
    });

})
;

