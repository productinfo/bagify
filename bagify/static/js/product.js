function product() {
    const view = {
        display: document.getElementById('displayed-image'),
        frame_rows: document.querySelectorAll('.frame_row'),
        color_buttons: document.querySelector('.color-option').parentNode,
        add_to_cart: document.getElementById('add_to_cart_btn'),

        sendToaster(options) {
            const toaster = document.querySelector('.toasty');
            document.querySelector('.toasty .title').innerHTML = options.title;
            document.querySelector('.toasty .body').innerHTML = options.body;
            toaster.querySelector('div').classList.add(options.color);

            toaster.hidden = false;
            setTimeout(() => toaster.hidden=true, 2000);
        },
    }

    const data = {
        cart: ( getCookie('cart')? JSON.parse(getCookie('cart')) : [] ),
        item_id: document.querySelector('[data-id]').dataset.id,
        item_name: document.querySelector('[data-name]').dataset.name,
        selected_color: null,
    }


    function showImage() {
        const src = document.querySelector(`input[name=${data.selected_color}]:checked`).value;
        view.display.src = src;
    }

    function showFrames() {
        const value = document.querySelector(`input[name="colors"]:checked`).value;
        data.selected_color = value;

        for(row of view.frame_rows) {
            row.hidden = (row.dataset.color === value) ? false : true;
        }
    }

    function addToCart() {
        const item = {
            id: data.item_id,
            color: data.selected_color,
        }

        data.cart.push(item);
        setCookie('cart', JSON.stringify(data.cart), 7);

        view.sendToaster({color:'success', body:`${data.selected_color.toUpperCase()} ${data.item_name} added to cart.`, title:'Success'})
    }

    function init() {
        showFrames();
        showImage();

        view.color_buttons.addEventListener('input', () => {
            showFrames();
            showImage();
        });

        view.frame_rows[0].parentElement.addEventListener('input', showImage)

        view.add_to_cart.addEventListener('click', addToCart)
    }

    init();
}

document.addEventListener('DOMContentLoaded', product)
