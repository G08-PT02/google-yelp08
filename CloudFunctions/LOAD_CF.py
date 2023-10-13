from google.cloud import bigquery

project_name = 'pure-hue-399113'
datawarehouse = 'restaurant_staging_dataset'

schemas_id = {

                'restaurants_dim':[
                bigquery.SchemaField("business_id", "STRING"),
                bigquery.SchemaField("name", "STRING"),],
                'geographical_data_dim':[
                bigquery.SchemaField("business_id", "STRING"),
                bigquery.SchemaField("address", "STRING"),
                bigquery.SchemaField("city", "STRING"),
                bigquery.SchemaField("state", "STRING"),
                bigquery.SchemaField("postal_code", "STRING"),
                bigquery.SchemaField("latitude", "FLOAT64"),
                bigquery.SchemaField("longitude","FLOAT64"),],
                'attributes_google_dim': [
                bigquery.SchemaField("business_id", "STRING"),
                bigquery.SchemaField("Health_safety", "STRING"),
                bigquery.SchemaField("Accessibility", "STRING"),
                bigquery.SchemaField("Planning", "STRING"),
                bigquery.SchemaField("Payments", "STRING"),
                bigquery.SchemaField("Offerings", "STRING"),
                bigquery.SchemaField("Amenities", "STRING"),
                bigquery.SchemaField("From_the_business", "STRING"),
                bigquery.SchemaField("Popular_for", "STRING"),
                bigquery.SchemaField("Atmosphere", "STRING"),
                bigquery.SchemaField("Highlights", "STRING"),
                bigquery.SchemaField("Dining_options", "STRING"),],
                'schedules_dim':[
                bigquery.SchemaField("business_id", "STRING"),
                bigquery.SchemaField("Monday", "STRING"),
                bigquery.SchemaField("Tuesday", "STRING"),
                bigquery.SchemaField("Wednesday", "STRING"),
                bigquery.SchemaField("Thursday", "STRING"),
                bigquery.SchemaField("Friday", "STRING"),
                bigquery.SchemaField("Saturday", "STRING"),
                bigquery.SchemaField("Sunday", "STRING"),],
                'review_google_fact':[
                bigquery.SchemaField("business_id", "STRING"),
                bigquery.SchemaField("user_id", "STRING"),
                bigquery.SchemaField("name", "STRING"),
                bigquery.SchemaField("rating", "INT64"),
                bigquery.SchemaField("text", "STRING"),
                bigquery.SchemaField("date", "DATE"),],
                'yelp_reviews':[
                bigquery.SchemaField("review_id", "STRING"),
                bigquery.SchemaField("user_id", "STRING"),
                bigquery.SchemaField("business_id", "STRING"),
                bigquery.SchemaField("stars", "INT64"),
                bigquery.SchemaField("useful", "INT64"),
                bigquery.SchemaField("funny", "INT64"),
                bigquery.SchemaField("cool", "INT64"),
                bigquery.SchemaField("text", "STRING"),
                bigquery.SchemaField("date", "DATE"),],
                'category_google_dim': [
                bigquery.SchemaField("business_id", "STRING"),
                bigquery.SchemaField("American_restaurant", "INT64"),
                bigquery.SchemaField("Asian_restaurant", "INT64"),
                bigquery.SchemaField("Barbecue_restaurant", "INT64"),
                bigquery.SchemaField("Breakfast_restaurant", "INT64"),
                bigquery.SchemaField("Caribbean_restaurant", "INT64"),
                bigquery.SchemaField("Chicken_restaurant", "INT64"),
                bigquery.SchemaField("Chicken_wings_restaurant", "INT64"),
                bigquery.SchemaField("Chinese_restaurant", "INT64"),
                bigquery.SchemaField("Dessert_restaurant", "INT64"),
                bigquery.SchemaField("Dominican_restaurant", "INT64"),
                bigquery.SchemaField("Family_restaurant", "INT64"),
                bigquery.SchemaField("Fast_food_restaurant", "INT64"),
                bigquery.SchemaField("Fine_dining_restaurant", "INT64"),
                bigquery.SchemaField("Greek_restaurant", "INT64"),
                bigquery.SchemaField("Hamburger_restaurant", "INT64"),
                bigquery.SchemaField("Health_food_restaurant", "INT64"),
                bigquery.SchemaField("Hot_dog_restaurant", "INT64"),
                bigquery.SchemaField("Indian_restaurant", "INT64"),
                bigquery.SchemaField("Italian_restaurant", "INT64"),
                bigquery.SchemaField("Jamaican_restaurant", "INT64"),
                bigquery.SchemaField("Japanese_restaurant", "INT64"),
                bigquery.SchemaField("Korean_restaurant", "INT64"),
                bigquery.SchemaField("Latin_American_restaurant", "INT64"),
                bigquery.SchemaField("Mediterranean_restaurant", "INT64"),
                bigquery.SchemaField("Mexican_restaurant", "INT64"),
                bigquery.SchemaField("New_American_restaurant", "INT64"),
                bigquery.SchemaField("Peruvian_restaurant", "INT64"),
                bigquery.SchemaField("Pizza_restaurant", "INT64"),
                bigquery.SchemaField("Salvadoran_restaurant", "INT64"),
                bigquery.SchemaField("Seafood_restaurant", "INT64"),
                bigquery.SchemaField("Soul_food_restaurant", "INT64"),
                bigquery.SchemaField("Sushi_restaurant", "INT64"),
                bigquery.SchemaField("Taco_restaurant", "INT64"),
                bigquery.SchemaField("Thai_restaurant", "INT64"),
                bigquery.SchemaField("Vegan_restaurant", "INT64"),
                bigquery.SchemaField("Vietnamese_restaurant", "INT64"),],
                'yelp_users':[
                bigquery.SchemaField("user_id", "STRING"),
                bigquery.SchemaField("name", "STRING"),
                bigquery.SchemaField("review_count", "INT64"),
                bigquery.SchemaField("yelping_since", "DATE"),
                bigquery.SchemaField("useful", "INT64"),
                bigquery.SchemaField("funny", "INT64"),
                bigquery.SchemaField("cool", "INT64"),
                bigquery.SchemaField("friends", "STRING"),
                bigquery.SchemaField("fans", "INT64"),
                bigquery.SchemaField("compliment_more", "INT64"),
                bigquery.SchemaField("compliment_profile", "INT64"),
                bigquery.SchemaField("compliment_cute", "INT64"),
                bigquery.SchemaField("compliment_list", "INT64"),
                bigquery.SchemaField("compliment_note", "INT64"),
                bigquery.SchemaField("compliment_plain", "INT64"),
                bigquery.SchemaField("compliment_cool", "INT64"),
                bigquery.SchemaField("compliment_funny", "INT64"),
                bigquery.SchemaField("compliment_writer", "INT64"),
                bigquery.SchemaField("compliment_photos", "INT64"),],

                'tips_yelp_dim':[
                bigquery.SchemaField("user_id", "STRING"),
                bigquery.SchemaField("business_id", "STRING"),
                bigquery.SchemaField("text", "STRING"),
                bigquery.SchemaField("date", "DATE"),
                bigquery.SchemaField("compliment_count", "INT64"),]

            }

