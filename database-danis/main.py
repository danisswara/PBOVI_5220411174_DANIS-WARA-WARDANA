import mysql.connector

class Database:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.connection.cursor()
            print("Koneksi ke database berhasil.\n")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def execute_query(self, query):
        try:
            if not self.connection.is_connected():
                self.connect()
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            return results
        except mysql.connector.Error as err:
            print(f"Error executing query: {err}")
            return None

    def commit_and_close(self):
        try:
            self.connection.commit()
            print("Perubahan telah di-commit.")
        except mysql.connector.Error as err:
            print(f"Error committing changes: {err}")
        finally:
            if self.connection.is_connected():
                self.cursor.close()
                self.connection.close()
                print("Koneksi ditutup.")


class Minuman:
    def __init__(self, nama_minuman, jenis_minuman, harga_minuman, jumlah_stok):
        self.nama_minuman = nama_minuman
        self.jenis_minuman = jenis_minuman
        self.harga_minuman = harga_minuman
        self.jumlah_stok = jumlah_stok

    def save_to_database(self, db):
        query = f"INSERT INTO tabel_minuman (nama_minuman, jenis_minuman, harga_minuman, jumlah_stok) VALUES ('{self.nama_minuman}', '{self.jenis_minuman}', {self.harga_minuman}, {self.jumlah_stok})"
        db.execute_query(query)
        db.commit_and_close()
        print(f"Minuman {self.nama_minuman} telah disimpan ke dalam database.")

    def read_from_database(self, db):
        query = f"SELECT * FROM tabel_minuman WHERE nama_minuman = '{self.nama_minuman}'"
        results = db.execute_query(query)
        if results:
            for row in results:
                print("ID           :", row[0])
                print("Nama         :", row[1])
                print("Jenis        :", row[2])
                print("Harga        :", row[3])
                print("Jumlah Stok  :", row[4])
        else:
            print(f"Minuman {self.nama_minuman} tidak ditemukan dalam database.")

    def update_in_database(self, db):
        query = f"UPDATE tabel_minuman SET jenis_minuman = '{self.jenis_minuman}', harga_minuman = {self.harga_minuman}, jumlah_stok = '{self.jumlah_stok}' WHERE nama_minuman = '{self.nama_minuman}'"
        db.execute_query(query)
        db.commit_and_close()
        print(f"Informasi Minuman {self.nama_minuman} telah diperbarui di dalam database {db.database}")

        
    def delete_from_database(self, db):
        query = f"DELETE FROM tabel_minuman WHERE nama_minuman = '{self.nama_minuman}'"
        db.execute_query(query)
        db.commit_and_close()
        print(f"Minuman {self.nama_minuman} telah dihapus dari database.")

class Menu:
    def __init__(self, database):
        self.database = database

    def show_menu(self):
        query = f"SELECT * FROM tabel_minuman"
        results = self.database.execute_query(query)
        if results:
            for no,row in enumerate(results):
                print(f"{no+1}. {row[1]} = Rp {row[3]:,.2f}")

# membuat object database
database = Database('localhost', 'root', 'root', '5220411174')
database.connect()

# membuat object daftar myMenu untuk menampilkan daftar menu
myMenu = Menu(database)

# Membuat 5 daftar objek minuman
everyday_latte = Minuman('Everyday Latte', 'Coffee Series', 12000, 10)
my_sweaty_berry = Minuman('My Sweaty Berry', 'Sweat Series', 14000, 20)
dark_choco = Minuman('Dark Choco', 'Milk Series', 10000, 20)
tropical_slim = Minuman('Tropical Slim', 'Tea Series', 20000, 20)
red_velvet = Minuman('Red Velvet', 'Milk Series', 70000, 20)

# memasukkan objek ke dalam tabel database
# tampung_menu = [everyday_latte, my_sweaty_berry, dark_choco, tropical_slim, red_velvet]
# for list_menu in tampung_menu:
#     list_menu.save_to_database(database)

# tropical_slim.delete_from_database(database)


myMenu.show_menu()

# print("Daftar Minuman\n")
# myMenu.show_menu()


