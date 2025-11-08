# Configuración de la Base de Datos

## Problema: Error de conexión a Supabase

Si estás viendo el error: `could not translate host name "db.utysncfiyunejnujadmk.supabase.co" to address`

## Solución

### Paso 1: Verificar conexión a internet
Asegúrate de tener conexión a internet activa.

### Paso 2: Crear archivo .env

Crea un archivo llamado `.env` en la raíz del proyecto (mismo nivel que `api/`, `templates/`, etc.) con el siguiente contenido:

```env
DB_HOST=db.utysncfiyunejnujadmk.supabase.co
DB_NAME=postgres
DB_USER=tu_usuario_de_supabase
DB_PASSWORD=tu_contraseña_de_supabase
DB_PORT=5432
SECRET_KEY=clave_secreta_super_segura
```

### Paso 3: Obtener credenciales de Supabase

1. Ve a tu panel de Supabase: https://app.supabase.com
2. Selecciona tu proyecto
3. Ve a **Settings** → **Database**
4. Busca la sección **Connection string** o **Connection info**
5. Copia los siguientes valores:
   - **Host**: Debería ser algo como `db.xxxxx.supabase.co`
   - **Database name**: Generalmente `postgres`
   - **User**: Generalmente `postgres`
   - **Password**: La contraseña que configuraste al crear el proyecto
   - **Port**: Generalmente `5432`

### Paso 4: Verificar el hostname

Si el hostname `db.utysncfiyunejnujadmk.supabase.co` no funciona:
- Verifica en tu panel de Supabase que el hostname sea correcto
- Es posible que el proyecto haya sido pausado o eliminado
- Verifica que el proyecto esté activo en Supabase

### Paso 5: Reiniciar el servidor

Después de crear el archivo `.env`, reinicia tu servidor Flask.

## Nota de Seguridad

⚠️ **IMPORTANTE**: El archivo `.env` contiene información sensible. 
- NO lo subas a Git
- Asegúrate de que esté en tu `.gitignore`


