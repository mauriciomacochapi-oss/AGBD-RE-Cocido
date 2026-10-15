from sqlalchemy import URL, create_engine, text
from sqlalchemy.exc import SQLAlchemyError

DB_HOST = "10.9.120.5"
DB_PORT = 3306
DB_DATABASE = "RE-Codido"
DB_USERNAME = "recocido"
DB_PASSWORD = "rc123456"

url = URL.create(
    "mysql+pymysql",
    host=DB_HOST,
    port=DB_PORT,
    database=DB_DATABASE,
    username=DB_USERNAME,
    password=DB_PASSWORD,
)

motor = create_engine(url)

try:

    with motor.connect() as conexion:
        resultado = conexion.execute(text("SELECT 1")).scalar_one()
    print("Conexion a MySQL OK.")

except SQLAlchemyError as error:
    print("No se pudo conectar. Revisa la red, la base, el usuario y la clave.")
    print(error.orig)
else:
    print(f"conexion exitosa {resultado}")    