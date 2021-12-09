const notificacionSwal=(titleText, text, icon, confirmationButtomText) => {
    Swal.fire({
        titleText: titleText,
        text: text,
        icon: icon,
        confirmButtomText: confirmationButtomText,
    });
};
