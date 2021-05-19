import yaml
import os
import re
import glob
from jinja2 import Environment, FileSystemLoader

def _short_desc(style):
    if re.match('(?i)^[a,e,i,o,u]', style):
        return f"_Style_: An _{style}_ Cocktail."
    return f"_Style_: A {style} Cocktail."

def _generate_ingredients(ingredients):
    return_val = []
    for ingredient in ingredients:
        return_val.append({"name": ingredient, "pour": ingredients[ingredient]})
    return return_val

def load_cocktails(path):
    cocktail_yamls = glob.iglob(f'{path}/**/*.yaml', recursive=True)
    cocktails = []
    for cocktail in cocktail_yamls:
        with open(cocktail, 'r') as f:
            try:
                cocktail_dict = yaml.safe_load(f)
                cocktail_dict['cocktail_desc_short'] = _short_desc(cocktail_dict['Style'])
                cocktail_dict['Ingredients'] =_generate_ingredients(cocktail_dict['Ingredients'])
                cocktails.append(cocktail_dict)
            except yaml.YAMLError as exc:
                print(exc)
                raise("Unable to load cocktail.")
    return cocktails

def main():

    j2_env = Environment(loader=FileSystemLoader('.'), trim_blocks=True)
    template = j2_env.get_template('script/cocktail.jinja2')
    if not os.path.exists('./pages'):
        os.makedirs('./pages')
    if not os.path.exists('./pages/cocktails'):
        os.makedirs('./pages/cocktails')
    for cocktail in load_cocktails("./cocktails"):
        out = template.render(cocktail)
        with open(f"./pages/cocktails/{cocktail['Name']}.md", "w") as f:
            f.write(out)

if __name__ == "__main__":
    main()
