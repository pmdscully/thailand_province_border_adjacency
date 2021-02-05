import pandas as pd

    
class Province(object):
    def __init__(self, PROV_NAME="", **kwargs):
        self.PROV_NAME = str(PROV_NAME)
        self.data = kwargs
    
    def __hash__(self):
        return hash(self.__repr__())
    def __eq__(self, o):
        return self.__repr__() == o.__repr__()
    def __str__(self):
        return self.__repr__()
    def __repr__(self):
        return f'{self.__class__.__name__}> {self.PROV_NAME}'

    @staticmethod
    def _invalid_instance():
        return Province(PROV_NAME="**INVALID**")


class ProvinceRelationParser:
    def __init__(self, relations_input_dataset:str=None, province_lookup:dict=None, ignore_parse_lines:list=[""]):
        self._province_lookup = province_lookup
        self.province_relations = {}
        self._province_naming_errors=[]
        self._relation_error = []
        
        self.__parse( relations_input_dataset, ignore_parse_lines )
        self.__has_valid_mutual_borders()

    def __parse(self, relations_input_dataset, ignore_parse_lines=[""]):
        # remove blank lines
        relations_input_dataset = [l for l in relations_input_dataset if l not in ignore_parse_lines]
        for s in relations_input_dataset:
            prov, neighbours = self._get_relation_from_text(s)
            self.province_relations[prov] = neighbours
        
    def _get_relation_from_text(self, s):
        arr = s.split("->")
        k = arr[0].strip().upper()
        k = self.__is_valid_name_lookup_or_else( k , source=k )
        v = [ self.__is_valid_name_lookup_or_else( v.strip().upper() , source=k ) for v in arr[1].split(",") ]
        return k , v

    def __is_valid_name_lookup_or_else(self, k, source):
        if k in self._province_lookup:
            ret = self._province_lookup[ k ]
        else:
            self._province_naming_errors+=[f"Missing Province Lookup: {source} -> {k}"]
            ret = Province._invalid_instance()
        return ret
    
    def __has_valid_mutual_borders(self):
        """
        True: curr_province has pv in curr_province's neighbour_provinces.
        Test: confirm curr_province is in pv's neighbour_provinces.
        """
        c=0
        for curr_province , neighbour_provinces in self.province_relations.items():
            c+=1
            # True: pv is in curr_province's neighbour_provinces.
            for pv in neighbour_provinces:
                # Test: Neighbour exists:
                if pv not in self.province_relations:
                    self._relation_error += [f"{c}. Missing Province Neighbour Entry for {curr_province.PROV_NAME} -> {pv.PROV_NAME}."]
                    continue
                pv_neighbours = self.province_relations[pv] # lookup to find another province's neighbours          
                # Test: curr_province is in pv's neighbour_provinces.
                if curr_province not in pv_neighbours: 
                    self._relation_error += [f"{c}. Missing Mutual Neighbour for {curr_province.PROV_NAME} -> {pv.PROV_NAME}."]
                    continue
                    
    def _report_relation_errors(self):        
        return "Province Relation Errors:\n"+("\n".join(self._relation_error)) if len(self._relation_error) > 0 else "Province Relation Errors: None Found"
    
    def _report_province_naming_errors(self):
        return "Province Name Errors:\n"+("\n".join(self._province_naming_errors)) if len(self._province_naming_errors) > 0 else "Province Name Errors: None Found"

    def __repr__(self):
        r = [self._report_relation_errors(), self._report_province_naming_errors(),"","Province Neighbour Relations:"]
        for p,neighbour in self.province_relations.items():
            r.append( f"{p.PROV_NAME}:\n" + "\n".join(["\t"+n.PROV_NAME for n in neighbour]) )
        return "\n".join(r)

    def get_mappings_dict(self):
        """ Return the dictionary of province mappings. 
            - Key is Province Object.
            - Value is List of Province Objects. 
            - Format is thus: { <Province> : [ <Province> , ... ] }
        """
        return self.province_relations





def read_relations_dataset(filename):
    lines = []
    with open(filename, 'r') as fd:
        lines = fd.read().split("\n")
    lines = [l for l in lines if l != ""]
    return lines

def read_provincial_dataset( **kwords ):
    #df = pd.read_csv( kwords['filename'], encoding=kwords['encoding'] )
    df = pd.read_csv( kwords['filename'] )
    d = dict([(kwargs['PROV_NAME'], Province(**kwargs)) for kwargs in df.to_dict(orient='records')])
    return d


if __name__ == "__main__":
    # provincial_lookup = read_provincial_dataset( filename="../province_data_latlon.csv", encoding="iso8859_11" )
    provincial_lookup = read_provincial_dataset( filename="../province_data_latlon.csv" )
    data = read_relations_dataset('../thailand_province_relations.txt')
    prp = ProvinceRelationParser(data, provincial_lookup)
    print( prp )
    dictionary_of_mappings = prp.get_mappings_dict()
    for k,v in dictionary_of_mappings.items():
        pass
    
    # Lookup Data for a Province:
    province = provincial_lookup['NARATHIWAT']
    print(province)

    # Lookup Neighbouring Provinces:
    print( dictionary_of_mappings[Province('NARATHIWAT')] )

    neighbours = dictionary_of_mappings[Province('NARATHIWAT')]
    print( len(neighbours) )