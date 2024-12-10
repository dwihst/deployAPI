
from  fastapi import FastAPI, HTTPException, Header
import pandas as pd

#create object/instance
app = FastAPI()

#create API key
API_key = "jeno"

#create endpoint home
@app.get("/")
def home ():
    return{"message": "Selamat datang di Toko Dwi"}

# create endpoint data
@app.get("/data")
def read_data():
    #untuk read data from csv
    df =  pd.read_csv("data.csv")
    #convert data frame to dict with record for each row
    return df.to_dict(orient="records") #mengembalikan data
#sumber:https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_dict.html
#kalo to_dict = lebih rapi dibandingkan to_json

#create endpoint data with number of parameter id
@app.get("/data/{number_id}") #tidak apa2 tidak sesuai 
def read_item(number_id: int):
    #untuk read data from csv
    df =  pd.read_csv("data.csv")
    #convert data frame to dict with record for each row
    #return df.to_dict(orient="records") #mengembalikan data

    #menambahakan data filter by id
    filter_data = df[df["id"] == number_id] #wrap jadi [] agar tidak menjadi boolean

    #check if fillter data is empty
    if len(filter_data) == 0:
        raise HTTPException(status_code = 404, detail = "Data tidak ditemukan")

    #convert filter dataframe to dict w/ record for each row
    return filter_data.to_dict(orient="records")

#create endpoint update file csv
@app.put("/item/{number_id}")
def update_item(number_id: int, nama_barang: str, harga:float):
    # read data  from csv
    df =  pd.read_csv("data.csv")
    #create dataframe from input
    updated_df = pd.DataFrame([
        {"id": number_id,
         "nama_barang":nama_barang,
         "harga":harga}]
    ) #atau bisa menggunakan' harga},index=[0])'

    #menggabungkan dataframe lama menjadi dataframe baru
    df = pd.concat([df, updated_df], ignore_index=True) #bisa concat banyak apabila taroh di list

    #simpan ke csv
    df.to_csv("data.csv", index=False)

    return {"message": f"Item with name {nama_barang} has been savedsuccessfully."}

@app.get("/secret")
def read_secret(api_key: str = Header(None)): #ini header API
    #read data
    secret_df = pd.read_csv("secret_data.csv")

    #cek apakah if api key valid apa engga
    if api_key != API_key:
        #if api key tidak valid return error
        raise HTTPException(status_code = 401, detail = "API key tidak valid")
    
    return secret_df.to_dict(orient = "records")


