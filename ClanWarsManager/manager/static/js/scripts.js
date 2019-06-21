$(document).ready(function () {
    M.AutoInit();
    $(".dropdown-trigger").dropdown({
        coverTrigger: false
    });
});

function toast(message, icon = null) {
    const msgHtml = `<span>${message}</span>`;
    const msgIcon = icon == null ? '' : `<i class='material-icons'>${icon}</i>`
    M.toast({ html: `${msgHtml}${msgIcon}`});
}