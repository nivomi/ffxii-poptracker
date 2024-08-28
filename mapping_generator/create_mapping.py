import json
# ff12 AP datapackage
with open("./mapping_generator/ff12_datapackage.json") as dp_file:
    datapackage = json.load(dp_file)
# list of key items (i.e. items the tracker cares about)
with open("./mapping_generator/key_items.json") as key_map_file:
    key_items: list[str] = json.load(key_map_file)
# tracker's items.json
with open("./items/items.json") as item_data_file:
    item_data: list[dict] = json.load(item_data_file)
# 'override' file - for items whose tracker name and AP name don't match
with open("./mapping_generator/item_overrides.json") as override_file:
    item_overrides: dict[str,str] = json.load(override_file)

# get tracker code and type (consumable, toggle) for a given AP item name
def get_codetype_from_name(name: str) -> tuple[str, str]:
    override = item_overrides.get(name)
    # if there's an override, use it
    truename = override if override is not None else name
    # find poptracker code from display name
    item_def = next((x for x in item_data if x['name'] == truename), {})
    item_code = item_def.get('codes')
    item_type = item_def.get('type')
    if item_code is not None:
        return item_code, item_type
    print(f"""DATA PROBLEM: No matching code for "{name}" in items/items.json :( """)
    if override is not None:
        print(f"""\tname overridden to {override} by mapping_generator/item_overrides.json""")
    return "BAD_DATA", "BAD_DATA"

with open("./scripts/archipelago/item_mapping.lua", 'w') as out_file:

    out_file.write("return {\n")

    for item in key_items:
        item_code, item_type = get_codetype_from_name(item)
        item_id = datapackage['item_name_to_id'][item]
        out_file.write(f"""\t[{item_id}] = {{"{item_code}", "{item_type}"}},\n""")

    out_file.write("}")