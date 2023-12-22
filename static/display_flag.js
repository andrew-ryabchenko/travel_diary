const countryInput = document.querySelector('input#country');
const countryFlagIcon = document.querySelector('span#countryFlag');

countryInput.addEventListener("focusout", (e) => {
    let xhttp = new XMLHttpRequest();
    xhttp.open("get", `/flag?country=${e.target.value}`, true);
    xhttp.onload = (e) => {
        if (xhttp.status == 200){
            countryFlagIcon.innerHTML = xhttp.responseText;
        }
    }
    xhttp.send();
})