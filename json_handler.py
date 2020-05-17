import json

def add_entry(data, country_name):
    #create new entry if the country isnt in the database yet
    if country_name not in data: data[country_name] = {}
    return data

def add_categoryentry(data, country_name, category_entry, category):
    #add the category if the category doesnt exist in the entry
    if category not in data[country_name]:
        data[country_name][category] = category_entry
    else:
        #if the category exists, but there is no list, create a list
        if type(data[country_name][category]) != list:
            data[country_name][category] = [data[country_name][category]]
        #add the category entry to the existing list
        data[country_name][category].append(category_entry)
    return data


#opening and loading to json the main data file
file = open('countries.json')
file_content = file.read()
data = json.loads(file_content)

if(input('Enter "y" to delete a category.\n') == 'y'):

    category = input('Enter category\n')
    for country in data:
        del data[country][category]

#check if a own category with default value is to be created
elif(input('Enter "y" for own category and values.\n') == 'y'):
    
    #enter the category name and the default value
    category = input('Enter category.\n')
    value = input('Enter value. Enter "list" for a list.\n')
    if(value == 'list'):
        value = []
    
    #add the category to the dataset
    for country in data:
        data[country][category] = value

else:

    #entering, opening and loading to json the file to pull new data from
    file = open(input('Enter file\n'))
    file_content = file.read()
    new_data = json.loads(file_content)

    #choose if the file to be extracted a geo.json
    if(input('Enter "y" for geo.json\n') == 'y'):
        
        #do the following for each country in the new data set
        for country in new_data['features']:
            country_name = country['properties']['name']
            data = add_entry(data, country_name)

            categories = ['id', 'geometry']
            for category in categories:
                data = add_categoryentry(data, country_name, country[category], category)
    else:

        #entering the new category to be added to main file entries
        category = input('Enter category\n')

        #do the following for each country in the new data set
        for country in new_data:
            country_name = country['country']
            #add entry
            data = add_entry(data, country_name)
            #update the country name of the entry
            data[country_name]['name'] = country_name
            #add the categoryentry
            data = add_categoryentry(data, country_name, country[category], category)

#write the updated json to the main file
file_content = json.dumps(data, indent=2)
file = open('countries.json', 'w')
file.write(file_content)