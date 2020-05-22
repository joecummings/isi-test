"""
Module to create new dataset of Wikipedia article IDs based on a Wikipedia category.
These IDs should then by matched to a JSON dump of Wikipedia articles using the 
script `format_wikipedia.py`.

Makes use of the Wikipedia-Python API: https://wikipedia-api.readthedocs.io/en/latest/API.html
"""
import argparse
from pathlib import Path
from typing import List, Mapping, Any

import wikipediaapi


def get_category_members(category_members: Mapping[str, Any], max_level: int) -> List[str]:
    """
    Recursively gets all page IDs associated with a category to a max depth

    Args:
        category_members: all Wikipedia articles and subcategories associated with the input category
        max_level: the max depth to recurse looking for Wikipedia articles
    
    Returns:
        List of Wikipedia article IDs
    """

    print(category_members)

    def get_category_members_sub(category_members, level, max_level, ids):
        
        if level == max_level:
            return ids

        for c in category_members.values():
            if c.ns == wikipediaapi.Namespace.CATEGORY and level < max_level:
                get_category_members_sub(c.categorymembers, level=level+1, max_level=max_level, ids=ids)
            else:
                print(f"{'*' * (level + 1)}: {c.title}")
                ids.append(str(c.pageid))
       
        return ids

    return get_category_members_sub(category_members, level=0, max_level=max_level, ids=[])

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--category", type=str, help="Wikipedia category from which articles will be pulled, without the preceding 'Category:' tag")
    p.add_argument("--max-level", type=int, help="Max level of articles to include from category page.", default=3)
    p.add_argument("--output", type=Path, help="Name of output file.")

    args = p.parse_args()

    wiki = wikipediaapi.Wikipedia("en")

    starting_page = wiki.page(f"Category:{args.category}")
    if not starting_page.exists():
        raise ValueError("Not a valid Wikipedia category")
    ids = get_category_members(starting_page.categorymembers, max_level=args.max_level)
    with open(args.output, "w+") as _file:
        for _id in ids:
            _file.write(f"{_id}\n")

if __name__ == "__main__":
    main()
