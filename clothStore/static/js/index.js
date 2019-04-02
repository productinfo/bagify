function getCookie(cname) {
  const name = cname + "=";
  const ca = document.cookie.split(';');
  for(var i = 0; i < ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

function setCookie(cname, cvalue, exdays) {
  let d = new Date();
  d.setTime(d.getTime() + (exdays*24*60*60*1000));
  const expires = "expires="+ d.toUTCString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

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

    function addToCart(evt) {
        const target = evt.target;
        if(!target.classList.contains('cart-button')) return;

        let newProduct = +target.dataset.id;
        let cart = getCookie('cart') || '[]';

        cart = JSON.parse(cart);
        cart.push(newProduct);
        cart = JSON.stringify(cart);
        setCookie('cart', cart, 7);



    }

    function init() {
        $('[data-toggle="tooltip"]').tooltip()
        setItemsCollapse();

        document.querySelector('.arrow.left').addEventListener('click', () => scrollItems('left'));

        document.querySelector('.arrow.right').addEventListener('click', () => scrollItems('right'));

        document.querySelector('.items-scroll').addEventListener('click', addToCart)

        document.querySelector('.alert');


    }

    init();
}
document.addEventListener('DOMContentLoaded', ()=> {
    indexPage();
});
