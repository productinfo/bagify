function account() {
    const view = {
        showModal(content) {
            const modal = document.querySelector('.modal');
            document.querySelector('.modal-title').innerHTML = `Order n.${content.id}`;

            const source   = document.getElementById("modal-template").innerHTML;
            const template = Handlebars.compile(source);
            const html = template(content);

            document.querySelector('.modal-body').innerHTML = html;
            $('.modal').modal('show')
        }
    }


    function init() {
        document.querySelectorAll('.js-orders').forEach(container => container.addEventListener('click', showOrder));

        document.querySelector('.js-addresses').addEventListener('click', removeAddress)

        document.querySelector('.address-form').addEventListener('submit', addAddress)

        document.querySelector('.js-reset_password').addEventListener('submit', resetPassword)

        document.querySelector('.js-delete_account').addEventListener('submit', deleteAccount)
    }

    function showOrder(evt) {
        if(evt.target.tagName != 'A' && evt.target.tagName != 'I') return;
        const id = evt.target.closest('[data-order]').dataset.order;

        fetch('/order/' + id)
            .then(rsp => rsp.json())
            .then(rsp => view.showModal(rsp))
    }

    function removeAddress(evt) {
        const id = evt.target.dataset.id;
        if(!id) return;
        const body = {
            type:'address',
            action:'remove',
            id,
        }

        const callback = () => evt.target.closest('li').remove();

        sendPost(JSON.stringify(body), callback);
    }

    function addAddress(evt) {
        evt.preventDefault();
        const body = {
            type:'address',
            action:'add',
        }
        const data = new FormData(evt.target)
        for([key, value] of data.entries()) {
            body[key] = value;
        }

        const callback = rsp => {
            const li = `<li class="list-group-item" >
                        ${body['address']} ${body['complement']}
                        <button type="button" class="float-right btn btn-sm btn-danger" data-id="${rsp['id']}" name="button">Remove</button>
                        </li>`

            document.querySelector('.js-addresses').insertAdjacentHTML('beforeend', li);

            document.querySelector('.no_saved').remove();
        }
        sendPost(JSON.stringify(body), callback)
    }

    function sendPost(body, callback) {
        const csrf = getCookie('csrftoken');
        fetch('', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrf,
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            credentials: 'same-origin',
            body: body
        }).then(rsp => rsp.json())
        .then(rsp => {
            if(rsp['success']) {
                callback(rsp);
            }
        });
    }

    function resetPassword(evt) {
        evt.preventDefault()
        const body = {
            type: 'change_password'
        }
        evt.target.querySelectorAll('input').forEach(input => {
            body[input.name] = input.value;
        })

        console.log(body);

        callback = () => {};

        sendPost(JSON.stringify(body), callback);
    }

    function deleteAccount(evt) {
        evt.preventDefault();
        const pass = this.querySelector('input').value;
        const body = {
            type: 'delete_account',
            pass: pass,
        }

        callback = () => window.location.replace('/');

        sendPost(JSON.stringify(body), callback);
        }

    init();
}
document.addEventListener('DOMContentLoaded', account)
