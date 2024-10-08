import pandas as pd
from decimal import Decimal, InvalidOperation

def to_decimal(value):
    try:
        value = value.replace(",", "") if isinstance(value, str) else value
        return round(Decimal(value), 2)
    except (InvalidOperation, TypeError):
        return None

file_path = '/Users/dorisavedikian/NALShapes_Internal/dairy-idea/DATA_&_Resources/annualmilkprodfactors.csv'
df = pd.read_csv(file_path, skiprows=31, skipfooter=8, engine='python')
#df.drop(df.columns[[2, 3, 4, 6, 10, 11, 12, 13, 14]], axis=1, inplace=True)
df.drop(df.columns[[1, 2, 3, 5, 9, 10, 11, 12, 13]], axis=1, inplace=True)
df.columns = ['Year', 'DairyCowCount', 'TotalMilkProduction', 'AverageAllMilkPrice', 'DairyRationCost']
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
@prefix nalt:_ <https://lod.nal.usda.gov/nalt/> .
"""
    index_start = 33

    for i, row in enumerate(df.iterrows()):
        year = row[1]['Year']
        dairy_cow_count_value = to_decimal(row[1]['DairyCowCount'])
        rdf += f"""
s:DairyCowCountObservation_b{index_start + i}
    rdf:type qb:Observation ;
    dct:subject nalt:_Dairy ;
    nalt:_location "US" ;
    nalt:_year "{year}"^^xsd:gYear ;
    nalt:_dairyCowCount [
        qudt:value "{dairy_cow_count_value}"^^xsd:decimal ;
        qudt:conversionMultiplier "1000"^^xsd:decimal
    ] .
"""
    for i, row in enumerate(df.iterrows()):
        year = row[1]['Year']
        total_milk_prod_value = to_decimal(row[1]['TotalMilkProduction'])
        rdf += f"""
s:TotalMilkProductionObservation_d{index_start + i}
    rdf:type qb:Observation ;
    dct:subject nalt:_Dairy ;
    nalt:_location "US" ;
    nalt:_year "{year}"^^xsd:gYear ;
    nalt:_totalMilkProduction [
        qudt:value "{total_milk_prod_value}"^^xsd:decimal ;
        qudt:conversionMultiplier "1000000"^^xsd:decimal ;
        qudt:unit unit:LB
    ] .
"""
    for i, row in enumerate(df.iterrows()):
        year = row[1]['Year']
        avg_milk_price = to_decimal(row[1]['AverageAllMilkPrice'])
        rdf += f"""
s:AverageAllMilkPriceObservation_e{index_start + i}
    rdf:type qb:Observation ;
    dct:subject nalt:_Dairy ;
    nalt:_location "US" ;
    nalt:_year "{year}"^^xsd:gYear ;
    nalt:_averageAllMilkPrice [
        qudt:value "{avg_milk_price}"^^xsd:decimal ;
        qudt:unit v:dollarsPerCWT
    ] .
"""
    for i, row in enumerate(df.iterrows()):
        year = row[1]['Year']
        dairy_ration_cost = to_decimal(row[1]['DairyRationCost'])
        rdf += f"""
s:DairyRationCostObservation_f{index_start + i}
    rdf:type qb:Observation ;
    dct:subject nalt:_Dairy ;
    nalt:_location "US" ;
    nalt:_year "{year}"^^xsd:gYear ;
    nalt:_dairyRationCost [
        qudt:value "{dairy_ration_cost}"^^xsd:decimal ;
        qudt:unit v:dollarsPerCWT
    ] .
"""
    return rdf 

rdf_data = generate_rdf_for_dataset(df)
rdf_output_path = '/Users/dorisavedikian/NALShapes_Internal/dairy-idea/validation_and_query_2/milk_supply_factors_rdf.ttl'
with open(rdf_output_path, 'w') as f:
    f.write(rdf_data)
print(f"RDF data has been saved to {rdf_output_path}")
