import pandas as pd
import re

def get_recs(text_input):
    text_input = str(text_input)
    text_input = re.sub('[-]]',' ',text_input)
    text_input = text_input.lower()
    qr = text_input.split()

    k = 0
    product_desc = []
    while k < len(qr):
        if k+1 < len(qr) and qr[k+1] == "free":
            k += 1
        elif qr[k] == "free":
            k += 1
        elif qr[k] == "no":
            k += 2
        else:
            product_desc.append(qr[k])
            k += 1

    allergen_tags = ["gluten free","treenut free","dairy free","soy free",
    "egg free","peanut free","sesame free","dairy free","wheat free"]

    k = 0
    in_tag1 = []
    in_tag2 = []
    in_count = 0
    while k < len(qr):
        if k+1 < len(qr) and qr[k+1] == "free":
            sub_list = f"{qr[k]} {qr[k+1]}"
            if sub_list in allergen_tags:
                k +=1
            elif sub_list not in allergen_tags and in_count ==0:
                in_tag1.append(qr[k])
                in_count += 1
                k +=1
            elif sub_list not in allergen_tags and in_count == 1:
                in_tag2.append(qr[k])
                k +=1
            else:
                k += 1
        elif qr[k] == "no":
            sub_list = f"{qr[k+1]} free"
            if sub_list in allergen_tags:
                k +=1
            elif sub_list not in allergen_tags and in_count ==0:
                in_tag1.append(qr[k+1])
                in_count += 1
                k +=1
            elif sub_list not in allergen_tags and in_count == 1:
                in_tag2.append(qr[k+1])
                k +=1
            else:
                k += 1
        else:
            k += 1

    k = 0
    aller_token1 = []
    aller_token2 = []
    aller_token3 = []
    r_count = 0
    while k < len(qr):
        if qr[k] == "free" and r_count == 0:
            if qr[k-1] in in_tag1 or qr[k-1] in in_tag2:
                k +=1
            else:
                aller_token1.append(f"{qr[k-1]} {qr[k]}")
                r_count += 1
                k +=1
        elif qr[k] == "free" and r_count == 1:
            if qr[k-1] in in_tag1 or qr[k-1] in in_tag2:
                k +=1
            else:
                aller_token2.append(f"{qr[k-1]} {qr[k]}")
                r_count += 1
                k +=1
        elif qr[k] == "free" and r_count == 2:
            if qr[k-1] in in_tag1 or qr[k-1] in in_tag2:
                k +=1
            else:
                aller_token3.append(f"{qr[k-1]} {qr[k]}")
                r_count += 1
                k +=1
        elif qr[k] == "no" and r_count == 0:
            if qr[k+1] in in_tag1 or qr[k+1] in in_tag2:
                k +=1
            else:
                aller_token1.append(f"{qr[k+1]} free")
                r_count += 1
                k +=1
        elif qr[k] == "no" and r_count == 1:
            if qr[k+1] in in_tag1 or qr[k+1] in in_tag2:
                k +=1
            else:
                aller_token2.append(f"{qr[k+1]} free")
                r_count += 1
                k +=1
        elif qr[k] == "no" and r_count == 2:
            if qr[k+1] in in_tag1 or qr[k+1] in in_tag2:
                k +=1
            else:
                aller_token3.append(f"{qr[k+1]} free")
                r_count += 1
                k +=1
        else:
            k +=1

    print(in_tag1)
    print(in_tag2)
    print(aller_token1)
    print(aller_token2)
    print(aller_token3)
    print(product_desc)

    df = pd.read_csv('results_id_name_tag_ingredients.csv',
     delimiter=',',converters={i: str for i in range(0, 100)})
    df['tags'] = df['tags'].transform(lambda x: str(re.sub("-\"","", x)))
    products = df.values.tolist()
    
    rec_list = []

    i=0
    while i < len(products):
        clean_product = products[i][1]
        products[i][1] = list(products[i][1].lower().split(' '))
        products[i][2] = re.sub('[/]',' ', products[i][2])
        products[i][2] = re.sub('"Gluten Free Coeliac Celiac"','gluten free,coeliac,celiac', products[i][2])
        products[i][2] = re.sub('[^A-Za-z, ]','', products[i][2]).lower().split(',')
        ingredients = re.sub('[^A-Za-z, ]','', products[i][3]).lower().split(',')
        
        ingredient_list = []
        for ing in ingredients:
            sub = ing.split(' ')
            for ele in sub:
                ingredient_list.append(ele)

        if len(in_tag1) > 0:
            for ele in in_tag1:
                check5 = ele not in ingredient_list
        else:
            check5 = True
        
        if len(in_tag2) > 0:
            for ele in in_tag2:
                check6 = ele not in ingredient_list
        else:
            check6 = True
            

        if len(product_desc) > 0:
            check1 = all(item in products[i][1] for item in product_desc)
        else:
            check1 = True
        if len(aller_token1) > 0:
            check2 = all(item in products[i][2] for item in aller_token1)
        else:
            check2 = True

        if len(aller_token2) > 0:
            check3 = all(item in products[i][2] for item in aller_token2)
        else:
            check3 = True

        if len(aller_token3) > 0:
            check4 = all(item in products[i][2] for item in aller_token3)
        else:
            check4 = True

        if check1 and check2 and check3 and check4 and check5 and check6:
            rec_list.append(clean_product)

        i += 1
    return(rec_list)
