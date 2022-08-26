from pandas import read_csv

# products = read_csv('./resources/products.csv', delimiter=';')
product_cats = read_csv("./resources/product_categories.csv", delimiter=";")
product_cats = product_cats[['category_id', 'product_id']]
# product_cats['product_id'] = product_cats['product_id'].apply(lambda x:products.iloc[x-1]['id'])
product_cats.to_csv("./resources/product_categories.csv", sep=";", index=False)