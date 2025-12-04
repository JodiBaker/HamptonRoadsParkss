import requests
#import psycopg2
from flask import Flask, render_template, request



app = Flask(__name__)


#API endpoint URL for fetching park data
API_LIST = {
     "newport news": "https://maps.nnva.gov/gis/rest/services/Operational/Park/MapServer/0/query?outFields=*&where=1%3D1&f=geojson",
     "hampton": "https://services3.arcgis.com/IFfZzsUkSirJaEqg/arcgis/rest/services/Hampton_Roads_Parks/FeatureServer/0/query?where=COUNTY%20%3D%20'HAMPTON'&outFields=*&outSR=4326&f=json"
}
     
@app.route("/", methods=['GET'])
def home():
    return render_template("index.html", result=None)




@app.route('/results', methods=['GET','POST'])
def show_parks():

     parks = []
     search_word = ''
     


     if request.method == 'POST':
          search_word = request.form.get('search_word', '').lower()
          api_url = API_LIST.get(search_word)
          print(api_url)

          if api_url:
               response = requests.get(api_url)

               #Check if the request was successful
               if response.status_code == 200:
                    data = response.json()
                    features = data.get("features", [])
                    
                    
                    #loop through features to extract location names
                    for feature in features:
                         location = feature.get("properties",{}) #hampton
                         locality = feature.get("attributes", {}) #     
                         parks.append({
                         'location': location.get("LOCATIONNAME") or locality.get("PARK_NAME"),
                         'dogpark': location.get("DOGPARK") or locality.get("DOG_PARK"),
                         'beach': location.get("BEACH") or locality.get("SWIMMING_AREA"),

                         })
                    print(parks)
          
                    print("Data fetched successfully")
               else:
                    print(f"Failed to fetch data: {response.status_code}")

          filter_column = request.form.get('filter_column')

          if filter_column not in ['dogpark', 'beach', 'boatramp']:

               filtered_parks = parks
          else:
               filtered_parks = [park for park in parks if park.get(filter_column) == 'true']

     #Render the index.html template with the parks data
     
     return render_template('index.html', parks=parks, search_word=search_word)
    

if __name__ == '__main__':
     app.run(debug=True)

















































#establish db connection parameters
"""db_setup = {
    'host': 'localhost',
    'database': 'HampRoadsParks',
    'user': 'postgres',
    'password': 'jalloJM@2020',
    'port': '5432'  
}"""



# Function with DB Connection setup
"""def search_item(search_word):
        #term = self.input.text

        try:
            #connection to postgreSQL
            conn = psycopg2.connect(**db_setup)
            cursor = conn.cursor()

            #Query DB
            query = 'SELECT "locationname" FROM "NewportNewsParks" WHERE "jurisdiction" ILIKE %s'
            query2 = 'SELECT "name" FROM "HParks" WHERE "jurisdiction" ILIKE %s'

            if search_word.lower() =="newport news":
                 q =cursor.execute(query, ('%'+search_word+'%',))
                 
            elif search_word.lower() == "hampton":
                 q2 = cursor.execute(query2, ('%'+search_word+'%',))
            else:
                 return []

                   
            #Collect data and close connection
            results = cursor.fetchall()
            cursor.close()
            conn.close()
            return results


        except Exception as e:
            print(f"Exception occured in search_item: {e}")
            return[("Error: " + str(e),)]
    

@app.route("/", methods=['GET'])
def home():
    return render_template("index.html", result=None)

@app.route("/results", methods=['POST'])
def results():
     search_term = request.form.get('search_word', '').strip()
     print("search term:", search_term)
     data = search_item(search_term)
     print("results", search_term)
     return render_template('index.html',result=data)

@app.route("/filter", methods=['POST'])
def filter():
    filter_term = request.form.get('filter_column')
    filter_value = request.form.get('filter_value')

    allowed_columns = ["dogpark", "boatramp", "beach"]

    if filter_term not in allowed_columns:
         return "Invalid filter column", 400
    if filter_value not in ['true', 'false']:
         return "missing filter value", 400
    
    bool_value = filter_value ='true'

    sql=f'SELECT "locationname" FROM "NewportNewsParks" WHERE "{filter_term}" = %s'
    sql2=f'SELECT "name" FROM "HParks" WHERE "{filter_term}" = %s'

    #sql2=f'SELECT "NAME" FROM "hparks" WHERE '
    conn = psycopg2.connect(**db_setup)
    cur = conn.cursor()
    
    cur.execute(sql, (bool_value,))
    result = cur.fetchall()
    conn.close()
    cur.close()
    return render_template("index.html", result=result)
    
 
    

if __name__ == "__main__":
    app.run(debug=True)"""



