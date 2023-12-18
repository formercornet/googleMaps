import folium
import googlemaps
import os



GOOGLE_MAPS_API_KEY = ''
gmaps = googlemaps.Client(key='') #removed key for security purposes

desktop_directory = os.path.join(os.path.expanduser('~'), 'Desktop')
html_file_path = os.path.join(desktop_directory, 'delivery_routes_map.html')

def geocode_address(address):
    try:
        # Geocode the address
        geocode_result = gmaps.geocode(address)

        # Extract latitude and longitude
        location = geocode_result[0]['geometry']['location']
        return location['lat'], location['lng']
    except Exception as e:
        print("Error geocoding address: {0}".format(e))
        return None




def plot_delivery_routes(warehouse_coordinates, delivery_coordinates):
    # Create a map centered around the warehouse
    m = folium.Map(location=warehouse_coordinates, zoom_start=12)

    # Plot warehouse marker
    folium.Marker(location=warehouse_coordinates, popup='Warehouse', icon=folium.Icon(color='green', icon='home', prefix='fa')).add_to(m)
    folium.Marker(location=delivery_coordinates, popup='Delivery Point', icon=folium.Icon(color='red', icon='truck', prefix='fa')).add_to(m)
    # Plot delivery route
    #folium.PolyLine(locations=[warehouse_coordinates, delivery_coordinates, warehouse_coordinates], color='blue', weight=2.5, opacity=1).add_to(m)
                  
    # Request directions from the Google Maps Directions API
    directions = gmaps.directions(
        origin=warehouse_coordinates,
        destination=delivery_coordinates,
        mode="driving"
    )

    # Check if directions were successfully retrieved and contain legs information
    if directions and 'legs' in directions[0]:
        # Extract the polyline information from the first leg of the journey
        polyline = directions[0]['legs'][0]['steps']
        
        # Iterate over each step in the polyline
        for step in polyline:
            # Extract the encoded polyline points
            points = step['polyline']['points']

            # Decode the polyline points to obtain a list of coordinates
            locations = googlemaps.convert.decode_polyline(points)

            # Convert list of dictionaries to a list of tuples
            locations = [(location['lat'], location['lng']) for location in locations]

            # Print the locations for debugging
            print(locations)

            # Add a PolyLine to the Folium map using the decoded coordinates
            folium.PolyLine(locations=locations, color='blue', weight=2.5, opacity=1).add_to(m)

    # Save the map

    # Save the map
    m.save(html_file_path)
    print(f"Map saved to: {html_file_path}")




warehouse_address = "Tower 2 Boulevard Plaza Sheikh Mohammed Bin Rashid Blvd, Dubai, Dubai, United Arab Emirates"
warehouse_coordinates = geocode_address(warehouse_address)

delivery_address = "OYO 1028 Home 1 BHK Jumeirah Apartment 1, NA - 16C St - Al Satwa - Dubai - United Arab Emirates"
delivery_coordinates = geocode_address(delivery_address)

plot_delivery_routes(warehouse_coordinates, delivery_coordinates)
