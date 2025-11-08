# 📍 Dónde Encontrar las Credenciales del Pooler en Supabase

## ⚠️ La pantalla que estás viendo

La pantalla de **"Connection pooling configuration"** es para **configurar** el pooler (tamaño del pool, conexiones máximas), pero **NO** muestra las credenciales de conexión.

---

## 🔍 Dónde Están las Credenciales del Pooler

Las credenciales del pooler están en una sección diferente. Sigue estos pasos:

### Opción 1: Desde la Página Principal de Database

1. Ve a **Settings** → **Database** (en el menú lateral)
2. En la página de Database, busca una sección que diga:
   - **"Connection string"** o
   - **"Connection info"** o
   - **"Connection pooling"** (diferente a "Connection pooling configuration")
3. Deberías ver algo como:

```
Connection pooling
Session mode:
postgresql://postgres:[YOUR-PASSWORD]@aws-0-us-east-1.pooler.supabase.com:6543/postgres?pgbouncer=true
```

O en formato separado:
```
Host: aws-0-us-east-1.pooler.supabase.com
Port: 6543
Database: postgres
User: postgres
Password: [tu contraseña]
```

### Opción 2: Desde el Editor SQL

1. Ve a **SQL Editor** en el menú lateral
2. Haz clic en **"New query"**
3. En la parte superior, busca un botón o enlace que diga **"Connection info"** o **"Connection string"**
4. Ahí deberías ver las credenciales del pooler

### Opción 3: Construir el Hostname Manualmente

Si no encuentras las credenciales, puedes construir el hostname del pooler basándote en tu región:

1. Ve a **Settings** → **General**
2. Busca tu **región** (ej: `us-east-1`, `eu-west-1`, `ap-southeast-1`)
3. El hostname del pooler sigue este patrón:
   ```
   aws-0-[TU-REGION].pooler.supabase.com
   ```

Por ejemplo:
- Si tu región es `us-east-1`: `aws-0-us-east-1.pooler.supabase.com`
- Si tu región es `eu-west-1`: `aws-0-eu-west-1.pooler.supabase.com`

---

## 📝 Formato del archivo .env

Una vez que tengas el hostname del pooler, tu archivo `.env` debería verse así:

```env
DB_HOST=aws-0-us-east-1.pooler.supabase.com
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=tu_contraseña_de_supabase
DB_PORT=6543
SECRET_KEY=clave_secreta_super_segura
```

**Nota importante:**
- El **hostname** termina en `.pooler.supabase.com` (no `.supabase.co`)
- El **puerto** es `6543` (no `5432`)
- El **database** es `postgres`
- El **user** es `postgres`
- La **contraseña** es la misma que usas para la conexión directa

---

## 🔍 Buscar en la Página de Database

En la página de **Settings** → **Database**, busca:

1. **Pestañas o secciones** que digan:
   - "Connection string"
   - "Connection info"
   - "Connection pooling" (diferente a "Connection pooling configuration")
   - "Session mode"
   - "Transaction mode"

2. **Botones o enlaces** que digan:
   - "Copy connection string"
   - "Show connection string"
   - "Connection details"

3. **Código o texto** que contenga:
   - `pooler.supabase.com`
   - `:6543`
   - `postgresql://postgres:`

---

## ✅ Verificar que Funciona

Después de crear el archivo `.env` con las credenciales del pooler, ejecuta:

```powershell
.\venv\Scripts\python.exe test_connection.py
```

Esto verificará si la conexión al pooler funciona.

---

## 🆘 Si No Encuentras las Credenciales

1. **Verifica tu región** en Settings → General
2. **Construye el hostname** manualmente: `aws-0-[TU-REGION].pooler.supabase.com`
3. **Usa el puerto 6543** (siempre es el mismo para el pooler)
4. **Usa las mismas credenciales** que para la conexión directa (user: postgres, password: tu contraseña)

---

## 📌 Resumen Rápido

| Qué Buscar | Dónde Está |
|------------|------------|
| Hostname del pooler | Settings → Database → Connection pooling (NO "configuration") |
| Puerto | Siempre `6543` para el pooler |
| Database | Siempre `postgres` |
| User | Siempre `postgres` |
| Password | La misma que para la conexión directa |


