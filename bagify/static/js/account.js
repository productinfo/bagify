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
        },

        sendToaster(options) {
            const toaster = document.querySelector('.toasty');
            document.querySelector('.toasty .title').innerHTML = options.title;
            document.querySelector('.toasty .body').innerHTML = options.body;
            toaster.querySelector('div').classList.add(options.color);

            toaster.hidden = false;
            setTimeout(() => toaster.hidden=true, 2000);
        },
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

        const callback = rsp => {
            if(rsp['success']) evt.target.closest('li').remove();
        }

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
            if(rsp['success']) {
                const li = `<li class="list-group-item" >
                            ${body['address']} ${body['complement']}
                            <button type="button" class="float-right btn btn-sm btn-danger" data-id="${rsp['id']}" name="button">Remove</button>
                            </li>`

                document.querySelector('.js-addresses').insertAdjacentHTML('beforeend', li);

                document.querySelector('.no_saved').remove();
            }

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
        .then(rsp => callback(rsp));
    }

    function resetPassword(evt) {
        evt.preventDefault()
        const body = {
            type: 'change_password'
        }

        evt.target.querySelectorAll('input').forEach(input => {
            body[input.name] = input.value;
            input.value = '';
        })

        if(body.new_pas !== body.confirm_pas) {
            view.sendToaster({color:'danger', body:'Passwords do not match.', title:'Operation Failed'})
            return;
        }

        callback = rsp => {
            if(rsp['success']){
                view.sendToaster({color:'success', title:'Success', body:'Password changed.'})
            } else {
                view.sendToaster({title:'Operation Failed', body:'Wrong password', color:'danger'})
            }

        };

        sendPost(JSON.stringify(body), callback);
    }

    function deleteAccount(evt) {
        evt.preventDefault();
        const pass = this.querySelector('input').value;
        const body = {
            type: 'delete_account',
            pass: pass,
        }

        callback = rsp => {
            if(rsp['success']) {
                window.location.replace('/')
            } else {
                view.sendToaster({color:'danger', title:'Operation Failed.', body:'Wrong password.'})
            }
        };

        sendPost(JSON.stringify(body), callback);
        }

    init();
}
document.addEventListener('DOMContentLoaded', account)
