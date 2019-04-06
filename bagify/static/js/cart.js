function cart() {
    const view = {
        container: document.querySelector('.cart'),
        rows: document.getElementsByClassName('cart-item'),

        showTotal(price, items) {
            document.querySelector('.total-price').innerHTML = (price) ? '$' + price : '';
            document.querySelector('.total-items').innerHTML = items;
        }
    }

    const data = {
        cart: cart,
    }

    function init() {
        getTotal();

        view.container.addEventListener('click', evt => {
            if(evt.target.classList.contains('remove')) handleRemove(evt)
        })

    }

    function getTotal() {
        let count = 0;
        for(row of view.rows) {
            count += +row.dataset.price;
        }
        const numb = view.rows.length;
        view.showTotal(count, numb);
    }

    function handleRemove(evt) {
        console.log('here');
        const row = evt.target.closest('.cart-item')
        const id = row.dataset.id;
        const color = row.dataset.color;

        row.remove();
        removeItem(id, color);
        getTotal();

    }

    function removeItem(id, color) {
        let cart = getCookie('cart');
        if(!cart) return 1;

        cart = JSON.parse(cart);

        const cartId = cart.findIndex(item => item.id === id && item.color === color);
        cart.splice(cartId, 1);

        setCookie('cart', JSON.stringify(cart), 7)

    }
    init();
}

document.addEventListener('DOMContentLoaded', cart);
