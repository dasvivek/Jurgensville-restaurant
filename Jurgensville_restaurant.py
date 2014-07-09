
#Jurgensville restaurant code
#Developed by Vivek Das
#09072014 - version 1

import sys
import csv as csv
import itertools

def read_csv(filename):
    try:
        dataset = csv.reader(open(filename),delimiter=",",escapechar=" ")
        data_list = []
        data_dict={}
        for row in dataset:
            if data_dict.has_key(row[0]):
                data_dict[row[0]].append(tuple(row[1:]))
            else:
				data_dict[row[0]] = []
				data_dict[row[0]].append(tuple(row[1:]))
        dataset_dict = dict([(key,sorted(menu,key=lambda x:x[0])) for key,menu in data_dict.items()])
        return dataset_dict
    except IOError as e:
        print e
        return {}

def get_list_combo(dataset,menulist):
    combo_dict ={}
    min_value=(-1,10000000000)
    menu_combinations=[x for x in itertools.permutations(menulist,len(menulist))]
    for key,value in dataset.items():
        filtered_combinations = [y for y in itertools.ifilter(lambda x:set(menulist).issubset(set(x[1:])),value)]
        if len(filtered_combinations) > 0:
            if float(filtered_combinations[0][0]) < min_value[1]:
                min_value = (key,float(filtered_combinations[0][0]))
            combo_dict[key] = filtered_combinations[0]
    if min_value[0] != -1:
        return min_value

def get_distributed_combo(dataset,menulist):
    distributed_dict ={}
    menu_availability= -1
    for key,value in dataset.items():
        distributed_combinations = [y for y in itertools.ifilter(lambda x: set(menulist).intersection(set(x[1:])),value)]
        if len(distributed_combinations) > 0:
            excepted_combinations = [y for y in itertools.ifilter(lambda x: set(menulist).difference(set(x[1:])),distributed_combinations)]
            if len(excepted_combinations) > 0:
                union_set = [i[1:] for i in itertools.chain(distributed_combinations,excepted_combinations)]
                if set().union(*union_set).intersection(menulist) == set(menulist):
                    if key in distributed_dict:
                        distributed_dict[key].append(sum([float(pair[0]) for pair in distributed_combinations]))
                    else:
                        distributed_dict[key]=[]
                        distributed_dict[key].append(sum([float(pair[0]) for pair in distributed_combinations]))
        else:
            menu_availability = None
    if menu_availability == -1:
        return None
    else:
        if len(distributed_dict) > 0:
            Restaurant_with_less_price = min(distributed_dict, key=distributed_dict.get),
            return (Restaurant_with_less_price[0],distributed_dict[Restaurant_with_less_price[0]][0])
        
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "format <filename> <MenuItem1> <MenuItem2> ..."
    else:
        menulist = list(set(sys.argv[2:])) #removing duplicate entries from input
        dataset = read_csv(sys.argv[1])
        if len(menulist) > 3:
            print "Max Length of unique inputs exceeded 3"
        else:
            menu_combo = get_list_combo(dataset,menulist)
            menu_distributed_availability = get_distributed_combo(dataset,menulist)
            if menu_combo == None and menu_distributed_availability == None:
                print "Concerned Menu Not Available"
            elif menu_combo == None and menu_distributed_availability != None:
                print menu_distributed_availability[0],menu_distributed_availability[1]
            elif menu_distributed_availability == None and menu_combo != None:
                print menu_combo[0],menu_combo[1]
            else:
                if menu_combo[1] <= menu_distributed_availability[1]:
                    print menu_combo[0],menu_combo[1]
                else:
                    print menu_distributed_availability[0],menu_distributed_availability[1]
