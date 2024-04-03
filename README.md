# Binar-Gold-Challenge
Get started with Exploratory data analysis (EDA) using pandas, regex, matplotlib and seaborn
## Tentang API
![Alt text](image.png)
Proses pembuatan API menggunakan flask dan Swagger UI untuk membantu membuat tampilan antar-muka dokumentasi (docs) yang lebih interaktif. Pada API ini terdapat 2 endpoint yaitu:
> 1. **Text Processing** digunakan untuk membersihkan text dengan masukkan (input) berupa string 
> 2. **Upload & Process File CSV** digunakan untuk membersihkan text dengan masukkan (input) berupa file CSV.

## Daftar Fungsi API
### Text Processing
Pada Text Processing proses cleaning data mencakup:
1. Semua huruf akan diubah menjadi lowercase
1. Menghapus kata url, http dan http 
1. Menghapus semua kata yang mengandung ‘/’ seperti /n dan /th47g
1. Menghapus text emoji seperti :D dan :)
1. Menghapus semua karakter di luar huruf, angka dan whitespace
1. Menghapus extra space

### Upload & Process File CSV
Pada Upload & Process File CSV  - Tweet Cleaning Data proses cleaning data mencakup:
1. Semua huruf akan diubah menjadi lowercase
1. Menghapus kata user, rt, url, https, http dan &amp
1. Menghapus semua kata yang mengandung ‘/’ seperti /n dan /th47g
1. Menghapus text emoji seperti :D dan :)
1. Menghapus semua karakter di luar huruf dan whitespace
1. Menghapus semua angka
1. Menghapus extra space
1. Mengubah setiap kata yang terdapat pada New Kamus Alay menjadi arti katanya
1. Menghapus stopword yang terdapat pada List stopword

## Daftar File
Selain API, terdapat file lain yang digunakan untuk proses Cleaning dan Exploratory Data Analysis (EDA)
- EDA Tweet data part 1.ipynb
- EDA Tweet data part 2.ipynb

> 2 file di atas merupakan file yang berisi semua proses EDA menggunakan dataset yang bersumber dari *Workshop on Abusive Language Online* (Ibrohim M,  2019) yang publikasinya dapat diakses [di sini](https://www.aclweb.org/anthology/W19-3506) sementara untuk datasetnya dapat diakses [di sini](https://github.com/okkyibrohim/id-multi-label-hate-speech-and-abusive-language-detection).

### Dalam Folder API
- **app.py** adalah program untuk menjalankan API
- **DataCleaning.py** merupakan file yang digunakan untuk proses cleaning di dalam program API
- **Data_For_DataCleaning** merupakan folder yang berisi file .csv dan .txt untuk keperluan program **DataCleaning.py**
- **DataBase** merupakan folder yang digunakan untuk menyimpan seluruh data pre dan pasca processing menggunakan API
- **docs** merupakan folder yang berisi template Swagger UI

    > **text_processing.yml** template yang digunakan untuk endpoint **Text Processing**
    
    > **processing_file.yml** template yang digunakan untuk endpoint **Upload & Process File CSV**
