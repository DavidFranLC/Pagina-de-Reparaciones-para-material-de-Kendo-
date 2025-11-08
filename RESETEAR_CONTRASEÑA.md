# 🔐 Cómo Resetear la Contraseña de Supabase

## ⚠️ Error: "Tenant or user not found"

Este error significa que la **contraseña** en tu archivo `.env` no coincide con la contraseña real de Supabase.

---

## 🔄 Paso a Paso: Resetear la Contraseña

### 1. Ve a Settings → Database

1. Abre: https://app.supabase.com
2. Selecciona tu proyecto
3. Ve a **Settings** → **Database** (en el menú lateral)

### 2. Busca la Sección de Contraseña

En la página de Database, busca una sección que diga:
- **"Database password"** o
- **"Reset database password"** o
- **"Change database password"**

### 3. Resetear la Contraseña

1. Haz clic en **"Reset database password"** o **"Generate new password"**
2. Se generará una nueva contraseña
3. **Copia la contraseña inmediatamente** (algunas veces solo se muestra una vez)
4. Si no la copias, tendrás que resetearla de nuevo

### 4. Actualizar el archivo .env

Abre tu archivo `.env` y actualiza la contraseña:

```env
DB_HOST=aws-0-us-east-2.pooler.supabase.com
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=la_nueva_contraseña_aqui
DB_PORT=6543
SECRET_KEY=clave_secreta_super_segura
```

**⚠️ IMPORTANTE:**
- Copia la contraseña **exactamente** como aparece (sin espacios)
- No agregues comillas alrededor de la contraseña
- Si la contraseña tiene caracteres especiales, asegúrate de copiarlos correctamente

### 5. Reiniciar Flask

Después de actualizar el `.env`, **reinicia completamente** el servidor Flask:
1. Detén el servidor (Ctrl+C)
2. Inícialo de nuevo

---

## 🔍 Verificar la Contraseña Actual

Si no quieres resetear la contraseña, puedes intentar verificar cuál es:

1. Ve a **Settings** → **Database**
2. Busca si hay alguna sección que muestre la contraseña actual
3. Algunos paneles la muestran oculta (con asteriscos) o te permiten "mostrar" la contraseña

---

## ✅ Verificar que Funciona

Después de actualizar el `.env` con la contraseña correcta:

1. Reinicia Flask completamente
2. Intenta hacer login
3. Deberías ver en la consola:
   ```
   ℹ️ Usando Session Pooler: aws-0-us-east-2.pooler.supabase.com:6543
   ✅ Conexión exitosa a la base de datos
   ```

---

## 🆘 Si el Problema Persiste

1. **Verifica que no haya espacios** en el archivo `.env`:
   ```env
   # ❌ INCORRECTO (tiene espacios)
   DB_PASSWORD= mi_contraseña 
   
   # ✅ CORRECTO (sin espacios)
   DB_PASSWORD=mi_contraseña
   ```

2. **Verifica que el usuario sea "postgres"**:
   ```env
   DB_USER=postgres
   ```

3. **Verifica que el database sea "postgres"**:
   ```env
   DB_NAME=postgres
   ```

4. **Intenta resetear la contraseña de nuevo** si no estás seguro

---

## 📌 Resumen

1. Ve a **Settings** → **Database** en Supabase
2. Haz clic en **"Reset database password"**
3. Copia la nueva contraseña
4. Actualiza `DB_PASSWORD` en tu archivo `.env`
5. Reinicia Flask completamente
6. Prueba el login de nuevo


