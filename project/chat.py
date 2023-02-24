import pandas as pd

df = pd.read_csv('hotaling_cocktails-Cocktails.csv')

def cocktail_bot():
    user_input = input("What drink would you like to use as an ingredient in a cocktail? ")
    results = df[df['Ingredients'].str.contains(user_input, case=False)]
    if len(results) > 0:
        print("Here are some cocktail recipes that contain " + user_input + " as an ingredient:")
        for index, row in results.iterrows():
            print("Cocktail Name: " + row['Cocktail Name'])
            print("Ingredients: " + row['Ingredients'])
            print("\n")
    else:
        print("Sorry, I couldn't find any cocktail recipes containing " + user_input + " as an ingredient. Please try again.")
        
cocktail_bot()