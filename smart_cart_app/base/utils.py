import random

def gerenrate_url(id):
    final_slug = ''
    for _ in range(20):
        final_slug += random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    return f'http://localhost:8000/{id}/{final_slug}'

def get_invoice(adding_items : dict, removing_items : dict) -> dict:
    add_dict, remove_dict = {}, {}
    for _, item_dict in adding_items.items():
        add_dict[item_dict['product']] = item_dict['uid']
    for _, item_dict in removing_items.items():
        remove_dict[item_dict['product']] = item_dict['uid']
    final_structure = {}
    for name, uid in add_dict.items():
        final_structure[name] = final_structure.get(name, 0) + 1
    for name, uid in remove_dict.items():
        try:
            final_structure[name] = final_structure.get(name) - 1
        except:
            pass
    return final_structure