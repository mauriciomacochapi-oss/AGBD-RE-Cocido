from sqlalchemy import URL, create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from sqlalchemy import URL, create_engine, text, String

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



# ==========================================
    # 1. Función para calcular las estrellas según el puntaje
    # ==========================================
    def calcular_estrellas(puntaje: int) -> int:
        if puntaje >= 1200:
            return 3
        elif puntaje >= 800:
            return 2
        elif puntaje >= 400:
            return 1
        else:
            return 0

# ==========================================
    # AQUÍ AGREGAS TU ORM Y LA CREACIÓN DE LA TABLA
    # ==========================================
    
    class Base(DeclarativeBase):
        pass

    class Jugador(Base):
        __tablename__ = "jugadores"

        _id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
        _nombre: Mapped[str] = mapped_column(String(50), nullable=False)
        _puntaje: Mapped[int] = mapped_column(default=0, nullable=False)
        _estrellas: Mapped[int] = mapped_column(default=0, nullable=False) # <--- Nueva columna
    try:
        Base.metadata.create_all(bind=motor)
        print("¡Tabla 'jugadores' creada exitosamente mediante ORM!")
    except SQLAlchemyError as e:
        print("Error al crear la tabla:", e)

    
    # ==========================================
    # 3. AQUÍ ABAJO ESTA LA PRUEBA DE INSERCION
    # ==========================================
    puntaje_obtenido = 950 

    with Session(motor) as sesion:
        nuevo_jugador = Jugador(
            _nombre="Mauricio",
            _puntaje=puntaje_obtenido,
            _estrellas=calcular_estrellas(puntaje_obtenido)
        )
        sesion.add(nuevo_jugador)
        sesion.commit()
        print("¡Jugador guardado con éxito en la base de datos!")

    