import csv

class Melon:

    def __init__(
        self,
        melon_id,
        common_name,
        price,
        image_url,
        color,
        seedless,
                    ):
        self.melon_id = melon_id
        self.common_name = common_name
        self.price = price
        self.image_url = image_url
        self.color = color
        self.seedless = seedless

    def __repr__(self):
        """Convenience method to show information about melon in console."""

        return (
            f"<Melon: {self.melon_id}, {self.common_name}>"
        )
    
    def price_str(self):
        """Return price formatted as string $x.xx"""

        return f"${self.price:.2f}"
    
# def find_melon(melons, melon_id):
#     for melon in melons:
#         if 
    
def get_by_id(melon_id):
    """Return a melon, given its ID."""

    return melon_dict[melon_id]

def all_melons():
    """Return list of melons."""
    all = []
    for melon in melon_dict:
        all.append(melon_dict[melon])
    return all

    """Alternate method"""

    """return list(melon_dict.values())"""

# with open("melons.csv") as csvfile:
#     rows = csv.DictReader(csvfile)
#     for row in rows:
#         print(row)

melon_dict = {}

with open("melons.csv") as csvfile:
    rows = csv.DictReader(csvfile)

    for row in rows:
        melon_id = row['melon_id']
        melon = Melon(
            melon_id,
            row['common_name'],
            float(row['price']),
            row['image_url'],
            row['color'],
            eval(row['seedless']))

        melon_dict[melon_id] = melon

# print(get_by_id('cren').color)
# print(all_melons())
        
"""pip install -r requirements.txt python3 to install all dependencies listed in the written txt file"""