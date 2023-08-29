import random

def gerenrate_url(id):
    final_slug = ''
    for _ in range(20):
        final_slug += random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    return f'http://localhost:8000/{id}/{final_slug}'

def get_invoice(adding_items : dict, removing_items : dict) -> dict:
    add_dict, remove_dict = {}, {}
    for entry in adding_items.values():
        product = entry['product']
        if product in add_dict:
            add_dict[product] += 1
        else:
            add_dict[product] = 1
    print(add_dict)
    if removing_items:
        for entry in removing_items.values():
            product = entry['product']
            print(product)
            if product in remove_dict:
                remove_dict[product] += 1
            else:
                remove_dict[product] = 1
        print(remove_dict)
    
    final_structure = {}

    for itemName, itemCount in add_dict.items():
        removeCount = remove_dict.get(itemName, 0)
        final_structure[itemName] = 0 if (itemCount-removeCount) < 0 else (itemCount-removeCount)
        

    print(final_structure)
    return final_structure