# Thailand Province Border-Adjacency Mappings

**Project:** This project creates a mapping dataset between adjacent provinces in Thailand. Dataset uses a data-relations `X -> Y, Z` convention, so we can easily integrate neighbouring provincial-level-data or visualise the relations as below using GraphViz:

![Adjacency map](Thailand_Province_Neighbours.png)

**Contents:** The repo contains **(1) a dataset of the province neighbours** of each province in Thailand (correct as of Feb 2nd 2021/2564) and **(2) code to parse and verify data relations for mutual consistency and naming consistency**. This code can easily be adapted or used directly on other datasets that already use 'PROV_NAME' as an identifier for naming conventions.

**Why make this?** This useful mapping dataset for Thailand's provinces is not publicly available elsewhere. Once I created it, it needed to be validated as consistent/correct.

**What is it useful for?:** In many geographical/GIS data analysis tasks correlating or combining datasets from different places is important to find patterns. In cases like risk analysis for COVID-19 disease infections or trends in agricultural practices, risk of wild-fires spreading, etc, a trend tends to transition across adjacent borders. 

From the ground-up, this mapping dataset lets data analysts immediately combine provincial-datasets to produce solutions to these kinds of questions.

**Who is this intended for?:** Mainly for Data Analysts working on regional GIS problems. Secondly, the code provides a base for Data Analysts to build and verify new "mappings" datasets.



## About the Mapping Dataset:

There are two formattings of the dataset: `thailand_data_relations.txt` and `thailand_data_relations_quoted.txt`. The latter provides each province name in double-quotes for convenience in some applications (like GraphViz).

In brief, the dataset is simply a set of relations, i.e. 

    x -> y, z

Which is read as *"`x` is related to `y` and `z`*" and one relation is given per line.

For Thailand, we have examples such as:

    Phuket -> Phangnga
    Narathiwat -> Yala, Pattani

The relations format let's us verify the ***mutual consistency*** of relations, so we can discover and correct inconsistencies by confirming that for `x -> y` there must also be a `y -> x`.

<p align="center">
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Thailand_provinces_en.svg/1050px-Thailand_provinces_en.svg.png" width="150">
</p>

Province Neighbours are determined using the [Provinces and Administrative Areas Map Image - Wikipedia](https://en.wikipedia.org/wiki/Provinces_of_Thailand) map image (above). The canonical source for resolving ambiguities is the Province's Wikipedia entry. As an example, [Phuket Province - Wikipedia](https://en.wikipedia.org/wiki/Phuket_Province) specifies that *"Phuket Island is connected [...] to Phang Nga Province"*, unambiguously determining `Phuket -> Phang Nga`.


By following a naming convention, we can confirm ***naming consistency*** too, ensuring all names exist in a source dataset (i.e. `x` exists in our naming convention dataset). For Thailand mappings, the naming convention dataset used is the spatial provincial dataset for Thailand from [phannisa_province_data_latlon.csv (utf-8)](https://github.com/pnphannisa/thailand_spatial_resources), which uses naming conventions canonically specified by Thai authorities. The same naming set can be found in [Province of Thailand - Wikipedia](https://en.wikipedia.org/wiki/Provinces_of_Thailand).


## Code Requirements:
Platform requirements:
```
Python 3.x
```
Library Dependencies:
```
pandas==0.23.0
unittest (built-in for Py3)
```

## How to Use Code Module
The code is also useful to get the mapping dataset parsed into a mapped dictionary format, to use programmatically in your own applications.

The dictionary format is `{<Province Obj> : [ <Province Obj>, <Province Obj>, ... ] }`. 

By default, a `Province` has an identifier as `p.PROV_NAME` and other data `p.data`, created via `Province(PROV_Name='name',optional_dictionary_of_data)`

For example:

```
# Import the module:
from province_neighbours import read_provincial_dataset, read_relations_dataset, Province, ProvinceRelationParser

# - Read in the datasets:
naming_convention_dataset = read_provincial_dataset( filename="../phannisa_province_data_latlon_v02_utf8.csv" )
mappings = read_relations_dataset('../thailand_province_relations.txt')

# - Parse the mappings into a dict format:
prp = ProvinceRelationParser(mappings, naming_convention_dataset)

# Print out any consistency errors and the full set of mappings.
print( prp )
prp._report_relation_errors()  # or `prp._relation_error` in list format 
prp._report_province_naming_errors() # or `prp._province_naming_errors`
```
At this point, we have parsed and verified the mappings. Next, use the dictionary in your application:
```
# Get the dictionary of mappings:
dictionary_of_mappings = prp.get_mappings_dict()
for k,v in dictionary_of_mappings.items():
    pass # as you like.

# Lookup Data for a Province by Name:
province = naming_convention_dataset['NARATHIWAT']
print(province)

# Lookup Neighbouring Provinces from the Dictionary:
print( dictionary_of_mappings[Province('NARATHIWAT')] )

neighbours = dictionary_of_mappings[Province('NARATHIWAT')]
print( len(neighbours) )
```

### How to Run Our Code:
```
git clone https://github.com/pmdscully/thailand_province_border_adjacency.git
python --version    # Verify Python version is => Py 3.x
pip install pandas==0.23.0
cd thailand_province_border_adjacency\test
python test_province_relation_parser.py
```
Once all tests pass, then:
```
cd ..\src
python province_neighbours.py
```

## Final words

All original contents in the repo are licensed under the MIT License, i.e. free use and modify without warranty.

For any questions or issues, feel free to get in contact. I'm always happy to know how our open source work gets used, so let me know if you find it useful.