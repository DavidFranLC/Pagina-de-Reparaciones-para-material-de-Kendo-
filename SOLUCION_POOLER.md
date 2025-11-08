# Solución: Error "Tenant or user not found" con Supabase Pooler

## Problema

Cuando usas el **Session Pooler** de Supabase (puerto 6543), el formato del usuario debe incluir el identificador del proyecto.

## Solución

### 1. Agregar la variable `SUPABASE_PROJECT_REF` a tu archivo `.env`

El identificador del proyecto está en tu URL de Supabase:
- URL: `https://utysncfiyunejnujadmk.supabase.co`
- Identificador: `utysncfiyunejnujadmk`

Agrega esta línea a tu archivo `.env`:

```env
SUPABASE_PROJECT_REF=utysncfiyunejnujadmk
```

### 2. Formato del usuario con pooler

Con el pooler, el usuario debe tener el formato: `usuario.proyecto_ref`

**Ejemplo:**
- Usuario base: `postgres`
- Proyecto: `utysncfiyunejnujadmk`
- Usuario para pooler: `postgres.utysncfiyunejnujadmk`

El código ahora formatea automáticamente el usuario cuando detecta que estás usando el pooler.

### 3. Archivo `.env` completo

Tu archivo `.env` debe verse así:

```env
DB_HOST=aws-0-us-east-2.pooler.supabase.com
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=tu_contraseña_aqui
DB_PORT=6543
SUPABASE_PROJECT_REF=utysncfiyunejnujadmk
SECRET_KEY=clave_secreta_super_segura
```

### 4. Verificar la conexión

Después de actualizar el `.env`, ejecuta:

```powershell
.\venv\Scripts\python.exe test_db_connection.py
```

Deberías ver:
```
[OK] Conexion exitosa!
[OK] Version de PostgreSQL: ...
[OK] Todo funciona correctamente!
```

## Notas importantes

- El identificador del proyecto es la parte antes de `.supabase.co` en tu URL
- No cambies `DB_USER` a `postgres.utysncfiyunejnujadmk` manualmente
- El código formatea automáticamente el usuario cuando detecta el pooler
- Solo necesitas agregar `SUPABASE_PROJECT_REF` a tu `.env`

## ¿Dónde encontrar el identificador del proyecto?

1. Ve a https://app.supabase.com
2. Selecciona tu proyecto
3. Ve a Settings → General
4. El identificador está en "Reference ID" o en la URL del proyecto


