
from regulations.models import Category


def get_values_from_paragraph_name(paragraph_name):
    """
    returns category_id, sub_category identifier, regime_number and regime name based on the paragraph name string,
    e.g. "0A005" will return id field corresponding category 0, "A", 5, and "Wassenaar Arrangement"
    """
    category = paragraph_name[0:1]
    subcategory = paragraph_name[1:2]
    regime_number = int(paragraph_name[2:])
    regime_name = "Wassenaar Arrangement"
    if regime_number // 100 == 1:
        regime_name = "Missile Technology Control Regime"
    elif regime_number // 100 == 2:
        regime_name = "Nuclear Suppliers Group"
    elif regime_number // 100 == 3:
        regime_name = "Australia Group"
    elif regime_number // 100 == 4:
        regime_name = "Chemical Weapons Convention"    
            
    # find out which part of category 5 the regulations belongs tp
    if category == "5" and subcategory + str(regime_number) in ["A2", "A3", "A4", "B2", "D2", "E2"]:
        category_id = category = Category.objects.filter(identifier=int(category), part = 2).first()
    elif category == "5":
        category_id = category = Category.objects.filter(identifier=int(category), part = 1).first()
    else: 
    # for other categories the identifier is unique
        category_id = category = Category.objects.filter(identifier=int(category)).first()
        
    return category_id, subcategory, regime_number, regime_name