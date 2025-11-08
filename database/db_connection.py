import psycopg2
import os
import socket
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env en la raíz del proyecto
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(base_dir, '.env')
load_dotenv(env_path)

def resolve_hostname(hostname):
    """Intenta resolver el hostname a una dirección IP"""
    try:
        # Intentar obtener la dirección IPv4 primero
        ipv4 = socket.gethostbyname(hostname)
        return ipv4
    except socket.gaierror:
        try:
            # Si no hay IPv4, intentar IPv6
            ipv6_info = socket.getaddrinfo(hostname, None, socket.AF_INET6)
            if ipv6_info:
                return ipv6_info[0][4][0]
        except:
            pass
    return None

def get_db_connection():
    # Validar que todas las variables de entorno estén configuradas
    required_vars = ["DB_HOST", "DB_NAME", "DB_USER", "DB_PASSWORD"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        error_msg = f"❌ Variables de entorno faltantes: {', '.join(missing_vars)}. Por favor, crea un archivo .env en la raíz del proyecto."
        print(error_msg)
        raise ValueError(error_msg)
    
    db_host = os.getenv("DB_HOST")
    db_port = int(os.getenv("DB_PORT", 5432))
    db_user = os.getenv("DB_USER")
    
    # Verificar si estamos usando el pooler
    is_pooler = "pooler" in db_host.lower() or db_port == 6543
    if is_pooler:
        print(f"ℹ️ Usando Session Pooler: {db_host}:{db_port}")
        # Para el pooler, el usuario debe incluir el identificador del proyecto
        # Formato: usuario.proyecto_ref (ej: postgres.utysncfiyunejnujadmk)
        proyecto_ref = os.getenv("SUPABASE_PROJECT_REF")
        if proyecto_ref and "." not in db_user:
            # Si tenemos el proyecto_ref y el usuario no tiene el formato correcto, agregarlo
            db_user = f"{db_user}.{proyecto_ref}"
            print(f"ℹ️ Usuario formateado para pooler: {db_user}")
        elif not proyecto_ref:
            print(f"⚠️ ADVERTENCIA: Usando pooler pero SUPABASE_PROJECT_REF no está configurado.")
            print(f"   El usuario debe tener el formato: usuario.proyecto_ref")
            print(f"   Ejemplo: postgres.utysncfiyunejnujadmk")
    
    # Intentar resolver el hostname si es necesario
    resolved_ip = None
    try:
        resolved_ip = resolve_hostname(db_host)
        if resolved_ip:
            print(f"ℹ️ Hostname resuelto: {db_host} -> {resolved_ip}")
    except Exception as e:
        print(f"⚠️ No se pudo resolver el hostname, intentando conexión directa: {e}")
    
    try:
        # Intentar conexión con el hostname original
        connection = psycopg2.connect(
            host=db_host,
            database=os.getenv("DB_NAME"),
            user=db_user,
            password=os.getenv("DB_PASSWORD"),
            port=db_port,
            connect_timeout=10  # Timeout de 10 segundos
        )
        print("✅ Conexión exitosa a la base de datos")
        return connection
    except psycopg2.OperationalError as e:
        error_msg = str(e)
        if "could not translate host name" in error_msg or "Name or service not known" in error_msg:
            # Si hay una IP resuelta, intentar con esa
            if resolved_ip:
                print(f"🔄 Intentando conexión con IP resuelta: {resolved_ip}")
                try:
                    connection = psycopg2.connect(
                        host=resolved_ip,
                        database=os.getenv("DB_NAME"),
                        user=db_user,
                        password=os.getenv("DB_PASSWORD"),
                        port=db_port,
                        connect_timeout=10
                    )
                    print("✅ Conexión exitosa a la base de datos usando IP resuelta")
                    return connection
                except Exception as e2:
                    print(f"❌ También falló la conexión con IP: {e2}")
            
            print(f"❌ Error de conexión: No se puede resolver el host de la base de datos.")
            print(f"   Host: {db_host}")
            print(f"   IP resuelta: {resolved_ip if resolved_ip else 'No disponible'}")
            print(f"   Verifica tu conexión a internet y que el hostname sea correcto.")
            print(f"   Sugerencia: Verifica en Supabase que el proyecto esté activo.")
        elif "Tenant or user not found" in error_msg:
            print(f"❌ Error de autenticación: Usuario o contraseña incorrectos.")
            print(f"   Host: {db_host}")
            print(f"   Usuario usado: {db_user}")
            print(f"   Database: {os.getenv('DB_NAME')}")
            if is_pooler:
                print(f"   💡 IMPORTANTE: Con el pooler, el usuario debe tener el formato: usuario.proyecto_ref")
                print(f"      Ejemplo: postgres.utysncfiyunejnujadmk")
                print(f"      Agrega SUPABASE_PROJECT_REF a tu archivo .env")
            print(f"   💡 Verifica las credenciales en Supabase:")
            print(f"      1. Ve a Settings → Database")
            print(f"      2. Verifica o resetea la contraseña")
            print(f"      3. Si usas pooler, asegúrate de usar el formato: postgres.proyecto_ref")
        else:
            print(f"❌ Error de conexión a la base de datos: {e}")
        raise
    except Exception as e:
        print(f"❌ Error de conexión a la base de datos: {e}")
        raise

