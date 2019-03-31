function indexPage() {
    function setItemsCollapse() {
        let radios = document.querySelectorAll('.items-scroll .header input');

        radios.forEach(radio => radio.addEventListener('input', evt => {
            if(!evt.target.checked) return;

            let target = $(evt.target.value);
            let oposing = (evt.target.value == '#newItems')? $('#popularItems') : $('#newItems');

            target.removeClass('rollOut');
            target.collapse('show');
            oposing.addClass('rollOut');
            oposing.collapse('hide')

        }));

        let collapseId = $('.items-scroll .header input:checked').val();
        $(collapseId).collapse('show')
    }


    function init() {
        setItemsCollapse();
    }

    init();
}
document.addEventListener('DOMContentLoaded', indexPage);
