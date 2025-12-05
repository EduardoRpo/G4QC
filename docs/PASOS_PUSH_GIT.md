# 🚀 Pasos para Subir Cambios - Solución Directa

## ❌ Error que Tienes

```
remote: Repository not found.
fatal: repository 'https://github.com/jgomezv2/G4QC.git/' not found
```

---

## ✅ Solución en 2 Pasos

### PASO 1: Verificar/Crear Repositorio en GitHub

**Abre en tu navegador:**
```
https://github.com/jgomezv2/G4QC
```

#### Si ves "404 Not Found" (repositorio no existe):

1. Ve a: **https://github.com/new**
2. **Repository name**: `G4QC`
3. **Description**: (opcional)
4. **Público o Privado**: Elige
5. **NO marques nada** (README, .gitignore, license)
6. Clic en **"Create repository"**

#### Si ves el repositorio (existe):

El problema es autenticación → Ve al PASO 2

---

### PASO 2: Configurar Autenticación

GitHub requiere un **Personal Access Token** (ya no acepta contraseñas).

#### Crear Token:

1. Ve a: **https://github.com/settings/tokens**
2. Clic: **"Generate new token"** → **"Generate new token (classic)"**
3. **Note**: `G4QC Token`
4. **Expiration**: 90 días (o sin expiración)
5. **Scopes**: Marca **`repo`** (todos los permisos)
6. Clic: **"Generate token"**
7. **COPIA EL TOKEN** (guárdalo, solo se muestra una vez)

#### Configurar Token en Git:

**Opción A: En la URL (Recomendado)**
```powershell
# Reemplaza TU_TOKEN con el token que copiaste
git remote set-url origin https://TU_TOKEN@github.com/jgomezv2/G4QC.git
```

**Opción B: Al hacer push (te pedirá credenciales)**
```powershell
git push origin main
# Username: jgomezv2
# Password: [pega el token aquí]
```

---

## 🎯 Comando Final

Una vez que:
- ✅ El repositorio existe en GitHub
- ✅ Tienes el token configurado

Ejecuta:
```powershell
git push origin main
```

---

## ✅ Verificar que Funcionó

Después del push deberías ver algo como:
```
Enumerating objects: 15, done.
Counting objects: 100% (15/15), done.
Delta compression using up to 8 threads
Compressing objects: 100% (10/10), done.
Writing objects: 100% (15/15), 2.5 KiB | 2.5 MiB/s, done.
Total 15 (delta 3), reused 0 (delta 0), pack-reused 0
To https://github.com/jgomezv2/G4QC.git
   63f2ce4..109ecdf  main -> main
```

---

## 🔍 Verificar Estado

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

## 💡 Resumen Ultra Rápido

1. **Verifica**: https://github.com/jgomezv2/G4QC existe?
   - NO → Créalo en https://github.com/new
   - SÍ → Ve al paso 2

2. **Token**: Crea token en https://github.com/settings/tokens
   - Scope: `repo`
   - Copia el token

3. **Configura**: 
   ```powershell
   git remote set-url origin https://TU_TOKEN@github.com/jgomezv2/G4QC.git
   ```

4. **Push**:
   ```powershell
   git push origin main
   ```

---

**¿Necesitas ayuda con algún paso específico?**

