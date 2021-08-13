import json
with open('testj.json') as data_file:
    data = json.load(data_file)
    # update the data dictionary then re-dump it in the file
    data.update({
        "colonists_regions": ["66666", "77777"],
        "nation_regions": [],
        "brigands_regions": [],
        "treasury_regions": [],
        "events_regions": []
    })

with open('testj.json', 'w') as data_file:
    json.dump(data, data_file, indent=2)