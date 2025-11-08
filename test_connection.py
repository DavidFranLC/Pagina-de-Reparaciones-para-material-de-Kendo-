"""
Script de diagnóstico para verificar la conexión a Supabase
"""
import os
import socket
import sys
from dotenv import load_dotenv

# Configurar codificación UTF-8 para Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Cargar variables de entorno
base_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(base_dir, '.env')
load_dotenv(env_path)

def test_dns_resolution(hostname):
    """Intenta resolver el hostname a una dirección IP"""
    print(f"\n{'='*60}")
    print(f"RESOLUCION DNS para: {hostname}")
    print(f"{'='*60}")
    
    try:
        # Intentar IPv4
        print("\n1. Intentando resolucion IPv4...")
        ipv4 = socket.gethostbyname(hostname)
        print(f"   [OK] IPv4 encontrada: {ipv4}")
    except socket.gaierror as e:
        print(f"   [ERROR] No se pudo resolver IPv4: {e}")
        ipv4 = None
    
    try:
        # Intentar IPv6
        print("\n2. Intentando resolucion IPv6...")
        ipv6_info = socket.getaddrinfo(hostname, None, socket.AF_INET6)
        if ipv6_info:
            ipv6 = ipv6_info[0][4][0]
            print(f"   [OK] IPv6 encontrada: {ipv6}")
        else:
            ipv6 = None
    except Exception as e:
        print(f"   [ERROR] No se pudo resolver IPv6: {e}")
        ipv6 = None
    
    # Intentar con getaddrinfo (más completo)
    try:
        print("\n3. Intentando resolucion con getaddrinfo...")
        addr_info = socket.getaddrinfo(hostname, 5432, socket.AF_UNSPEC, socket.SOCK_STREAM)
        if addr_info:
            print(f"   [OK] Se encontraron {len(addr_info)} direccion(es):")
            for i, info in enumerate(addr_info[:3], 1):  # Mostrar solo las primeras 3
                family, socktype, proto, canonname, sockaddr = info
                ip = sockaddr[0]
                family_name = "IPv4" if family == socket.AF_INET else "IPv6"
                print(f"      {i}. {family_name}: {ip}")
        else:
            print("   [ERROR] No se encontraron direcciones")
    except Exception as e:
        print(f"   [ERROR] Error en getaddrinfo: {e}")
    
    return ipv4, ipv6

def test_port_connection(hostname, port):
    """Intenta conectar al puerto para verificar si está abierto"""
    print(f"\n{'='*60}")
    print(f"PRUEBA DE CONEXION al puerto {port}")
    print(f"{'='*60}")
    
    try:
        print(f"\nIntentando conectar a {hostname}:{port}...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((hostname, port))
        sock.close()
        
        if result == 0:
            print(f"   [OK] Puerto {port} esta ABIERTO y accesible")
            return True
        else:
            print(f"   [ERROR] Puerto {port} esta CERRADO o no accesible (codigo: {result})")
            print(f"   [INFO] Esto podria indicar un problema de firewall")
            return False
    except socket.gaierror as e:
        print(f"   [ERROR] Error de DNS: {e}")
        print(f"   [INFO] No se puede resolver el hostname")
        return False
    except Exception as e:
        print(f"   [ERROR] Error de conexion: {e}")
        return False

def test_with_ip(ip, port):
    """Intenta conectar usando una IP directamente"""
    print(f"\n{'='*60}")
    print(f"PRUEBA DE CONEXION usando IP: {ip}")
    print(f"{'='*60}")
    
    try:
        print(f"\nIntentando conectar a {ip}:{port}...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((ip, port))
        sock.close()
        
        if result == 0:
            print(f"   [OK] Conexion exitosa usando IP {ip}")
            return True
        else:
            print(f"   [ERROR] No se pudo conectar usando IP {ip} (codigo: {result})")
            return False
    except Exception as e:
        print(f"   [ERROR] Error: {e}")
        return False

def check_env_file():
    """Verifica que el archivo .env existe y tiene las variables necesarias"""
    print(f"\n{'='*60}")
    print(f"VERIFICACION DEL ARCHIVO .env")
    print(f"{'='*60}")
    
    env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
    
    if os.path.exists(env_file):
        print(f"   [OK] Archivo .env encontrado: {env_file}")
        
        required_vars = ["DB_HOST", "DB_NAME", "DB_USER", "DB_PASSWORD"]
        missing = []
        
        for var in required_vars:
            value = os.getenv(var)
            if value:
                # Ocultar contraseña
                display_value = "***" if var == "DB_PASSWORD" else value
                print(f"   [OK] {var}: {display_value}")
            else:
                print(f"   [ERROR] {var}: NO CONFIGURADA")
                missing.append(var)
        
        if missing:
            print(f"\n   [ADVERTENCIA] Variables faltantes: {', '.join(missing)}")
            return False
        else:
            print(f"\n   [OK] Todas las variables estan configuradas")
            return True
    else:
        print(f"   [ERROR] Archivo .env NO encontrado en: {env_file}")
        print(f"   [INFO] Crea el archivo .env en la raiz del proyecto")
        return False

def main():
    print("\n" + "="*60)
    print("DIAGNOSTICO DE CONEXION A SUPABASE")
    print("="*60)
    
    # Verificar archivo .env
    env_ok = check_env_file()
    
    if not env_ok:
        print("\n❌ Por favor, configura el archivo .env primero")
        return
    
    # Obtener hostname y puerto
    hostname = os.getenv("DB_HOST")
    port = int(os.getenv("DB_PORT", 5432))
    
    if not hostname:
        print("\n❌ DB_HOST no está configurado en el archivo .env")
        return
    
    # Resolver hostname
    ipv4, ipv6 = test_dns_resolution(hostname)
    
    # Probar conexión al puerto
    port_open = test_port_connection(hostname, port)
    
    # Si hay una IP resuelta, intentar conectar directamente
    if ipv4:
        test_with_ip(ipv4, port)
    
    # Resumen y recomendaciones
    print(f"\n{'='*60}")
    print("RESUMEN Y RECOMENDACIONES")
    print(f"{'='*60}")
    
    if not ipv4 and not ipv6:
        print("\n[ERROR] PROBLEMA: No se puede resolver el hostname")
        print("   Soluciones:")
        print("   1. Verifica tu conexion a internet")
        print("   2. Verifica que el hostname sea correcto en Supabase")
        print("   3. Intenta cambiar el DNS (8.8.8.8 o 1.1.1.1)")
    elif not port_open:
        print("\n[ERROR] PROBLEMA: El puerto esta cerrado o bloqueado")
        print("   Soluciones:")
        print("   1. Verifica el firewall de Windows:")
        print("      - Abre 'Firewall de Windows Defender'")
        print("      - Ve a 'Configuracion avanzada'")
        print("      - Verifica las reglas de salida para Python")
        print("   2. Verifica que tu antivirus no este bloqueando")
        print("   3. Verifica que el proyecto de Supabase este activo")
    else:
        print("\n[OK] La resolucion DNS y la conexion al puerto funcionan")
        print("   El problema podria estar en:")
        print("   1. Las credenciales de la base de datos")
        print("   2. La configuracion de psycopg2")
        print("   3. Un problema temporal de Supabase")

if __name__ == "__main__":
    main()

