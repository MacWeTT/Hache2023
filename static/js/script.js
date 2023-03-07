// var countDownDate = new Date("March 26, 2023 10:00:00").getTime();

// var x = setInterval(function () {

//     // Get today's date and time
//     var now = new Date().getTime();

//     // Find the distance between now and the count down date
//     var distance = countDownDate - now;

//     // Time calculations for days, hours, minutes and seconds
//     document.getElementById("days").innerText = Math.floor(distance / (1000 * 60 * 60 * 24));
//     document.getElementById("hours").innerText = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
//     document.getElementById("minutes").innerText = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
//     document.getElementById("seconds").innerText = Math.floor((distance % (1000 * 60)) / 1000);
//     // If the count down is over, write some text
// }, 1000);


const answerField = document.getElementById("temp-ans");
const hint = document.getElementById("hint").textContent;

try {
    document.getElementById('buttonHint').addEventListener('click', () => {
        iziToast.info({
            title: 'Hint',
            message: hint,
            position: 'bottomCenter',
            timeout: false,
            closeOnClick: true,
            buttons: [
                ['<button>Click to Copy</button>', function (instance, toast) {
                    navigator.clipboard.writeText(hint);
                }, true],
            ],
        });
    })
} catch (err) {
    console.log("Error occured.")
}



document.querySelector('.check').addEventListener("click", (e) => {
    if (answerField.value) {
        check(e)
    }
});

answerField.addEventListener("keyup", nice)

function nice(e) {
    const val = answerField.value

    if (e.keyCode === 13 && val) {
        e.preventDefault();

        check(e);
    }
}
function check(e) {
    document.getElementById("button-addon2").style.display === "none";
    let form = $('#answer-form');
    $('#answer-form #id_answer').val($('#temp-ans').val());
    $.ajax({
        type: 'POST',
        url: form.attr("action"),
        data: form.serialize(),
        success: function (response) {
            const response_div = document.getElementById("response");
            if (response.winner === true) {
                location.reload();
            }
            else {
                if (response.correct === true) {
                    document.getElementById("button-addon2").disabled = false;
                    iziToast.success({
                        title: 'Correct',
                        message: 'Great, Fetching Your Next Question !',
                    });
                    setTimeout(() => location.reload(), 2000);
                }
                else if (response.correct === false) {
                    document.getElementById("button-addon2").disabled = false;
                    if (response.customCode == 20) {
                        iziToast.warning({
                            position: 'topRight',
                            title: 'Gift For You!',
                            buttons: [

                                ['<button>Click Here</button>', function (instance, toast) {
                                    window.location.replace(response.errorM);
                                }, true]
                            ]
                        });

                    } else if (response.customCode == 10) {
                        createBalloons(10)
                    } else {
                        iziToast.warning({
                            position: 'topRight',
                            title: 'Incorrect',
                            message: response.errorM,
                        });
                    }



                    $('#answer-form').trigger('reset');
                    $('#temp-ans').val('');
                    setTimeout(() => response_div.innerHTML = "", 3000);
                }
                else {
                    iziToast.error({
                        position: 'topRight',
                        message: "Error!",
                    });
                }
            }
        },
        error: function (response) {
            console.log(response)
            iziToast.error({
                position: 'topRight',
                message: "Error!",
            });
        }
    });
}



function random(num) {
    return Math.floor(Math.random() * num)
}

function getRandomStyles() {
    var r = random(255);
    var g = random(255);
    var b = random(255);
    var mt = random(200);
    var ml = random(50);
    var dur = random(5) + 5;
    return `
    background-color: rgba(${r},${g},${b},0.7);
    color: rgba(${r},${g},${b},0.7); 
    box-shadow: inset -7px -3px 10px rgba(${r - 10},${g - 10},${b - 10},0.7);
    margin: ${mt}px 0 0 ${ml}px;
    animation: float ${dur}s ease-in infinite
    s`
}

function createBalloons(num) {
    var balloonContainer = document.getElementById("balloon-container")
    for (var i = num; i > 0; i--) {
        var balloon = document.createElement("div");
        balloon.className = "balloon";
        balloon.id = `balloon${i}`
        balloon.style.cssText = getRandomStyles(); balloonContainer.append(balloon);
    }

    setTimeout(deleteballons, 6000);

}

function deleteballons() {
    for (var i = 10; i > 0; i--) {
        var balloon = document.getElementById(`balloon${i}`)
        balloon.remove()
    }
}