def load_datawarehouse(event, context):
    file = event
    file_name=file['name']   #se saca el nombre del archivo nuevo en el bucket ETL

    print(f"Se detectó que se subió el archivo {file_name} en el bucket {file['bucket']}.")
    source_bucket_name = file['bucket'] #nombre del bucket donde esta el archivo
    
    if "metadato_sitio.parquet" in file_name:
        table_name = 'restaurants_dim'
    elif "metadato_sitio_geo.parquet" in file_name:
        table_name = 'geographical_data_dim'
    elif "metadato_sitio_misc.parquet" in file_name:
        table_name= 'attributes_google_dim'
    elif "metadato_sitio_horarios.parquet" in file_name:
        table_name= 'schedules_dim'
    elif "metadato_sitio_categ.parquet" in file_name:
        table_name= 'category_google_dim'
    elif "reviews_estados" in file_name:
        table_name = 'review_google_fact'
    elif "yelps_business_sample_business" in file_name:
        table_name = 'restaurants_dim'
    elif "yelps_business_sample_geograficos" in file_name:
        table_name='geographical_data_dim'
    elif "yelps_business_sample_horarios" in file_name:
        table_name='schedules_dim'
    elif "yelps_reviews_sample" in file_name:
        table_name = 'reviews_yelp_fact'
    elif "user_sample.parquet" in file_name:
        table_name = 'users_yelp_dim'
    elif "tip_sample.parquet" in file_name:
        table_name = 'tips_yelp_dim'
    elif "yelps_business_sample_geo.parquet" in file_name:
        table_name = 'geographical_data_dim'
    

    
    # Construct a BigQuery client object.
    client = bigquery.Client()

    # TODO(developer): Set table_id to the ID of the table to create.
    # table_id = "your-project.your_dataset.your_table_name"

    source_path = "gs://"+source_bucket_name+"/"+file_name # ruta al archivo cargado en el bucket de stage
    table_id = project_name + "." + datawarehouse + "." + table_name 
    # table_id - ruta a la tabla a carga en big query: "nombre_del_proyecto"."nombre_de_la_base_de_datos"."nombre de la tabla"
    # cambiar nombre del proyecto y nombre de la base de datos en bigquery arriba (al inicio)  
    print(f"Archivo source_bucket_name : {source_path}.")
    print(f"Archivo table_name : {table_name}.")
    print(f"Archivo table_id : {table_id}.")


    job_config = bigquery.LoadJobConfig(
        schema= schemas_id[table_name],
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        # The source format defaults to CSV, so the line below is optional.
        source_format=bigquery.SourceFormat.PARQUET,
    )
    #poner ubicación de archivo customers
    uri = source_path

    load_job = client.load_table_from_uri(
        uri, table_id, job_config=job_config
    )  # Make an API request.

    load_job.result()  # Waits for the job to complete.

    destination_table = client.get_table(table_id)  # Make an API request.
    print("Loaded {} rows in the table {}".format(destination_table.num_rows,table_name))