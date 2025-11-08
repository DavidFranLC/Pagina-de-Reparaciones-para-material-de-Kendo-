# 🔧 Guía: Verificar Firewall y Resolver Hostname

## 📋 Índice
1. [Ejecutar el Script de Diagnóstico](#ejecutar-el-script-de-diagnóstico)
2. [Verificar el Firewall de Windows](#verificar-el-firewall-de-windows)
3. [Resolver el Hostname Manualmente](#resolver-el-hostname-manualmente)
4. [Soluciones Adicionales](#soluciones-adicionales)

---

## 🚀 Ejecutar el Script de Diagnóstico

Primero, ejecuta el script de diagnóstico que creamos:

```powershell
# Activar el entorno virtual
.\venv\Scripts\Activate.ps1

# Ejecutar el script de diagnóstico
python test_connection.py
```

Este script te mostrará:
- ✅ Si el archivo `.env` existe y está configurado
- ✅ Si se puede resolver el hostname a una IP
- ✅ Si el puerto 5432 está abierto
- ✅ Recomendaciones específicas según el problema

---

## 🛡️ Verificar el Firewall de Windows

### Método 1: Verificar desde PowerShell

```powershell
# Ver reglas de firewall que afectan a Python
Get-NetFirewallRule | Where-Object {$_.DisplayName -like "*Python*"} | Format-Table DisplayName, Enabled, Direction, Action
```

### Método 2: Verificar desde la Interfaz Gráfica

1. **Abrir el Firewall de Windows Defender:**
   - Presiona `Win + R`
   - Escribe: `wf.msc`
   - Presiona Enter

2. **Verificar Reglas de Salida:**
   - En el panel izquierdo, haz clic en **"Reglas de salida"**
   - Busca reglas relacionadas con:
     - `Python`
     - `python.exe`
     - `pythonw.exe`
     - `Flask`

3. **Si no hay reglas o están bloqueadas:**
   - Haz clic derecho en **"Reglas de salida"** → **"Nueva regla..."**
   - Selecciona **"Programa"** → Siguiente
   - Selecciona **"Esta ruta del programa"**
   - Busca tu Python: `C:\Users\VICTUS\Documents\Kendo_Reparaciones\venv\Scripts\python.exe`
   - Selecciona **"Permitir la conexión"**
   - Aplica a todos los perfiles (Dominio, Privada, Pública)
   - Dale un nombre: "Python - Permitir conexiones salientes"

### Método 3: Deshabilitar temporalmente el Firewall (Solo para pruebas)

⚠️ **ADVERTENCIA:** Solo haz esto para probar. Vuelve a activarlo después.

```powershell
# Deshabilitar firewall temporalmente (requiere permisos de administrador)
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled False

# Para volver a activarlo:
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True
```

---

## 🌐 Resolver el Hostname Manualmente

### Método 1: Usar nslookup (Windows)

```powershell
# Resolver el hostname
nslookup db.utysncfiyunejnujadmk.supabase.co

# Si solo quieres la IP:
nslookup db.utysncfiyunejnujadmk.supabase.co | Select-String "Address" | Select-Object -Last 1
```

### Método 2: Usar ping (Windows)

```powershell
# Ping mostrará la IP resuelta
ping db.utysncfiyunejnujadmk.supabase.co
```

### Método 3: Usar el script de Python

El script `test_connection.py` ya hace esto automáticamente, pero puedes hacerlo manualmente:

```python
import socket

hostname = "db.utysncfiyunejnujadmk.supabase.co"

# Resolver a IPv4
try:
    ipv4 = socket.gethostbyname(hostname)
    print(f"IPv4: {ipv4}")
except:
    print("No se pudo resolver IPv4")

# Resolver a IPv6
try:
    ipv6_info = socket.getaddrinfo(hostname, None, socket.AF_INET6)
    if ipv6_info:
        ipv6 = ipv6_info[0][4][0]
        print(f"IPv6: {ipv6}")
except:
    print("No se pudo resolver IPv6")
```

### Método 4: Usar la IP directamente en el .env

Si logras resolver el hostname a una IP, puedes usar esa IP directamente en el archivo `.env`:

```env
# En lugar de:
DB_HOST=db.utysncfiyunejnujadmk.supabase.co

# Usa la IP resuelta (ejemplo):
DB_HOST=54.123.45.67
```

⚠️ **Nota:** Las IPs de Supabase pueden cambiar, así que esto es solo una solución temporal.

---

## 🔧 Soluciones Adicionales

### 1. Cambiar el DNS

Si el problema es de resolución DNS, puedes cambiar a DNS públicos:

```powershell
# Cambiar a DNS de Google (requiere permisos de administrador)
netsh interface ip set dns "Wi-Fi" static 8.8.8.8
netsh interface ip add dns "Wi-Fi" 8.8.4.4 index=2

# O usar DNS de Cloudflare
netsh interface ip set dns "Wi-Fi" static 1.1.1.1
netsh interface ip add dns "Wi-Fi" 1.0.0.1 index=2
```

### 2. Verificar el Antivirus

Algunos antivirus bloquean conexiones de red:
- Verifica la configuración de tu antivirus
- Agrega una excepción para Python
- O desactiva temporalmente el firewall del antivirus para probar

### 3. Verificar Proxy/VPN

Si usas un proxy o VPN:
- Desactívalo temporalmente para probar
- O configura Python para usar el proxy

### 4. Verificar que Supabase esté Activo

1. Ve a https://app.supabase.com
2. Selecciona tu proyecto
3. Verifica que el estado sea **"Active"** (no "Paused")
4. Si está pausado, reactívalo

### 5. Usar Connection Pooling de Supabase

Supabase ofrece connection pooling en el puerto 6543. Intenta cambiar el puerto en tu `.env`:

```env
DB_PORT=6543
```

---

## 📝 Pasos Recomendados

1. ✅ Ejecuta `python test_connection.py` para diagnóstico
2. ✅ Verifica el firewall de Windows
3. ✅ Verifica tu antivirus
4. ✅ Prueba resolver el hostname manualmente
5. ✅ Si todo falla, intenta usar la IP directamente (temporalmente)

---

## 🆘 Si Nada Funciona

1. Verifica en Supabase que el proyecto esté activo
2. Verifica que las credenciales en `.env` sean correctas
3. Intenta desde otra red (móvil, otro WiFi)
4. Contacta al soporte de Supabase si el problema persiste


