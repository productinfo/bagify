function collection() {
    let data = {
        items: django_data,
        constraints: {
            categories: [],
            gender: [],
            query: '',
        },
        sortBy: '',
    };

    let view = {
        categories: document.getElementsByName('selected-categories'),
        genders: document.getElementsByName('gender'),
        search: document.getElementById('search'),
        catalog: document.getElementById('catalog'),

        loadCatalog(items) {
            this.catalog.innerHTML = '';

            let source = document.getElementById('catalog-template').innerHTML;
            let template = Handlebars.compile(source);
            let html = template({'items': items});

            this.catalog.innerHTML = html;
        },
    };

    function init() {
        gatherConstraints();

        [...view.categories, ...view.genders].forEach(element => element.onchange = updateCatalog );
        view.search.addEventListener('input', updateCatalog)
    }

    function gatherConstraints() {
        data.constraints.categories = [];
        view.categories.forEach(category => {
            if(category.checked) data.constraints.categories.push(category.value);
        })

        data.constraints.gender = [];
        view.genders.forEach(gender => {
            if(gender.checked) data.constraints.gender.push(gender.value);
        })

        data.constraints.query = view.search.value;
    }

    function filterItems() {
        let filtered = data.items;

        if(data.constraints.categories.length > 0) {
            filtered = filtered.filter(item => {
                return data.constraints.categories.includes(String(item.category_id))
            })
        }

        if(data.constraints.gender.length > 0) {
            filtered = filtered.filter(item => {
                if(item.gender == 'U') return 1;
                return data.constraints.gender.includes(item.gender);
            })
        }

        if(data.constraints.query) {
            let query = data.constraints.query.split(' ');
            for(let word of query){
                if(!word) continue;
                filtered = filtered.filter(item => {
                    return item.name.toLowerCase().includes(word.toLowerCase());
                })
            }
        }

        return filtered
    }

    function sortedItems(items) {
        let sorted = items.sort((it1, it2) => {
            console.log(it1, it2, 'first sort');
            return 1
        })
    }

    function updateCatalog(evt) {
        gatherConstraints();

        let filtered_items = filterItems();

        view.loadCatalog(filtered_items);
    }

    init();
}
document.addEventListener('DOMContentLoaded', collection)
