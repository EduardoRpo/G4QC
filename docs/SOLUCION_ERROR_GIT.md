# 🔧 Solución al Error "Repository not found"

## 🔍 Diagnóstico

El error "Git: remote: Repository not found" puede deberse a:

1. **El repositorio no existe en GitHub** (no se ha creado)
2. **Problemas de autenticación** (no tienes permisos o no estás autenticado)
3. **El repositorio es privado** y necesitas autenticarte
4. **El repositorio fue eliminado o renombrado**

---

## ✅ Soluciones

### Opción 1: Crear el Repositorio en GitHub (Si no existe)

1. Ve a: https://github.com/new
2. Nombre del repositorio: `G4QC`
3. Elige si será público o privado
4. **NO** inicialices con README, .gitignore o licencia (ya tienes código local)
5. Clic en "Create repository"

### Opción 2: Verificar Autenticación

Si el repositorio ya existe, el problema puede ser de autenticación:

#### Para HTTPS (lo que estás usando):
```powershell
# Verificar credenciales guardadas
git config --global credential.helper

# Si necesitas autenticarte, GitHub ahora requiere Personal Access Token
# Ve a: https://github.com/settings/tokens
# Crea un token con permisos "repo"
```

#### Cambiar a SSH (Alternativa):
```powershell
# Cambiar URL remota a SSH
git remote set-url origin git@github.com:jgomezv2/G4QC.git
```

### Opción 3: Verificar que el Repositorio Existe

Abre en el navegador:
```
https://github.com/jgomezv2/G4QC
```

Si ves "404 Not Found", el repositorio no existe y necesitas crearlo.

---

## 🚀 Pasos para Resolver

### Paso 1: Verificar si el repositorio existe

Abre: https://github.com/jgomezv2/G4QC

**Si NO existe:**
- Crea el repositorio en GitHub (Opción 1 arriba)

**Si SÍ existe:**
- El problema es de autenticación (Opción 2 arriba)

### Paso 2: Autenticarse (si el repo existe)

GitHub ya no acepta contraseñas, necesitas un **Personal Access Token**:

1. Ve a: https://github.com/settings/tokens
2. Clic en "Generate new token" → "Generate new token (classic)"
3. Dale un nombre (ej: "G4QC Development")
4. Selecciona scope: **`repo`** (todos los permisos de repo)
5. Genera el token
6. **Copia el token** (solo se muestra una vez)

### Paso 3: Usar el Token

Cuando hagas `git push`, te pedirá:
- **Username**: tu usuario de GitHub (jgomezv2)
- **Password**: **pega el token** (no tu contraseña)

O configúralo en la URL:
```powershell
git remote set-url origin https://TU_TOKEN@github.com/jgomezv2/G4QC.git
```

---

## 🔄 Alternativa: Usar SSH (Más Seguro)

### 1. Generar clave SSH (si no tienes):
```powershell
ssh-keygen -t ed25519 -C "tu_email@example.com"
```

### 2. Agregar clave a GitHub:
- Copia el contenido de: `~/.ssh/id_ed25519.pub`
- Ve a: https://github.com/settings/keys
- Agrega nueva SSH key

### 3. Cambiar remoto a SSH:
```powershell
git remote set-url origin git@github.com:jgomezv2/G4QC.git
```

---

## ✅ Verificar Configuración Actual

Tu configuración actual:
- **Remoto**: `https://github.com/jgomezv2/G4QC.git`
- **Branch local**: `main` (1 commit adelante)

---

## 🎯 Próximos Pasos

1. **Verifica si el repo existe**: https://github.com/jgomezv2/G4QC
2. **Si no existe**: Créalo en GitHub
3. **Si existe**: Configura autenticación (token o SSH)
4. **Intenta push de nuevo**: `git push origin main`

---

**¿El repositorio existe en GitHub o necesitas crearlo?**

