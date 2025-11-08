# 🔑 Cómo Obtener las Credenciales de Supabase para el archivo .env

## ⚠️ Diferencia Importante

La URL que tienes (`https://utysncfiyunejnujadmk.supabase.co`) es la **URL del proyecto** para usar la API REST de Supabase.

Para conectarte directamente a PostgreSQL con `psycopg2`, necesitas el **hostname de la base de datos**, que es diferente.

---

## 📋 Paso a Paso: Obtener las Credenciales

### 1. Ve a tu Panel de Supabase

1. Abre: https://app.supabase.com
2. Inicia sesión
3. Selecciona tu proyecto

### 2. Ve a la Configuración de la Base de Datos

1. En el menú lateral izquierdo, haz clic en **"Settings"** (Configuración) ⚙️
2. Luego haz clic en **"Database"** (Base de datos)

### 3. Busca la Sección "Connection string" o "Connection info"

En la página de Database, verás varias secciones. Busca una que diga:
- **"Connection string"** o
- **"Connection info"** o
- **"Connection pooling"**

### 4. Copia los Valores Necesarios

Verás algo como esto:

```
Host: db.utysncfiyunejnujadmk.supabase.co
Database name: postgres
Port: 5432
User: postgres
Password: [tu contraseña]
```

O una connection string como:
```
postgresql://postgres:[YOUR-PASSWORD]@db.utysncfiyunejnujadmk.supabase.co:5432/postgres
```

---

## 📝 Formato del archivo .env

Basándote en tu URL del proyecto (`https://utysncfiyunejnujadmk.supabase.co`), tu archivo `.env` debería verse así:

```env
DB_HOST=db.utysncfiyunejnujadmk.supabase.co
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=tu_contraseña_de_supabase
DB_PORT=5432
SECRET_KEY=clave_secreta_super_segura
```

### ⚠️ Nota Importante sobre el Hostname:

- ❌ **NO uses:** `https://utysncfiyunejnujadmk.supabase.co`
- ❌ **NO uses:** `utysncfiyunejnujadmk.supabase.co`
- ✅ **USA:** `db.utysncfiyunejnujadmk.supabase.co` (con "db." al inicio)

---

## 🔍 Si No Encuentras el Hostname

Si en el panel de Supabase no ves el hostname claramente, puedes:

### Opción 1: Construirlo Manualmente

Basándote en tu URL del proyecto:
- URL del proyecto: `https://utysncfiyunejnujadmk.supabase.co`
- Hostname de la BD: `db.utysncfiyunejnujadmk.supabase.co`

Simplemente agrega `db.` al inicio del dominio (sin el `https://`).

### Opción 2: Verificar en la Connection String

1. En Supabase, ve a **Settings** → **Database**
2. Busca la sección **"Connection string"**
3. Verás algo como:
   ```
   postgresql://postgres:[PASSWORD]@db.xxxxx.supabase.co:5432/postgres
   ```
4. El hostname es la parte después de `@` y antes de `:5432`

---

## ✅ Verificar que Funciona

Después de crear el archivo `.env`, ejecuta:

```powershell
.\venv\Scripts\python.exe test_connection.py
```

Este script verificará:
- ✅ Si el archivo `.env` existe
- ✅ Si todas las variables están configuradas
- ✅ Si se puede resolver el hostname
- ✅ Si el puerto está abierto

---

## 🆘 Si Tienes Problemas

1. **Verifica que el proyecto esté activo** (no pausado)
2. **Verifica que la contraseña sea correcta** (la que configuraste al crear el proyecto)
3. **Si olvidaste la contraseña**, puedes resetearla en Supabase:
   - Ve a **Settings** → **Database**
   - Busca la opción para resetear la contraseña

---

## 📌 Resumen Rápido

| Variable | Valor Ejemplo | Dónde Obtenerlo |
|----------|--------------|-----------------|
| `DB_HOST` | `db.utysncfiyunejnujadmk.supabase.co` | Settings → Database → Connection string |
| `DB_NAME` | `postgres` | Generalmente siempre es `postgres` |
| `DB_USER` | `postgres` | Generalmente siempre es `postgres` |
| `DB_PASSWORD` | `tu_contraseña` | La que configuraste al crear el proyecto |
| `DB_PORT` | `5432` | Generalmente siempre es `5432` |


