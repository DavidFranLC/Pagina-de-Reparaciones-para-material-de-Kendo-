# 🔐 Verificar Credenciales de Supabase

## ⚠️ Error: "Tenant or user not found"

Este error significa que las credenciales (usuario o contraseña) son incorrectas.

---

## 🔍 Cómo Verificar las Credenciales

### 1. Verificar la Contraseña en Supabase

1. Ve a **Settings** → **Database** en Supabase
2. Busca la sección **"Database password"** o **"Reset database password"**
3. Si no recuerdas la contraseña, puedes:
   - **Verla** si está visible (algunos paneles la muestran)
   - **Resetearla** haciendo clic en "Reset database password"

### 2. Verificar el Usuario

El usuario para el pooler generalmente es:
- `postgres` (usuario estándar)
- O puede ser el mismo que tu proyecto

### 3. Verificar el Database Name

El nombre de la base de datos generalmente es:
- `postgres` (base de datos estándar)

---

## 📝 Formato Correcto del .env

Tu archivo `.env` debería verse así:

```env
DB_HOST=aws-0-us-east-2.pooler.supabase.com
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=tu_contraseña_correcta_aqui
DB_PORT=6543
SECRET_KEY=clave_secreta_super_segura
```

**Importante:**
- La contraseña debe ser **exactamente** la misma que configuraste en Supabase
- No debe tener espacios al inicio o al final
- Si la contraseña tiene caracteres especiales, asegúrate de que estén correctamente escritos

---

## 🔄 Resetear la Contraseña en Supabase

Si no recuerdas la contraseña:

1. Ve a **Settings** → **Database**
2. Busca la sección **"Database password"**
3. Haz clic en **"Reset database password"** o **"Generate new password"**
4. Copia la nueva contraseña
5. Actualiza el archivo `.env` con la nueva contraseña
6. Reinicia Flask

---

## ✅ Verificar que las Credenciales Son Correctas

Después de actualizar el `.env`, ejecuta:

```powershell
.\venv\Scripts\python.exe test_connection.py
```

Si las credenciales son correctas, deberías ver:
- ✅ Archivo .env encontrado
- ✅ Todas las variables configuradas
- ✅ Resolución DNS exitosa
- ✅ Puerto abierto

Pero para verificar la conexión real con las credenciales, necesitas probar desde Flask.

---

## 🆘 Si el Problema Persiste

1. **Verifica que el proyecto esté activo** (no pausado)
2. **Verifica que estés usando el pooler correcto** (Session mode, no Transaction mode)
3. **Intenta resetear la contraseña** en Supabase
4. **Verifica que no haya espacios** en el archivo `.env`

---

## 💡 Nota sobre el Error del Logo

El error `404 Not Found: /static/img/logo.webp` es un problema menor:
- El archivo `logo.webp` no existe en tu carpeta `static/img/`
- Esto no afecta la funcionalidad principal
- Puedes ignorarlo o crear/agregar el archivo logo.webp si lo necesitas


