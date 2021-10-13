(function () {
    const form = document.forms[0]
    form.addEventListener("submit", function (event) {
        if (!form.checkValidity()) {
            event.preventDefault()
            event.stopPropagation()
        }
        form.classList.add("was-validated")
    }, false)
})()