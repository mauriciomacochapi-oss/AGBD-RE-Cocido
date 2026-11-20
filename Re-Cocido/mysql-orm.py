
import os

from dotenv import load_dotenv

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from sqlalchemy import URL, create_engine, text, String, Integer

# source venv/bin/activate 
# pip install python-dotenv
# python mysql-orm.py
# ==========================================
# 1. CARGAR VARIABLES DE ENTORNO
# ==========================================

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
DB_DATABASE = os.getenv("DB_DATABASE")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")


# ==========================================
# 2. CONEXION A MYSQL
# ==========================================

url = URL.create(
    "mysql+pymysql",
    host=DB_HOST,
    port=DB_PORT,
    database=DB_DATABASE,
    username=DB_USERNAME,
    password=DB_PASSWORD,
)

motor = create_engine(url)


# ==========================================
# 3. FUNCION PARA CALCULAR ESTRELLAS
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
# 4. DEFINICION DEL ORM
# ==========================================

class Base(DeclarativeBase):
    pass


class Jugador(Base):

    __tablename__ = "jugadores"

    _id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    _nombre: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    _puntaje: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )

    _estrellas: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )


# ==========================================
# 5. CONEXION Y CREACION DE TABLA
# ==========================================

try:

    with motor.connect() as conexion:

        resultado = conexion.execute(
            text("SELECT 1")
        ).scalar_one()

    print("\n================================")
    print(" CONEXION A MYSQL EXITOSA")
    print("================================")

    print(f"Resultado de conexion: {resultado}")


    # Crear la tabla solamente si no existe
    Base.metadata.create_all(bind=motor)

    print("\nTabla 'jugadores' verificada correctamente.")


    # ==========================================
    # 6. REGISTRO DE JUGADOR SIN DUPLICADOS
    # ==========================================

    puntaje_obtenido = 950
    nombre_jugador = "Mauricio"

    with Session(motor) as sesion:

        jugador_existente = sesion.query(Jugador).filter_by(
            _nombre=nombre_jugador
        ).first()


        # ==========================================
        # 7. SI EL JUGADOR NO EXISTE
        # ==========================================

        if jugador_existente is None:

            nuevo_jugador = Jugador(
                _nombre=nombre_jugador,
                _puntaje=puntaje_obtenido,
                _estrellas=calcular_estrellas(puntaje_obtenido)
            )

            sesion.add(nuevo_jugador)

            sesion.commit()

            print("\n================================")
            print(" JUGADOR REGISTRADO EXITOSAMENTE")
            print("================================")

            print(f"ID: {nuevo_jugador._id}")
            print(f"Nombre: {nuevo_jugador._nombre}")
            print(f"Puntaje: {nuevo_jugador._puntaje}")
            print(f"Estrellas: {nuevo_jugador._estrellas}")

            print("================================")


        # ==========================================
        # 8. SI EL JUGADOR YA EXISTE
        # ==========================================

        else:

            print("\n================================")
            print(" ⚠️ JUGADOR EXISTENTE")
            print("================================")

            print(
                f"El jugador '{nombre_jugador}' "
                "ya está registrado."
            )

            print("No se realizó una nueva inserción.")

            print(f"ID: {jugador_existente._id}")
            print(f"Nombre: {jugador_existente._nombre}")
            print(f"Puntaje: {jugador_existente._puntaje}")
            print(f"Estrellas: {jugador_existente._estrellas}")

            print("================================")


except SQLAlchemyError as error:

    print("\n================================")
    print(" ERROR EN LA BASE DE DATOS")
    print("================================")

    print(error)


finally:

    motor.dispose()
