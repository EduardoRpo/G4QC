# 🚀 Comandos para Subir Cambios a GitHub

## ❌ Error Actual

```
remote: Repository not found.
fatal: repository 'https://github.com/jgomezv2/G4QC.git/' not found
```

## 🔍 Posibles Causas

1. **El repositorio no existe en GitHub** (no se ha creado)
2. **Problema de autenticación** (no tienes permisos)
3. **El repositorio es privado** y no estás autenticado

---

## ✅ Solución Paso a Paso

### Paso 1: Verificar si el Repositorio Existe

Abre en tu navegador:
```
https://github.com/jgomezv2/G4QC
```

**Si ves "404 Not Found":**
- El repositorio no existe → Necesitas crearlo (ver abajo)

**Si ves el repositorio:**
- El problema es autenticación → Ve al Paso 2

---

### Paso 2A: Si el Repositorio NO Existe - Crearlo

1. Ve a: https://github.com/new
2. **Repository name**: `G4QC`
3. **Description**: (opcional) "Trading Platform"
4. **Público o Privado**: Elige según prefieras
5. **NO marques**: "Add a README file", "Add .gitignore", "Choose a license"
   - (Ya tienes código local, no necesitas inicializar)
6. Clic en **"Create repository"**

---

### Paso 2B: Si el Repositorio SÍ Existe - Configurar Autenticación

GitHub ya no acepta contraseñas, necesitas un **Personal Access Token**:

#### Crear Token:

1. Ve a: https://github.com/settings/tokens
2. Clic en **"Generate new token"** → **"Generate new token (classic)"**
3. **Note**: `G4QC Development`
4. **Expiration**: Elige una fecha (ej: 90 días o sin expiración)
5. **Select scopes**: Marca **`repo`** (todos los permisos de repositorio)
6. Clic en **"Generate token"**
7. **COPIA EL TOKEN** (solo se muestra una vez, guárdalo)

#### Usar el Token:

**Opción A: Al hacer push (te pedirá credenciales)**
```powershell
git push origin main
```
- Username: `jgomezv2`
- Password: **Pega el token** (NO tu contraseña de GitHub)

**Opción B: Configurar en la URL (más fácil)**
```powershell
# Reemplaza TU_TOKEN con el token que copiaste
git remote set-url origin https://TU_TOKEN@github.com/jgomezv2/G4QC.git

# Luego hacer push normalmente
git push origin main
```

**Opción C: Usar SSH (más seguro)**
```powershell
# Cambiar a SSH
git remote set-url origin git@github.com:jgomezv2/G4QC.git

# Luego hacer push
git push origin main
```

---

## 🎯 Comandos Rápidos

### Si el repositorio NO existe:
1. Créalo en GitHub (Paso 2A)
2. Luego:
```powershell
git push -u origin main
```

### Si el repositorio SÍ existe:
1. Crea un Personal Access Token
2. Configúralo:
```powershell
git remote set-url origin https://TU_TOKEN@github.com/jgomezv2/G4QC.git
git push origin main
```

---

## ✅ Verificar que Funcionó

Después del push, deberías ver:
```
Enumerating objects: X, done.
Counting objects: 100% (X/X), done.
Writing objects: 100% (X/X), done.
To https://github.com/jgomezv2/G4QC.git
   abc1234..def5678  main -> main
```

---

## 🔍 Verificar Estado Después

```powershell
git status
```

Debería mostrar:
```
On branch main
Your branch is up to date with 'origin/main'.
nothing to commit, working tree clean
```

---

**¿El repositorio existe en GitHub o necesitas crearlo primero?**

