from models import Categories, ItemsCategories


def get(categories_id, session=None, **kwargs):
    data = {
        'items_cnt': '',
        'instock_cnt': '',
        'name': '',
        'description': '',
        'extras': ''
    }
    categories = Categories.get_categories_by_id(session, categories_id).first()

    data['name'] = categories.name
    data['description'] = categories.description

    items_categories = ItemsCategories.get_items_categories_by_category_id(session, categories_id).all()

    data['items_cnt'] = items_categories.__len__()

    items = Categories.get_item_by_category_id(session, categories_id)



    print categories

