function collection() {
    const data = {
        items: items_data,
        constraints: {
            categories: [],
            gender: [],
            query: '',
        },
        sortBy: '',
    };

    const view = {
        categories: document.getElementsByName('selected-categories'),
        genders: document.getElementsByName('gender'),
        search: document.getElementById('search'),
        items: document.querySelectorAll('[data-id]'),
    };

    function init() {
        updateCatalog();

        // sets listeners for every input field to update the catalog
        [...view.categories, ...view.genders].forEach(element => element.onchange = updateCatalog );
        view.search.addEventListener('input', updateCatalog);
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

    function filterItemsIds() {
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

        const ids = filtered.map(item => item.id)
        return ids;
    }

    function sortedItems(items) {
        let sorted = items.sort((it1, it2) => {
            console.log(it1, it2, 'first sort');
            return 1
        })
    }

    function updateCatalog(evt) {

        // updates the constraints of the items
        gatherConstraints();

        // gets a list of id's of every item that fits the constraints
        let filtered_items_ids = filterItemsIds();

        // hides the elements not on the list
        for(card of view.items) {
            card.hidden = (filtered_items_ids.includes(+card.dataset.id)) ? false : true;
        }

    }

    init();
}
document.addEventListener('DOMContentLoaded', collection)
