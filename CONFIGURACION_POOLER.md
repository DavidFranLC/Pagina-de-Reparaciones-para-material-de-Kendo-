# 🔧 Configuración del Session Pooler de Supabase

## ⚠️ Problema: "Not IPv4 compatible"

Si ves el error **"Not IPv4 compatible"** en Supabase, significa que necesitas usar el **Session Pooler** en lugar de la conexión directa a PostgreSQL.

---

## 📋 Paso a Paso: Configurar el Session Pooler

### 1. Obtener las Credenciales del Pooler

1. Ve a tu panel de Supabase: https://app.supabase.com
2. Selecciona tu proyecto
3. Ve a **Settings** → **Database**
4. Busca la sección **"Connection pooling"** o **"Pooler settings"**
5. Verás algo como:

```
Session mode:
Host: aws-0-us-east-1.pooler.supabase.com
Port: 6543
Database: postgres
User: postgres
Password: [tu contraseña]
```

O una connection string:
```
postgresql://postgres:[PASSWORD]@aws-0-us-east-1.pooler.supabase.com:6543/postgres?pgbouncer=true
```

### 2. Formato del archivo .env con Pooler

Tu archivo `.env` debería verse así:

```env
DB_HOST=aws-0-us-east-1.pooler.supabase.com
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=tu_contraseña_de_supabase
DB_PORT=6543
SECRET_KEY=clave_secreta_super_segura
```

**Nota importante:**
- El **hostname** es diferente (termina en `.pooler.supabase.com`)
- El **puerto** es `6543` (no `5432`)
- El **database** sigue siendo `postgres`
- El **user** sigue siendo `postgres`

---

## 🔄 Actualizar el Código para Usar el Pooler

El código ya está preparado para usar el pooler. Solo necesitas:

1. Actualizar el archivo `.env` con el hostname y puerto del pooler
2. Reiniciar el servidor Flask

---

## ✅ Verificar la Configuración

Después de actualizar el `.env`, ejecuta:

```powershell
.\venv\Scripts\python.exe test_connection.py
```

Esto verificará si la conexión al pooler funciona.

---

## 📌 Diferencias Clave

| Tipo de Conexión | Hostname | Puerto | Uso |
|------------------|----------|--------|-----|
| **Directa** | `db.xxxxx.supabase.co` | `5432` | ❌ No compatible con IPv4 |
| **Session Pooler** | `aws-0-[region].pooler.supabase.com` | `6543` | ✅ Compatible con IPv4 |

---

## 🆘 Si No Encuentras el Pooler Settings

1. Ve a **Settings** → **Database**
2. Busca la pestaña o sección **"Connection pooling"**
3. Si no la ves, puede que necesites activarla primero
4. El hostname del pooler generalmente sigue el patrón:
   - `aws-0-[region].pooler.supabase.com`
   - Donde `[region]` es tu región (ej: `us-east-1`, `eu-west-1`, etc.)

---

## 💡 Ventajas del Session Pooler

- ✅ Compatible con IPv4
- ✅ Mejor rendimiento para aplicaciones web
- ✅ Manejo automático de conexiones
- ✅ Gratis en el plan gratuito de Supabase


