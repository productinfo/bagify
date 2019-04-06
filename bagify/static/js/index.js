

function indexPage() {
    function setItemsCollapse() {
        let radios = document.querySelectorAll('.items-scroll .header input');

        radios.forEach(radio => radio.addEventListener('input', evt => {
            if(!evt.target.checked) return;

            let target = $(evt.target.value);
            let oposing = (evt.target.value == '#newItems')? $('#popularItems') : $('#newItems');

            oposing.collapse('hide');
            target.collapse('show');

        }));

        let collapseId = $('.items-scroll .header input:checked').val();
        $(collapseId).collapse('show')
    }

    function getTotalItemsWidth(items) {
      const { left } = items[0].getBoundingClientRect();
      const { right } = items[items.length - 1].getBoundingClientRect();
      return right - left;
    }

    function scrollItems(direction) {
        const scroll = document.querySelector('.scrolling-wrapper.show');
        const scroll_width = scroll.offsetWidth;

        const items = scroll.querySelectorAll('.card-naked');
        const total_width = getTotalItemsWidth(items);

        const maxXOffset = 0;
        const minXOffset = - (total_width - scroll_width);

        const newScroll = (direction == 'right') ? scroll_width + scroll.scrollLeft : scroll.scrollLeft - scroll_width;

        scroll.scroll({
              left: newScroll,
              behavior: 'smooth'
            });
    }


    function init() {
        $('[data-toggle="tooltip"]').tooltip()
        setItemsCollapse();


        document.querySelector('.arrow.left').addEventListener('click', () => scrollItems('left'));
        document.querySelector('.arrow.right').addEventListener('click', () => scrollItems('right'));



    }

    init();
}
document.addEventListener('DOMContentLoaded', ()=> {
    indexPage();
});
