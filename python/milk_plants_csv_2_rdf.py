import pandas as pd

csv_path = '/Users/dorisavedikian/NALShapes_Internal/dairy-idea/DATA_&_Resources/milk-plants-08.csv'
df = pd.read_csv(csv_path)
df.columns = ['Year', 'TotalBeverageMilkConsumed', 'NumberOfPlants', 'AverageVolumePerPlant']
df = df[df['Year'].apply(lambda x: str(x).isnumeric())]

# Function to generate RDF Turtle format for the entire dataset
def generate_rdf_for_dataset(df):
    rdf = """
@prefix dct: <http://purl.org/dc/terms/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix qudt: <http://qudt.org/schema/qudt/> .
@prefix unit: <http://qudt.org/vocab/unit/> .
@prefix qb: <http://purl.org/linked-data/cube#> .
@prefix s: <https://lod.nal.usda.gov/nalt/shapes/> .
@prefix nalt: <https://lod.nal.usda.gov/nalt/> .
"""
    # Observation indices
    index_start = 3
    index_end = index_start + len(df) - 1

    for i, row in enumerate(df.iterrows()):
        year = row[1]['Year']
        total_milk_consumed = row[1]['TotalBeverageMilkConsumed'].replace(",", "")
        rdf += f"""
s:TotalMilkConsumedObservation_b{index_start + i}
    rdf:type qb:Observation ;
    dct:subject nalt:_Dairy ;
    nalt:_location "US" ;
    nalt:_year "{year}"^^xsd:gYear ;
    nalt:_totalMilkConsumed [
        qudt:value "{total_milk_consumed}"^^xsd:decimal ;
        qudt:conversionMultiplier "1000000"^^xsd:decimal ; 
        qudt:unit unit:LB
    ] .   

"""
    for i, row in enumerate(df.iterrows()):
        year = row[1]['Year']
        number_of_plants = int(row[1]['NumberOfPlants'])
        rdf += f"""
s:MilkPlantsObservation_c{index_start + i}
    rdf:type qb:Observation ;
    dct:subject nalt:_Dairy ;
    nalt:_location "US" ;
    nalt:_year "{year}"^^xsd:gYear ;
    nalt:_numberOfPlants "{number_of_plants}"^^xsd:integer ;
"""
    for i, row in enumerate(df.iterrows()):
        year = row[1]['Year']
        avg_volume_per_plant = row[1]['AverageVolumePerPlant']
        rdf += f"""
s:AverageVolumePerPlantObservation_d{index_start + i}
    rdf:type qb:Observation ;
    dct:subject nalt:_Dairy ;
    nalt:_location "US" ;
    nalt:_year "{year}"^^xsd:gYear ;
    nalt:_volumeProcessed [
        qudt:value "{avg_volume_per_plant}"^^xsd:decimal ;
        qudt:conversionMultiplier "1000000"^^xsd:decimal ; 
        qudt:unit unit:LB
    ] .
"""
    return rdf

rdf_data = generate_rdf_for_dataset(df)
rdf_output_path = '/Users/dorisavedikian/NALShapes_Internal/dairy-idea/validation_and_query_2/milk_plants_rdf.ttl'
with open(rdf_output_path, 'w') as f:
    f.write(rdf_data)
print(f"RDF data has been saved to {rdf_output_path}")