"""
Script para probar la conexión directa a Supabase y verificar las credenciales
"""
import os
import sys
import psycopg2
from dotenv import load_dotenv

# Configurar codificación UTF-8 para Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Cargar variables de entorno
base_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(base_dir, '.env')
load_dotenv(env_path)

def test_connection():
    print("\n" + "="*60)
    print("PRUEBA DE CONEXION A SUPABASE")
    print("="*60)
    
    # Obtener variables
    db_host = os.getenv("DB_HOST")
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_port = int(os.getenv("DB_PORT", 5432))
    
    # Verificar si estamos usando el pooler
    is_pooler = "pooler" in db_host.lower() if db_host else False or db_port == 6543
    if is_pooler:
        # Para el pooler, el usuario debe incluir el identificador del proyecto
        proyecto_ref = os.getenv("SUPABASE_PROJECT_REF")
        if proyecto_ref and "." not in db_user:
            db_user = f"{db_user}.{proyecto_ref}"
            print(f"\n[INFO] Usuario formateado para pooler: {db_user}")
        elif not proyecto_ref:
            print(f"\n[ADVERTENCIA] Usando pooler pero SUPABASE_PROJECT_REF no está configurado.")
            print(f"   El usuario debe tener el formato: usuario.proyecto_ref")
            print(f"   Ejemplo: postgres.utysncfiyunejnujadmk")
    
    print(f"\nConfiguracion:")
    print(f"  Host: {db_host}")
    print(f"  Port: {db_port}")
    print(f"  Database: {db_name}")
    print(f"  User: {db_user}")
    print(f"  Password: {'***' if db_password else 'NO CONFIGURADA'}")
    
    if not all([db_host, db_name, db_user, db_password]):
        print("\n[ERROR] Faltan variables de entorno")
        return
    
    print(f"\nIntentando conectar...")
    
    try:
        connection = psycopg2.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_password,
            port=db_port,
            connect_timeout=10
        )
        print("[OK] Conexion exitosa!")
        
        # Probar una consulta simple
        cursor = connection.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"[OK] Version de PostgreSQL: {version[0][:50]}...")
        
        cursor.close()
        connection.close()
        print("\n[OK] Todo funciona correctamente!")
        
    except psycopg2.OperationalError as e:
        error_msg = str(e)
        print(f"\n[ERROR] Error de conexion:")
        print(f"  {error_msg}")
        
        if "Tenant or user not found" in error_msg:
            print("\n[INFO] El error 'Tenant or user not found' significa:")
            print("  1. La contraseña es incorrecta")
            print("  2. El usuario no existe o es incorrecto")
            print("  3. El proyecto puede estar pausado")
            print("  4. Si usas pooler, el usuario debe tener el formato: usuario.proyecto_ref")
            print("\n[SOLUCION]")
            if is_pooler:
                print("  IMPORTANTE: Con el pooler, el usuario debe tener el formato: usuario.proyecto_ref")
                print("  Ejemplo: postgres.utysncfiyunejnujadmk")
                print("  Agrega SUPABASE_PROJECT_REF a tu archivo .env")
                print("  El identificador del proyecto está en tu URL de Supabase:")
                print("  https://[PROYECTO_REF].supabase.co")
            print("  1. Ve a Supabase: Settings -> Database")
            print("  2. Resetea la contraseña")
            print("  3. Copia la nueva contraseña EXACTAMENTE")
            print("  4. Actualiza DB_PASSWORD en el archivo .env")
            print("  5. Si usas pooler, agrega SUPABASE_PROJECT_REF a tu archivo .env")
            print("  6. Asegurate de que no haya espacios en la contraseña")
            
            # Verificar si hay espacios
            if db_password:
                if db_password != db_password.strip():
                    print("\n[ADVERTENCIA] La contraseña tiene espacios al inicio o final!")
                    print(f"  Original: '{db_password}'")
                    print(f"  Sin espacios: '{db_password.strip()}'")
        elif "could not translate host name" in error_msg:
            print("\n[INFO] Error de DNS - el hostname no se puede resolver")
        else:
            print(f"\n[INFO] Error completo: {error_msg}")
            
    except Exception as e:
        print(f"\n[ERROR] Error inesperado: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_connection()

