from pyrosm import OSM

# Ruta al archivo PBF descargado
pbf_file_path = "C:/repos/SimIA/cuba-map/cuba-latest.osm.pbf"

# # Inicializar el objeto OSM
# osm = OSM(pbf_file_path)

# Define el área de interés (bounding box) para La Habana
bbox = [23.1139, 82.3534, 23.1339, 82.3934] # Coordenadas aproximadas

# Inicializa el objeto OSM
osm = OSM(pbf_file_path, bbox)

# Lee las redes de carreteras
# Read all drivable roads
drive_net = osm.get_network(network_type="driving")